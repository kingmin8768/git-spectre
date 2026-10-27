"""git_scanner.py — the exhumation tools.

Every repository is a graveyard: commits are graves, branches are crypts,
and TODO comments are voices still whispering under the floorboards.
This module digs everything up (read-only — we never disturb the remains).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

RECORD_SEP = "\x1e"
UNIT_SEP = "\x1f"

DEAD_WORDS = ("TODO", "FIXME", "HACK", "XXX", "DEPRECATED")

# Languages where a '#' starts a comment.
HASH_COMMENT_EXT = {".py", ".sh", ".rb", ".yml", ".yaml", ".toml", ".r", ".pl"}
# Languages where '//' starts a comment.
SLASH_COMMENT_EXT = {
    ".js", ".ts", ".jsx", ".tsx", ".c", ".h", ".cc", ".cpp", ".hpp",
    ".java", ".go", ".rs", ".cs", ".swift", ".kt", ".scala", ".php",
}

HASH_CODE_RE = re.compile(
    r"^\s*#\s*(?:def\s|class\s|import\s|from\s|return\b|if\s|for\s|while\s|print\(|self\.)"
)
SLASH_CODE_RE = re.compile(
    r"^\s*//\s*(?:function\s|const\s|let\s|var\s|if\s|for\s|while\s|return\b|import\s|export\s|class\s)"
)
DEPRECATED_RE = re.compile(
    r"@(?:deprecated|Deprecated)|DeprecationWarning|\bdeprecated\b", re.IGNORECASE
)

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg",
    ".pdf", ".zip", ".gz", ".tar", ".7z", ".jar", ".woff", ".woff2",
    ".ttf", ".otf", ".eot", ".mp3", ".mp4", ".mov", ".avi", ".db", ".sqlite",
}


class RepoError(RuntimeError):
    """The spirits refuse to answer — this is not a git repository."""


@dataclass
class Commit:
    """One grave in the graveyard."""

    sha: str
    short: str
    author: str
    email: str
    date: datetime
    subject: str
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0

    @property
    def hour(self) -> int:
        return self.date.hour

    @property
    def weekday(self) -> int:
        return self.date.weekday()  # 0 = Monday, 6 = Sunday

    @property
    def is_nocturnal(self) -> bool:
        """Committed between 00:00 and 04:59 — the witching hours."""
        return self.hour < 5

    @property
    def is_lazy(self) -> bool:
        """A message too brief to summon anything."""
        msg = self.subject.strip()
        return len(msg) < 15 or msg.lower().startswith(("wip", "fix", "tmp", "asdf", "misc"))

    @property
    def is_colossal(self) -> bool:
        return (self.insertions + self.deletions) >= 500


@dataclass
class DeadThing:
    """Something that should be dead but isn't (or is dead but still here)."""

    kind: str          # "todo" | "commented_code" | "deprecated" | "zombie_branch"
    label: str         # the line of text, or the branch name
    where: str         # "path/file.py:42" or the branch name
    author: Optional[str] = None
    date: Optional[datetime] = None


@dataclass
class HauntReport:
    """The séance-room summary: how haunted is this repository?"""

    repo: str
    total_commits: int = 0
    authors: int = 0
    nocturnal_commits: int = 0
    lazy_messages: int = 0
    colossal_commits: int = 0
    todo_ghosts: int = 0
    commented_corpses: int = 0
    deprecated_tombstones: int = 0
    zombie_branches: int = 0
    haunt_index: int = 0
    grade: str = ""
    notes: List[str] = field(default_factory=list)


class RepoScanner:
    """Read-only exhumation of a git repository, via the git binary."""

    def __init__(self, path: str | Path = ".", now: Optional[datetime] = None):
        self.path = Path(path).resolve()
        self.now = now or datetime.now(timezone.utc)
        try:
            self._git("rev-parse", "--git-dir")
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise RepoError(f"{self.path} is not a git repository") from exc

    # ------------------------------------------------------------------ plumbing

    def _git(self, *args: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(self.path), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode != 0:
            raise RepoError(
                f"git {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}"
            )
        return proc.stdout

    # ------------------------------------------------------------------ commits

    def default_branch(self) -> Optional[str]:
        try:
            ref = self._git("symbolic-ref", "--short", "HEAD").strip()
        except RepoError:
            return None
        return ref or None

    def commits(self, max_count: Optional[int] = None) -> List[Commit]:
        fmt = (
            f"{RECORD_SEP}%H{UNIT_SEP}%h{UNIT_SEP}%an{UNIT_SEP}%ae"
            f"{UNIT_SEP}%aI{UNIT_SEP}%s"
        )
        args = ["log", f"--pretty=format:{fmt}", "--numstat", "--date=iso-strict"]
        if max_count:
            args.append(f"--max-count={max_count}")
        try:
            out = self._git(*args)
        except RepoError:
            return []  # unborn HEAD: a graveyard with no graves yet
        commits: List[Commit] = []
        for chunk in out.split(RECORD_SEP):
            chunk = chunk.strip("\n")
            if not chunk:
                continue
            lines = chunk.splitlines()
            fields = lines[0].split(UNIT_SEP)
            if len(fields) < 6:
                continue
            try:
                date = datetime.fromisoformat(fields[4])
            except ValueError:
                continue
            commit = Commit(
                sha=fields[0],
                short=fields[1],
                author=fields[2],
                email=fields[3],
                date=date,
                subject=fields[5],
            )
            for stat in lines[1:]:
                parts = stat.split("\t")
                if len(parts) >= 3 and parts[0] not in ("-", ""):
                    commit.files_changed += 1
                    try:
                        commit.insertions += int(parts[0])
                        commit.deletions += int(parts[1])
                    except ValueError:
                        pass
            commits.append(commit)
        return commits

    # ------------------------------------------------------------------ blame

    def blame(self, file_path: str) -> List[Dict[str, object]]:
        """Return one record per line of a tracked file: who wrote it, when, and why."""
        out = self._git("blame", "--line-porcelain", "--", file_path)
        records: List[Dict[str, object]] = []
        current: Dict[str, object] = {}
        lineno = 0
        for line in out.splitlines():
            if line.startswith("\t"):
                current["text"] = line[1:]
                current["line"] = lineno
                records.append(current)
                current = {}
                continue
            key, _, value = line.partition(" ")
            if key.isdigit() and not current:
                lineno = int(key.split()[0])
                current = {"sha": key, "author": None, "date": None, "summary": None}
            elif key == "author":
                current["author"] = value
            elif key == "author-time":
                try:
                    current["date"] = datetime.fromtimestamp(
                        int(value), tz=timezone.utc
                    )
                except (ValueError, OverflowError):
                    pass
            elif key == "summary":
                current["summary"] = value
        return records

    def blame_spirits(self, file_path: str) -> List[Tuple[str, int]]:
        """Authors ranked by how many lines of a file belong to them."""
        counts: Dict[str, int] = {}
        for record in self.blame(file_path):
            author = record.get("author") or "Unknown"
            counts[author] = counts.get(author, 0) + 1
        return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)

    def last_commit_touching(self, file_path: str) -> Optional[Commit]:
        try:
            out = self._git(
                "log", "-1",
                "--pretty=format:%H%x1f%h%x1f%an%x1f%ae%x1f%aI%x1f%s",
                "--", file_path,
            )
        except RepoError:
            return None
        fields = out.strip().split(UNIT_SEP)
        if len(fields) < 6:
            return None
        try:
            date = datetime.fromisoformat(fields[4])
        except ValueError:
            return None
        return Commit(sha=fields[0], short=fields[1], author=fields[2],
                      email=fields[3], date=date, subject=fields[5])

    # ------------------------------------------------------------------ branches

    def branches(self) -> List[Dict[str, object]]:
        out = self._git(
            "for-each-ref", "refs/heads",
            "--format=%(refname:short)%09%(committerdate:iso-strict)",
        )
        default = self.default_branch()
        result: List[Dict[str, object]] = []
        for line in out.splitlines():
            name, _, date_str = line.partition("\t")
            if not name:
                continue
            try:
                last = datetime.fromisoformat(date_str.strip())
            except ValueError:
                continue
            merged = True
            if default and name != default:
                probe = subprocess.run(
                    ["git", "-C", str(self.path), "merge-base", "--is-ancestor", name, default],
                    capture_output=True,
                )
                merged = probe.returncode == 0
            result.append({"name": name, "last": last, "merged": merged})
        return result

    # ------------------------------------------------------------------ dead code

    def tracked_files(self) -> List[str]:
        out = self._git("ls-files")
        return [line for line in out.splitlines() if line]

    def find_dead_code(self) -> List[DeadThing]:
        """Excavate TODOs, commented-out corpses, deprecated tombstones."""
        findings: List[DeadThing] = []
        for rel in self.tracked_files():
            suffix = Path(rel).suffix.lower()
            if suffix in BINARY_EXT:
                continue
            abs_path = self.path / rel
            try:
                text = abs_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, raw in enumerate(text.splitlines(), start=1):
                stripped = raw.strip()
                for word in DEAD_WORDS:
                    if word in raw:
                        findings.append(DeadThing(
                            kind="todo", label=stripped[:160],
                            where=f"{rel}:{lineno}",
                        ))
                        break
                if suffix in HASH_COMMENT_EXT and HASH_CODE_RE.match(raw):
                    findings.append(DeadThing(
                        kind="commented_code", label=stripped[:160],
                        where=f"{rel}:{lineno}",
                    ))
                elif suffix in SLASH_COMMENT_EXT and SLASH_CODE_RE.match(raw):
                    findings.append(DeadThing(
                        kind="commented_code", label=stripped[:160],
                        where=f"{rel}:{lineno}",
                    ))
                if DEPRECATED_RE.search(raw):
                    findings.append(DeadThing(
                        kind="deprecated", label=stripped[:160],
                        where=f"{rel}:{lineno}",
                    ))
        return findings

    def find_zombie_branches(self, days: int = 90) -> List[DeadThing]:
        """Branches that stopped breathing long ago and were never merged."""
        threshold = self.now.timestamp() - days * 86400
        zombies: List[DeadThing] = []
        for branch in self.branches():
            if branch["merged"]:
                continue
            last = branch["last"]
            if last.timestamp() < threshold:
                zombies.append(DeadThing(
                    kind="zombie_branch", label=str(branch["name"]),
                    where=str(branch["name"]), date=last,
                ))
        return zombies

    def all_dead_things(self, zombie_days: int = 90) -> List[DeadThing]:
        return self.find_dead_code() + self.find_zombie_branches(zombie_days)

    # ------------------------------------------------------------------ diagnose

    def diagnose(self, zombie_days: int = 90) -> HauntReport:
        commits = self.commits()
        total = len(commits)
        nocturnal = sum(1 for c in commits if c.is_nocturnal)
        lazy = sum(1 for c in commits if c.is_lazy)
        colossal = sum(1 for c in commits if c.is_colossal)
        findings = self.find_dead_code()
        todos = [f for f in findings if f.kind == "todo"]
        corpses = [f for f in findings if f.kind == "commented_code"]
        tombstones = [f for f in findings if f.kind == "deprecated"]
        zombies = self.find_zombie_branches(zombie_days)
        authors = len({c.author for c in commits})

        score = 0
        score += min(30, 2 * len(todos))
        score += min(20, 2 * len(corpses))
        score += min(10, 2 * len(tombstones))
        score += min(15, 5 * len(zombies))
        if total:
            score += int(25 * nocturnal / total)
            score += int(15 * lazy / total)
        score += min(10, 3 * colossal)
        score = min(100, score)

        notes: List[str] = []
        if total and authors == 1:
            notes.append("A single restless soul haunts this repository alone.")
        if nocturnal:
            notes.append(f"{nocturnal} commit(s) made between midnight and dawn.")
        if zombies:
            notes.append(f"{len(zombies)} zombie branch(es) never merged, never mourned.")

        report = HauntReport(
            repo=self.path.name,
            total_commits=total,
            authors=authors,
            nocturnal_commits=nocturnal,
            lazy_messages=lazy,
            colossal_commits=colossal,
            todo_ghosts=len(todos),
            commented_corpses=len(corpses),
            deprecated_tombstones=len(tombstones),
            zombie_branches=len(zombies),
            haunt_index=score,
            grade=haunt_grade(score),
            notes=notes,
        )
        return report


def haunt_grade(score: int) -> str:
    if score >= 85:
        return "Fully Possessed 💀 — the house is gone, the house is gone"
    if score >= 60:
        return "Séance Site 🔮 — spirits answer on every git pull"
    if score >= 30:
        return "Actively Haunted 😱 — cold spots in the blame"
    if score >= 10:
        return "Lightly Haunted 👻 — one candle flickers in the dark"
    return "Pristinely Poltergeist-Free 🕯️ — suspiciously clean"