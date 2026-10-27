"""Tests for the exhumation tools: RepoScanner."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from git_spectre.git_scanner import RepoError, RepoScanner, haunt_grade

NOW = datetime(2025, 11, 1, 12, 0, tzinfo=timezone.utc)


def test_non_repository_raises(plain_dir):
    with pytest.raises(RepoError):
        RepoScanner(plain_dir)


def test_commits_are_parsed_with_metadata(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=NOW)
    commits = scanner.commits()
    assert len(commits) == 2
    head = commits[0]  # most recent first
    assert head.author == "Bob Cursed"
    assert head.subject == "wip"
    assert head.date.hour == 3
    assert head.is_nocturnal is True
    assert head.is_lazy is True
    older = commits[1]
    assert older.author == "Ada Lovelace"
    assert older.is_nocturnal is False
    assert older.is_lazy is False
    assert older.files_changed == 1
    assert older.insertions == 2


def test_blame_attributes_lines_to_authors(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=NOW)
    records = scanner.blame("cursed.py")
    assert len(records) == 6
    authors = {r["author"] for r in records}
    assert "Bob Cursed" in authors
    spirits = scanner.blame_spirits("cursed.py")
    assert spirits[0][0] == "Bob Cursed"
    assert spirits[0][1] == 6


def test_last_commit_touching_returns_commit(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=NOW)
    commit = scanner.last_commit_touching("engine.py")
    assert commit is not None
    assert commit.author == "Ada Lovelace"
    assert "engine" in commit.subject


def test_dead_code_findings_are_excavated(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=NOW)
    findings = scanner.find_dead_code()
    kinds = {f.kind for f in findings}
    assert {"todo", "commented_code", "deprecated"} <= kinds
    todos = [f for f in findings if f.kind == "todo"]
    assert any("TODO: fix this before the demo" in f.label for f in todos)
    commented = [f for f in findings if f.kind == "commented_code"]
    assert any("old_summoning" in f.label for f in commented)
    deprecated = [f for f in findings if f.kind == "deprecated"]
    assert any(f.where.startswith("cursed.py:") for f in deprecated)
    # every finding carries a file:line location
    for f in findings:
        assert f.where and ":" in f.where


def test_zombie_branch_is_found_by_age_and_unmerged(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=NOW)
    zombies = scanner.find_zombie_branches(days=90)
    assert [z.label for z in zombies] == ["doomed"]
    assert zombies[0].date.year == 2020


def test_young_unmerged_branch_is_not_a_zombie(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=datetime(2020, 1, 2, tzinfo=timezone.utc))
    assert scanner.find_zombie_branches(days=90) == []


def test_diagnose_produces_scores_and_notes(haunted_repo):
    scanner = RepoScanner(haunted_repo, now=NOW)
    report = scanner.diagnose()
    assert 0 <= report.haunt_index <= 100
    assert report.total_commits == 2
    assert report.authors == 2
    assert report.nocturnal_commits == 1
    assert report.todo_ghosts >= 1
    assert report.zombie_branches == 1
    assert report.grade
    assert report.authors == 2  # two spirits share this graveyard
    assert any("midnight" in n for n in report.notes)
    assert any("zombie branch" in n for n in report.notes)


def test_haunt_grade_tiers():
    assert "Pristinely" in haunt_grade(0)
    assert "Lightly" in haunt_grade(10)
    assert "Actively" in haunt_grade(45)
    assert "Séance" in haunt_grade(70)
    assert "Fully Possessed" in haunt_grade(95)


def test_empty_repository_yields_no_commits(empty_repo):
    scanner = RepoScanner(empty_repo, now=NOW)
    assert scanner.commits() == []
    report = scanner.diagnose()
    assert report.total_commits == 0
    assert report.haunt_index >= 0