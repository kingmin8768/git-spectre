"""Tests for the séance room: the typer CLI, end to end against real repos."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from git_spectre.cli import app

runner = CliRunner()


def invoke(repo: Path, *args: str):
    result = runner.invoke(app, ["--repo", str(repo), *args], env={"COLUMNS": "200", "LINES": "60"})
    if result.exception is not None and result.exit_code not in (0, 1):
        # surface the real traceback instead of swallowing it
        import traceback
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
    return result


def test_haunt_runs_against_a_haunted_repo(haunted_repo):
    result = invoke(haunted_repo, "haunt", "--last", "2")
    assert result.exit_code == 0
    out = result.output
    assert "git-spectre" in out
    assert "Bob Cursed" in out
    assert "wip" in out
    assert "Poltergeist" in out


def test_haunt_targets_a_specific_commit(haunted_repo):
    result = invoke(haunted_repo, "haunt", "--commit", "abc")
    # short sha of the head commit starts with something; find it via scanner
    from git_spectre.git_scanner import RepoScanner
    sha = RepoScanner(haunted_repo).commits()[0].short
    result = invoke(haunted_repo, "haunt", "--commit", sha)
    assert result.exit_code == 0
    assert sha in result.output


def test_haunt_unknown_commit_is_rejected(haunted_repo):
    result = invoke(haunted_repo, "haunt", "--commit", "deadbeef")
    assert result.exit_code == 1
    assert "deadbeef" in result.output


def test_seance_summons_the_head_spirit(haunted_repo):
    result = invoke(haunted_repo, "seance")
    assert result.exit_code == 0
    assert "SÉANCE" in result.output.upper() or "Séance" in result.output
    assert "Why did you write this?" in result.output


def test_seance_on_a_file_interrogates_its_author(haunted_repo):
    result = invoke(haunted_repo, "seance", "cursed.py")
    assert result.exit_code == 0
    assert "Bob Cursed" in result.output
    assert "cursed.py" in result.output


def test_seance_unknown_target_is_rejected(haunted_repo):
    result = invoke(haunted_repo, "seance", "phantom.py")
    assert result.exit_code == 1


def test_graveyard_raises_the_ofrenda(haunted_repo, tmp_path):
    out_file = tmp_path / "OFRENDA.md"
    result = invoke(haunted_repo, "graveyard", "--output", str(out_file))
    assert result.exit_code == 0
    assert out_file.exists()
    md = out_file.read_text(encoding="utf-8")
    assert "OFRENDA.md" in md
    assert "TODO" in md
    assert "doomed" in md  # the zombie branch is on the altar
    assert "Haunt Index" in md
    assert "Exhumation complete" in result.output


def test_graveyard_no_write_skips_the_file(haunted_repo, tmp_path):
    out_file = tmp_path / "OFRENDA.md"
    result = invoke(haunted_repo, "graveyard", "--output", str(out_file), "--no-write")
    assert result.exit_code == 0
    assert not out_file.exists()
    assert "The Exhumed" in result.output or "Exhumation complete" in result.output


def test_diagnose_reports_the_haunt_index(haunted_repo):
    result = invoke(haunted_repo, "diagnose")
    assert result.exit_code == 0
    assert "HAUNT INDEX" in result.output
    assert "/ 100" in result.output
    assert "Witching-hour commits" in result.output
    assert "Zombie branches" in result.output


def test_epitaph_known_and_unknown(haunted_repo):
    ok = invoke(haunted_repo, "epitaph", "cursed.py:1")
    assert ok.exit_code == 0
    assert "🕯️" in ok.output or "lies" in ok.output
    bad = invoke(haunted_repo, "epitaph", "nowhere:99")
    assert bad.exit_code == 1


def test_commands_fail_gracefully_outside_a_repository(plain_dir):
    result = invoke(plain_dir, "diagnose")
    assert result.exit_code == 1
    assert "spirits refuse" in result.output


def test_empty_repo_is_handled_with_courtesy(empty_repo):
    for args in (("haunt",), ("seance",)):
        result = invoke(empty_repo, *args)
        assert result.exit_code == 0
        assert "empty" in result.output.lower() or "no graves" in result.output.lower() or "no spirits" in result.output.lower()


def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "git-spectre" in result.output