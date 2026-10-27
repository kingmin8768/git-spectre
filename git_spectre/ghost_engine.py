"""ghost_engine.py — the voices of the dead.

Dual-mode by design:

1. **Gemma mode** — if Ollama is installed and a Gemma open-weight model is
   pulled, every séance is narrated by a genuinely local LLM. Code, commit
   history and blame never leave the machine.
2. **Standalone mode** — if no model is present, the StandaloneHauntedEngine
   takes over: a deterministic, hash-seeded template engine that reads the
   *shape* of the history (witching-hour commits, lazy messages, colossi)
   and improvises a haunting from it. Still 100% offline, still 100% private.

Privacy is not a fallback here; it is the whole point. Both modes run with
zero network calls.
"""

from __future__ import annotations

import hashlib
import random
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional

from .git_scanner import Commit, DeadThing, RepoScanner

WITCHING_HOURS = range(0, 5)

# --------------------------------------------------------------------------- #
#  Standalone Haunted Engine
# --------------------------------------------------------------------------- #

PERSONAS = {
    "poltergeist": "The 3 AM Poltergeist 🕒",
    "wraith": "The Weekend Wraith 📅",
    "colossus": "The Colossus 👹",
    "bandido": "The Bearer of 'WIP' 🩹",
    "ghost": "The Forgotten Contributor 👻",
    "archivist": "The Ancient Archivist 📜",
}

QUIPS_NOCTURNAL = [
    "{author} pushed '{msg}' at {hour_str} — a time when even the servers pretend to sleep. Nothing written at that hour has ever been wise.",
    "This was written at {hour_str}. The dead keep those hours. So, apparently, did {author}.",
    "{n_changed} lines changed at {hour_str}. Coffee was involved. Judgment was not.",
]

QUIPS_LAZY = [
    "'{msg}' — the entire message. {author} looked upon {n_changed} changed lines and chose brevity over honesty. The grave marker says nothing, and so it says everything.",
    "The commit message reads '{msg}'. Archaeologists of the future will weep.",
    "'{msg}'. Two words. {n_changed} lines of consequence. A warning to us all.",
]

QUIPS_COLOSSAL = [
    "{n_changed} lines in a single commit. {author} did not write code; {author} performed a land acquisition.",
    "This commit is not reviewed, it is excavated. {n_changed} lines — no reviewer survives that without becoming one of us.",
]

QUIPS_DEFAULT = [
    "{author} wrote this on a {day_name}. A {day_name}! Some spirits never learned mercy.",
    "'{msg}' — said with such confidence, {n_changed} lines ago. History disagrees with the confidence.",
    "The code was changed {n_changed} lines' worth, then abandoned to time. Time always collects.",
]

QUIPS_OLD = [
    "This grave dates to {date_str}. Whatever problem it solved, the problem has since been reborn twice.",
    "{author} left this on {date_str} and never returned. Some say they still review PRs in the cloud.",
]

SEANCE_QUESTIONS = [
    "Why did you write this?",
    "What were you thinking at the time?",
    "Do you repent?",
]

SEANCE_ANSWERS_NOCTURNAL = [
    "It was {hour_str}. I thought I was brilliant. I was merely awake.",
    "The build was broken. The coffee was gone. The code wrote itself and I signed it.",
    "I repent of nothing at {hour_str}. Repentance requires consciousness.",
]

SEANCE_ANSWERS_DEFAULT = [
    "The ticket said 'urgent'. Nothing is urgent after three years, and yet here I am, summoned.",
    "I was young. The tests were few. You have inherited both my shortcuts and my shame.",
    "I meant to clean it up the following sprint. The following sprint became eternity.",
]

SEANCE_ANSWERS_LAZY = [
    "The message was '{msg}' because the truth was too long for the terminal.",
    "I wrote '{msg}' so future me would understand. Future me is you. I have failed.",
]

SEANCE_ANSWERS_COLOSSAL = [
    "I moved {n_changed} lines in one commit because splitting it was, in my judgment, unnecessary. My judgment is why you are holding this séance.",
]

SEANCE_FILE_ANSWERS = [
    "I wrote it because the deadline was a cliff and I was the cart.",
    "Half of it is mine. The other half was mine, until someone 'refactored' the soul out of it.",
    "Read the blame. My fingerprints are on every line you are afraid to touch.",
]

CLOSING_BENEDICTIONS = [
    "Go in peace. Do not refactor my work on a Friday.",
    "We are what we commit. Commit wisely.",
    "The candle is lit. The blame is read. You may log off now.",
]


@dataclass
class Seance:
    """A transcript of one interrogation of one summoned spirit."""

    spirit: str
    subject: str
    lines: List[str]

    def as_text(self) -> str:
        head = f"SÉANCE — {self.spirit} on '{self.subject}'"
        return head + "\n" + "\n".join(self.lines)


class StandaloneHauntedEngine:
    """A rule- and template-based engine that never needs a model, a GPU,
    or a network. Deterministic per commit (hash-seeded), so the same
    haunting is reproducible for screenshots and CI."""

    name = "standalone"

    def __init__(self, seed: Optional[int] = None):
        self._fixed_seed = seed

    def _rng(self, commit: Commit) -> random.Random:
        digest = hashlib.sha256(commit.sha.encode()).hexdigest()
        return random.Random(int(digest[:16], 16) if self._fixed_seed is None else self._fixed_seed)

    def persona_for(self, commit: Commit) -> str:
        if commit.is_colossal:
            return PERSONAS["colossus"]
        if commit.is_nocturnal:
            return PERSONAS["poltergeist"]
        if commit.is_lazy:
            return PERSONAS["bandido"]
        if commit.weekday >= 4:
            return PERSONAS["wraith"]
        return PERSONAS["ghost"]

    def haunt(self, commit: Commit, file_hint: Optional[str] = None) -> str:
        rng = self._rng(commit)
        persona = self.persona_for(commit)
        fields = {
            "author": commit.author,
            "msg": commit.subject,
            "hour_str": f"{commit.hour:02d}:{commit.date.minute:02d} AM-ish",
            "hour": commit.hour,
            "day_name": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][commit.weekday],
            "n_changed": commit.insertions + commit.deletions,
            "date_str": commit.date.strftime("%d %b %Y"),
        }
        bank: List[str] = []
        if commit.is_nocturnal:
            bank += QUIPS_NOCTURNAL
        if commit.is_lazy:
            bank += QUIPS_LAZY
        if commit.is_colossal:
            bank += QUIPS_COLOSSAL
        if not bank:
            bank = QUIPS_DEFAULT
        if file_hint:
            bank = bank + [q + f" (The haunting centres on {file_hint}.)" for q in bank]
        quips = [rng.choice(bank).format(**fields) for _ in range(2)]
        extra = rng.choice(QUIPS_OLD).format(**fields)
        return (
            f"{persona}\n"
            f"   ✦ {quips[0]}\n"
            f"   ✦ {quips[1]}\n"
            f"   ✦ {extra}"
        )

    def seance(self, commit: Commit, blame_summary: str = "") -> Seance:
        rng = self._rng(commit)
        spirit_name = f"{commit.author} (departed {commit.date.strftime('%d %b %Y')})"
        fields = {
            "author": commit.author,
            "msg": commit.subject,
            "hour_str": f"{commit.hour:02d}:{commit.date.minute:02d}",
            "n_changed": commit.insertions + commit.deletions,
        }
        if commit.is_nocturnal:
            answer_bank = SEANCE_ANSWERS_NOCTURNAL
        elif commit.is_lazy:
            answer_bank = SEANCE_ANSWERS_LAZY
        elif commit.is_colossal:
            answer_bank = SEANCE_ANSWERS_COLOSSAL
        else:
            answer_bank = SEANCE_ANSWERS_DEFAULT
        lines: List[str] = []
        for question, answer in zip(SEANCE_QUESTIONS, answer_bank):
            lines.append(f"  Q: {question}")
            lines.append(f"  A: {answer.format(**fields)}")
        if blame_summary:
            lines.append(f"  Q: Who else touched what you touched?")
            lines.append(f"  A: {blame_summary} Their fingerprints are everywhere. So are mine.")
        lines.append(f"  ✧ {rng.choice(CLOSING_BENEDICTIONS)}")
        return Seance(spirit=spirit_name, subject=commit.subject, lines=lines)


# --------------------------------------------------------------------------- #
#  Gemma mode (Ollama)
# --------------------------------------------------------------------------- #

OLLAMA_PROMPT = """You are the ghost of a developer haunting a git repository.
Stay in character: eerie, witty, briefly mocking, never cruel.
Commit author: {author}
Commit time: {date}
Commit message: {subject}
Lines changed: {n}
{extra}
In at most 6 short lines, react to this commit as its ghost would: one
spooky observation about the hour or the habit, one pointed remark about
the change, one cryptic warning for whoever inherits the code.
Do not mention that you are an AI. Do not use markdown headers."""


class OllamaGemmaEngine:
    """Narrates hauntings with a local Gemma model served by Ollama."""

    name = "gemma"

    def __init__(self, model: str, binary: str = "ollama"):
        self.model = model
        self.binary = binary
        self._fallback = StandaloneHauntedEngine()

    def _generate(self, prompt: str, timeout: int = 120) -> str:
        proc = subprocess.run(
            [self.binary, "run", self.model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            raise RuntimeError(f"ollama run failed: {proc.stderr.strip()[:200]}")
        return proc.stdout.strip()

    def haunt(self, commit: Commit, file_hint: Optional[str] = None) -> str:
        extra = f"File of interest: {file_hint}" if file_hint else ""
        prompt = OLLAMA_PROMPT.format(
            author=commit.author,
            date=commit.date.isoformat(),
            subject=commit.subject,
            n=commit.insertions + commit.deletions,
            extra=extra,
        )
        try:
            body = self._generate(prompt)
        except (RuntimeError, subprocess.SubprocessError, OSError):
            return self._fallback.haunt(commit, file_hint)
        return f"{self.persona_for(commit)} (via {self.model})\n{body}"

    def persona_for(self, commit: Commit) -> str:
        return self._fallback.persona_for(commit)

    def seance(self, commit: Commit, blame_summary: str = "") -> Seance:
        prompt = OLLAMA_PROMPT.format(
            author=commit.author,
            date=commit.date.isoformat(),
            subject=commit.subject,
            n=commit.insertions + commit.deletions,
            extra=f"Blame summary: {blame_summary}" if blame_summary else "",
        ) + "\nAnswer three questions — why you wrote it, what you were thinking, whether you repent — as the ghost, in a short dialogue."
        try:
            body = self._generate(prompt)
        except (RuntimeError, subprocess.SubprocessError, OSError):
            return self._fallback.seance(commit, blame_summary)
        return Seance(spirit=commit.author, subject=commit.subject, lines=["  " + line for line in body.splitlines() if line.strip()])


# --------------------------------------------------------------------------- #
#  Engine selection
# --------------------------------------------------------------------------- #

def detect_ollama_gemma(model_hint: str = "gemma") -> Optional[str]:
    """Return the exact Ollama model name if a Gemma-family model is pulled,
    else None. Never touches the network."""
    if shutil.which("ollama") is None:
        return None
    try:
        proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=15)
    except (subprocess.SubprocessError, OSError):
        return None
    if proc.returncode != 0:
        return None
    for line in proc.stdout.splitlines()[1:]:
        name = line.split()[0] if line.split() else ""
        if model_hint.lower() in name.lower():
            return name
    return None


def get_engine(model_hint: str = "gemma"):
    """Return (engine, mode_label). Gemma when available, standalone otherwise."""
    model = detect_ollama_gemma(model_hint)
    if model:
        return OllamaGemmaEngine(model), f"ollama:{model}"
    return StandaloneHauntedEngine(), "standalone"


def epitaph_for(thing: DeadThing, scanner: RepoScanner) -> str:
    """A one-line epitaph for a dead thing, used on tombstones."""
    rng = random.Random(hash(thing.where) & 0xFFFF)
    if thing.kind == "todo":
        return rng.choice([
            "It promised to be fixed 'later'. Later never filed a ticket.",
            "Here lies a note to the future. The future never reads.",
        ])
    if thing.kind == "commented_code":
        return rng.choice([
            "Commented out, never deleted. The classic limbo.",
            "It lives in a comment now. Neither code nor corpse.",
        ])
    if thing.kind == "deprecated":
        return rng.choice([
            "Marked deprecated. Mourned by none. Called by one legacy endpoint.",
            "Officially dead. Still receives visitors every night at 3 AM.",
        ])
    if thing.kind == "zombie_branch":
        return rng.choice([
            "It never crossed over to main. It never will.",
            "Pushed, abandoned, unmerged. The crypt door is still open.",
        ])
    return "Here lies code nobody remembers writing."