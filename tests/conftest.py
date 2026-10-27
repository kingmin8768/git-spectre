"""Shared fixtures: we build small haunted repositories for the exhumations."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

BASE_ENV = {
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "HOME": os.environ.get("HOME", "/tmp"),
    "LC_ALL": "C",
}


def git(repo: Path, *args: str, env_extra: dict | None = None, cwd: Path | None = None) -> str:
    env = os.environ.copy()
    env.update(BASE_ENV)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        ["git", "-C", str(cwd or repo), *args],
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0, f"git {' '.join(args)} failed:\n{proc.stderr}"
    return proc.stdout


def commit_file(repo: Path, relpath: str, content: str, message: str,
                author: str = "Ada Lovelace", email: str = "ada@analytical.engine",
                date: str | None = None) -> None:
    target = repo / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    env = {"GIT_AUTHOR_NAME": author, "GIT_AUTHOR_EMAIL": email,
           "GIT_COMMITTER_NAME": author, "GIT_COMMITTER_EMAIL": email}
    if date:
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    git(repo, "add", "-A", env_extra=env)
    git(repo, "commit", "-q", "-m", message, env_extra=env)


@pytest.fixture
def haunted_repo(tmp_path: Path) -> Path:
    """A repository with: a normal commit, a 3 AM lazy commit, dead code,
    and an unmerged zombie branch last touched in 2020."""
    repo = tmp_path / "haunted"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Ada Lovelace")
    git(repo, "config", "user.email", "ada@analytical.engine")

    # Commit 1: a decent, daylight commit.
    commit_file(
        repo, "engine.py",
        "def run():\n    return 'ok'\n",
        "feat: add the engine that runs",
        author="Ada Lovelace", date="2024-03-15T14:00:00+00:00",
    )

    # Commit 2: 3 AM, lazy message, by a different restless soul.
    commit_file(
        repo, "cursed.py",
        (
            "# TODO: fix this before the demo\n"
            "# def old_summoning():\n"
            "#     return 'spirit'\n"
            "@deprecated\n"
            "def summon():\n"
            "    return None  # FIXME: it returns nothing, like the void\n"
        ),
        "wip",
        author="Bob Cursed", email="bob@cursed.dev",
        date="2024-10-31T03:14:00+00:00",
    )

    # Zombie branch: a commit on 'doomed' that never reached main, dated 2020.
    git(repo, "checkout", "-q", "-b", "doomed")
    commit_file(
        repo, "ritual.txt", "unforgettable incantation\n",
        "experiment: the ritual that never shipped",
        author="Bob Cursed", date="2020-01-01T10:00:00+00:00",
    )
    git(repo, "checkout", "-q", "main")
    return repo


@pytest.fixture
def empty_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "empty"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    return repo


@pytest.fixture
def plain_dir(tmp_path: Path) -> Path:
    d = tmp_path / "not_a_repo"
    d.mkdir()
    return d