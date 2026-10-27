"""graveyard.py — Día de los Muertos for your dead code.

Excavated remains are laid out on an ofrenda: a markdown altar (OFRENDA.md)
and a terminal wake. TODO ghosts get candles. Commented-out corpses get
marigolds. Zombie branches get a name written in sugar ink so they can
finally cross over (or be deleted with dignity).
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .git_scanner import DeadThing, HauntReport

KIND_TITLES = {
    "todo": "🕯️ TODO Ghosts — voices still whispering under the floorboards",
    "commented_code": "🥀 Commented-Out Corpses — neither code nor corpse",
    "deprecated": "🪦 Deprecated Tombstones — officially dead, still visited at 3 AM",
    "zombie_branch": "🧟 Zombie Branches — pushed, abandoned, never merged",
}

KIND_ICONS = {
    "todo": "🕯️",
    "commented_code": "🥀",
    "deprecated": "🪦",
    "zombie_branch": "🧟",
}

TOMBSTONE = """\
```
        ╔═══════════════════════╗
        ║         R. I. P.      ║
        ║                       ║
        ║      {label:<17} ║
        ║                       ║
        ║   {where:<19} ║
        ╚═══════════════════════╝
```"""


def group(findings: List[DeadThing]) -> dict:
    grouped: dict = {}
    for thing in findings:
        grouped.setdefault(thing.kind, []).append(thing)
    return grouped


def build_ofrenda(
    repo_name: str,
    findings: List[DeadThing],
    report: Optional[HauntReport] = None,
    generated_at: Optional[datetime] = None,
) -> str:
    """Render the full OFRENDA.md altar as markdown."""
    generated_at = generated_at or datetime.now()
    grouped = group(findings)
    lines: List[str] = []
    lines.append("# 🕯️ OFRENDA.md — Altar for the Departed Code")
    lines.append("")
    lines.append(
        f"> Built by **git-spectre** on {generated_at.strftime('%d %b %Y at %H:%M')} "
        f"for `{repo_name}`. In this repository we honor the dead code:\n"
        "> may it rest, or may it rise."
    )
    lines.append("")

    total = len(findings)
    lines.append("## 🌼 The Count of the Dead")
    lines.append("")
    lines.append("| Offering | Spirits |")
    lines.append("| --- | --- |")
    for kind in ("todo", "commented_code", "deprecated", "zombie_branch"):
        lines.append(f"| {KIND_ICONS[kind]} {kind} | {len(grouped.get(kind, []))} |")
    lines.append(f"| ✠ **Total souls** | **{total}** |")
    lines.append("")
    if report is not None:
        lines.append(
            f"**Haunt Index: {report.haunt_index}/100 — {report.grade}**"
        )
        lines.append("")

    lines.append("## 🧡 The Ofrenda")
    lines.append("")
    lines.append("On this altar we place, in the tradition of Día de los Muertos:")
    lines.append("")
    lines.append("- 🌼 **Marigolds** (*cempasúchil*), so the dead code can find its way home")
    lines.append("- 🕯️ **Candles**, one for every TODO that was never a ticket")
    lines.append("- 🍞 **Pan de código**: bread for the maintainers who come after us")
    lines.append("- 🧂 **Salt**, for preservation — see also: every commented-out function")
    lines.append("")

    for kind in ("todo", "commented_code", "deprecated", "zombie_branch"):
        items = grouped.get(kind, [])
        if not items:
            continue
        lines.append(f"## {KIND_TITLES[kind]} ({len(items)})")
        lines.append("")
        for thing in items:
            lines.append(TOMBSTONE.format(
                label=(thing.label or thing.kind)[:17],
                where=thing.where[:19],
            ))
            lines.append("")
            lines.append(f"> *“{thing.label or thing.kind}”*")
            lines.append("")

    lines.append("## ✝️ Rites of Resurrection")
    lines.append("")
    lines.append("To help the dead cross over (or be laid to rest):")
    lines.append("")
    lines.append("1. **TODO ghosts** — turn each candle into a ticket, or blow it out.")
    lines.append("2. **Commented-out corpses** — version control already remembers them. Delete with dignity.")
    lines.append("3. **Deprecated tombstones** — schedule the funeral; remove the last callers.")
    lines.append("4. **Zombie branches** — merge, or close the crypt. A branch unmerged for 90+ days is not resting, it is rotting.")
    lines.append("")
    lines.append("*Generated locally. Nothing left this machine to make this altar.*")
    lines.append("")
    return "\n".join(lines)