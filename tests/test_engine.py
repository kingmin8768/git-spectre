"""Tests for the voices of the dead: ghost_engine."""

from __future__ import annotations

from datetime import datetime, timezone

from git_spectre.git_scanner import Commit
from git_spectre.ghost_engine import (
    StandaloneHauntedEngine,
    detect_ollama_gemma,
    epitaph_for,
    get_engine,
)
from git_spectre.git_scanner import DeadThing


def make_commit(**overrides) -> Commit:
    base = dict(
        sha="a" * 40,
        short="abc1234",
        author="Bob Cursed",
        email="bob@cursed.dev",
        date=datetime(2024, 10, 31, 3, 14, tzinfo=timezone.utc),
        subject="wip",
        files_changed=2,
        insertions=120,
        deletions=3,
    )
    base.update(overrides)
    return Commit(**base)


def test_nocturnal_commit_raises_the_poltergeist():
    engine = StandaloneHauntedEngine()
    haunting = engine.haunt(make_commit())
    assert "Poltergeist" in haunting
    assert "Bob Cursed" in haunting
    assert "wip" in haunting


def test_colossal_commit_raises_the_colossus():
    engine = StandaloneHauntedEngine()
    haunting = engine.haunt(make_commit(insertions=900, deletions=50, subject="refactor everything"))
    assert "Colossus" in haunting
    assert "950" in haunting


def test_haunting_is_deterministic_per_commit():
    engine = StandaloneHauntedEngine()
    first = engine.haunt(make_commit())
    second = engine.haunt(make_commit())
    assert first == second


def test_different_commits_are_haunted_differently():
    engine = StandaloneHauntedEngine()
    a = engine.haunt(make_commit(sha="a" * 40))
    b = engine.haunt(make_commit(sha="b" * 40))
    assert a != b


def test_seance_transcript_answers_questions():
    engine = StandaloneHauntedEngine()
    seance = engine.seance(make_commit(), blame_summary="Top spirit: Bob Cursed holds 6 lines.")
    text = seance.as_text()
    assert "Why did you write this?" in text
    assert "Do you repent?" in text
    assert "Bob Cursed" in text
    assert "Top spirit: Bob Cursed holds 6 lines." in text
    assert "wip" in text  # the spirit is confronted with its own message


def test_seance_of_a_daylight_honest_commit_differs_from_nocturnal():
    engine = StandaloneHauntedEngine()
    nocturnal = engine.seance(make_commit())
    daylight = engine.seance(make_commit(
        sha="c" * 40,
        date=datetime(2024, 10, 31, 14, 0, tzinfo=timezone.utc),
        subject="feat: add the engine that runs",
    ))
    assert nocturnal.lines != daylight.lines


def test_epitaphs_vary_by_kind():
    for kind in ("todo", "commented_code", "deprecated", "zombie_branch"):
        thing = DeadThing(kind=kind, label="remains", where="cursed.py:1")
        assert epitaph_for(thing, None)  # type: ignore[arg-type]


def test_engine_selection_falls_back_to_standalone():
    engine, mode = get_engine()
    if detect_ollama_gemma() is None:
        assert mode == "standalone"
        assert engine.name == "standalone"


def test_gemma_detection_returns_none_without_ollama():
    import shutil
    if shutil.which("ollama") is not None:
        # Ollama exists here; Gemma may or may not be pulled — just require a sane result.
        result = detect_ollama_gemma()
        assert result is None or "gemma" in result.lower()
    else:
        assert detect_ollama_gemma() is None