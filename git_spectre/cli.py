"""cli.py — the séance room. A typer app with gothic taste."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.text import Text

from . import __version__
from .git_scanner import Commit, RepoError, RepoScanner
from .ghost_engine import epitaph_for, get_engine
from .graveyard import KIND_ICONS, build_ofrenda, group

theme = Theme({
    "ghost": "magenta",
    "candle": "bright_yellow",
    "grave": "bright_black",
    "blood": "bold red",
    "marigold": "bright_yellow",
    "spectre": "bold cyan",
})

console = Console(theme=theme)
err_console = Console(theme=theme, stderr=True)

BANNER = r"""
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
 ⣿   ⢠⣤⣶⣶⣦⡀                                              ⣿
 ⣿   ⢸⣿⠋⠙⠛⠛⢿⣷      g i t - s p e c t r e                  ⣿
 ⣿    ⠙⠶⠶⠶⠶⠶⠛⠋   the haunted git history & digital séance  ⣿
 ⣿                                                             ⣿
 ⣿        ·˚🕯️ git-spectre · the dead read your diffs · 🕯️·˚            ⣿
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""

_repo_path: Path = Path(".")


app = typer.Typer(
    help="git-spectre — summon the ghosts of your git history with a local AI.",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
)


@app.callback()
def main_callback(
    repo: Path = typer.Option(
        Path("."),
        "--repo",
        "-r",
        help="Path to the haunted repository. Defaults to the current directory.",
        exists=True,
        file_okay=False,
    ),
) -> None:
    global _repo_path
    _repo_path = repo


def _scanner() -> RepoScanner:
    try:
        return RepoScanner(_repo_path)
    except RepoError as exc:
        err_console.print(f"[blood]The spirits refuse to answer:[/] {exc}")
        raise typer.Exit(code=1) from exc


def _panel(title: str, body: str, border: str = "ghost") -> Panel:
    return Panel(Text.from_markup(body), title=f"[spectre]{title}[/]", border_style=border, expand=False)


def _commit_header(commit: Commit) -> str:
    return (
        f"[spectre]{commit.short}[/] [grave]·[/] [candle]{commit.author}[/] [grave]·[/] "
        f"{commit.date.strftime('%d %b %Y %H:%M')} [grave]·[/] \"{commit.subject}\"\n"
        f"[grave]{commit.files_changed} file(s), +{commit.insertions}/-{commit.deletions}[/]"
    )


@app.command()
def haunt(
    last: int = typer.Option(3, "--last", "-n", min=1, help="How many recent graves to disturb."),
    commit: Optional[str] = typer.Option(None, "--commit", "-c", help="A specific commit (short or full sha)."),
) -> None:
    """Recent changes wake the dead. Let them comment on their own code."""
    console.print(BANNER, style="ghost")
    scanner = _scanner()
    commits = scanner.commits()
    if not commits:
        console.print("[marigold]This graveyard is empty. No graves, no ghosts. Yet.[/]")
        raise typer.Exit()
    engine, mode = get_engine()
    console.print(f"[grave]engine: {mode} · everything stays on this machine[/]\n")

    if commit:
        matches = [c for c in commits if c.sha.startswith(commit) or c.short == commit]
        if not matches:
            console.print(f"[blood]No grave bears the mark '{commit}'.[/]")
            raise typer.Exit(code=1)
        targets = matches
    else:
        targets = commits[:last]

    for c in targets:
        console.print(_panel(_commit_header(c), engine.haunt(c)))
        console.print()


@app.command()
def seance(
    target: Optional[str] = typer.Argument(None, help="A tracked file path or a commit sha. Defaults to the latest commit."),
    questions: int = typer.Option(3, "--questions", "-q", min=1, max=5, help="Questions to put to the spirit."),
) -> None:
    """A digital séance: summon the spirit of whoever wrote this, and interrogate it."""
    console.print(BANNER, style="ghost")
    scanner = _scanner()
    engine, mode = get_engine()
    console.print(f"[grave]engine: {mode} · the circle is closed · nothing leaves this machine[/]\n")

    commits = scanner.commits()
    if not commits:
        console.print("[marigold]No spirits to summon — the repository has no graves.[/]")
        raise typer.Exit()

    if target is None:
        chosen, blame_summary = commits[0], ""
    else:
        candidate_file = Path(_repo_path) / target
        is_file = candidate_file.exists() and not candidate_file.is_dir()
        match = None
        if not is_file:
            for c in commits:
                if c.sha.startswith(target) or c.short == target:
                    match = c
                    break
            if match is None:
                console.print(f"[blood]Nothing to summon at '{target}' — not a tracked file, not a commit.[/]")
                raise typer.Exit(code=1)
        if is_file:
            rel = target.replace("\\", "/")
            spirits = scanner.blame_spirits(rel)
            if not spirits:
                console.print(f"[blood]'{target}' is untracked. Its spirit has no body to haunt.[/]")
                raise typer.Exit(code=1)
            top_author, line_count = spirits[0]
            blame_summary = f"Top spirit: {top_author} holds {line_count} lines of '{rel}'."
            chosen = scanner.last_commit_touching(rel) or commits[0]
        else:
            chosen = match
            blame_summary = ""

    console.print(f"[candle]🕯️ Candle lit. Summoning the spirit of [bold]{chosen.author}[/]…[/]\n")
    seance_result = engine.seance(chosen, blame_summary)
    body = f"[grave]summoned via commit {chosen.short}: \"{chosen.subject}\"[/]\n\n" + "\n".join(seance_result.lines[: questions * 2 + 2])
    console.print(_panel(f"SÉANCE — {seance_result.spirit}", body, border="candle"))
    console.print("\n[grave]The candle is out. The spirit returns to the blame.[/]")


@app.command()
def graveyard(
    output: Path = typer.Option(Path("OFRENDA.md"), "--output", "-o", help="Where to build the altar."),
    write: bool = typer.Option(True, "--write/--no-write", help="Write OFRENDA.md to disk."),
) -> None:
    """Día de los Muertos: excavate the dead code and build an ofrenda."""
    console.print(BANNER, style="ghost")
    scanner = _scanner()
    findings = scanner.all_dead_things()
    report = scanner.diagnose()
    console.print(f"[marigold]Exhumation complete: {len(findings)} soul(s) found in '{scanner.path.name}'.[/]\n")

    table = Table(title="The Exhumed", border_style="grave")
    table.add_column("Kind", style="candle")
    table.add_column("Where", style="spectre")
    table.add_column("Remains", overflow="fold")
    for thing in findings:
        icon = KIND_ICONS.get(thing.kind, "✦")
        table.add_row(f"{icon} {thing.kind}", thing.where, thing.label)
    if findings:
        console.print(table)
    else:
        console.print("[ghost]Nothing dead was found. Either you are very disciplined, or very recent.[/]")
    console.print()

    if write:
        md = build_ofrenda(scanner.path.name, findings, report)
        output.write_text(md, encoding="utf-8")
        console.print(f"[candle]The altar has been raised: [bold]{output}[/][/]")
    console.print(f"[grave]Haunt Index: {report.haunt_index}/100 — {report.grade}[/]")


@app.command()
def diagnose() -> None:
    """Measure the repository's Haunt Index. Bring sage."""
    console.print(BANNER, style="ghost")
    scanner = _scanner()
    report = scanner.diagnose()

    gauge_color = "bright_green" if report.haunt_index < 30 else "yellow" if report.haunt_index < 60 else "blood"
    console.print(Panel(
        f"[{gauge_color}][bold]{report.haunt_index}[/] / 100 — {report.grade}[/]",
        title=f"[spectre]HAUNT INDEX — {report.repo}[/]",
        border_style=gauge_color,
    ))
    table = Table(border_style="grave")
    table.add_column("Reading", style="candle")
    table.add_column("Value", justify="right", style="spectre")
    table.add_row("Total graves (commits)", str(report.total_commits))
    table.add_row("Distinct spirits (authors)", str(report.authors))
    table.add_row("Witching-hour commits (00–05)", str(report.nocturnal_commits))
    table.add_row("Cursed brief messages", str(report.lazy_messages))
    table.add_row("Colossal commits (500+ lines)", str(report.colossal_commits))
    table.add_row(f"{KIND_ICONS['todo']} TODO ghosts", str(report.todo_ghosts))
    table.add_row(f"{KIND_ICONS['commented_code']} Commented-out corpses", str(report.commented_corpses))
    table.add_row(f"{KIND_ICONS['deprecated']} Deprecated tombstones", str(report.deprecated_tombstones))
    table.add_row(f"{KIND_ICONS['zombie_branch']} Zombie branches", str(report.zombie_branches))
    console.print(table)
    for note in report.notes:
        console.print(f"  [ghost]✦ {note}[/]")


@app.command()
def epitaph(
    where: str = typer.Argument(..., help="A 'file:line' or branch name, as listed by graveyard."),
) -> None:
    """Ask for a single epitaph for a single dead thing."""
    scanner = _scanner()
    findings = scanner.all_dead_things()
    for thing in findings:
        if thing.where == where:
            console.print(f"[candle]🕯️ {epitaph_for(thing, scanner)}[/]")
            return
    console.print(f"[blood]No grave found at '{where}'. Run 'graveyard' to list the dead.[/]")
    raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """The version, spoken plainly for once."""
    console.print(f"git-spectre {__version__} — {datetime.now().strftime('%Y')}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()