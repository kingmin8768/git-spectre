"""Tests for the altar builder: graveyard / OFRENDA.md."""

from __future__ import annotations

from datetime import datetime, timezone

from git_spectre.git_scanner import DeadThing
from git_spectre.graveyard import build_ofrenda, group

FINDINGS = [
    DeadThing(kind="todo", label="TODO: fix this before the demo", where="cursed.py:1"),
    DeadThing(kind="commented_code", label="# def old_summoning():", where="cursed.py:2"),
    DeadThing(kind="deprecated", label="@deprecated", where="cursed.py:4"),
    DeadThing(kind="zombie_branch", label="doomed", where="doomed"),
]


def test_ofrenda_contains_every_section():
    md = build_ofrenda("haunted", FINDINGS, generated_at=datetime(2025, 11, 1, 9, 0))
    assert "# 🕯️ OFRENDA.md" in md
    assert "`haunted`" in md
    for header in ("TODO Ghosts", "Commented-Out Corpses", "Deprecated Tombstones", "Zombie Branches"):
        assert header in md
    assert "Rites of Resurrection" in md


def test_ofrenda_counts_the_dead():
    md = build_ofrenda("haunted", FINDINGS)
    for kind, count in (("todo", 1), ("commented_code", 1), ("deprecated", 1), ("zombie_branch", 1)):
        row = next(line for line in md.splitlines() if kind in line and "|" in line)
        assert f"| {count} |" in row
    assert "**Total souls** | **4**" in md


def test_ofrenda_tombstones_carry_locations():
    md = build_ofrenda("haunted", FINDINGS)
    assert "cursed.py:1" in md
    assert "doomed" in md
    assert "R. I. P." in md


def test_ofrenda_with_no_dead_is_still_an_altar():
    md = build_ofrenda("clean", [], generated_at=datetime(2025, 11, 1))
    assert "# 🕯️ OFRENDA.md" in md
    assert "Total souls" in md


def test_group_buckets_by_kind():
    grouped = group(FINDINGS)
    assert set(grouped) == {"todo", "commented_code", "deprecated", "zombie_branch"}
    assert grouped["zombie_branch"][0].label == "doomed"


def test_ofrenda_mentions_privacy():
    md = build_ofrenda("haunted", FINDINGS)
    assert "Nothing left this machine" in md
    assert datetime.now(timezone.utc).year  # sanity: our clock is sane