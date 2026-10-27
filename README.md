<div align="center">

```
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
 ⣿   ⢠⣤⣶⣶⣦⡀                                              ⣿
 ⣿   ⢸⣿⠋⠙⠛⠛⢿⣷      g i t - s p e c t r e                  ⣿
 ⣿    ⠙⠶⠶⠶⠶⠶⠛⠋   the haunted git history & digital séance  ⣿
 ⣿                                                             ⣿
 ⣿        ·˚🕯️ git-spectre · the dead read your diffs · 🕯️·˚    ⣿
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

**Summon the ghosts of your git history — with a local, open-weight AI.**

👻 `haunt` · 🔮 `seance` · 🪦 `graveyard` · 📟 `diagnose`

*100% offline. 100% private. Zero tokens leave your machine.*

[![License: MIT](https://img.shields.io/badge/License-MIT-cb6ce6.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-8a2be2.svg)](https://www.python.org/)
[![Built with Gemma](https://img.shields.io/badge/AI-Gemma%20%2F%20Standalone-ff7518.svg)](https://ai.google.dev/gemma)
[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2026-7c3aed.svg)](https://hacktoberfest.com/)

</div>

---

**git-spectre** is a CLI that treats every repository as what it truly is: a
graveyard. Commits are graves. Branches are crypts. TODO comments are voices
still whispering under the floorboards. git-spectre exhumes them all — and
summons the *ghosts of your past developers* to comment on their own code,
using a **local open-weight model (Google Gemma via Ollama)** or a built-in
**Standalone Haunted Engine** that needs nothing but Python.

> **Why local AI?** Your commit history *is* your codebase's diary: author
> names, emails, 3 AM habits, half-finished secrets. Sending it to a cloud
> LLM to get a witty review is a data-leak dressed up as a feature.
> git-spectre runs its intelligence on-device, so the séance never leaves the
> room.

---

## 👻 The Four Rites

### `git-spectre haunt` — the ghosts comment on their own code

Analyzes recent commits (or a specific one) and lets the departed developer's
spirit chime in with chills and criticism:

```
$ git-spectre haunt --last 2

 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
 ⣿        ·˚🕯️ git-spectre · the dead read your diffs · 🕯️·˚    ⣿
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

engine: standalone · everything stays on this machine

╭─ 9f2c1ab · Bob Cursed · 31 Oct 2024 03:14 · "wip"
│           2 file(s), +123/-3
│
│ The 3 AM Poltergeist 🕒
│    ✦ Bob Cursed pushed 'wip' at 03:14 AM-ish — a time when even the servers
│      pretend to sleep. Nothing written at that hour has ever been wise.
│    ✦ 'wip' — the entire message. Bob Cursed looked upon 123 changed lines
│      and chose brevity over honesty. The grave marker says nothing, and so
│      it says everything.
│    ✦ This grave dates to 31 Oct 2024. Whatever problem it solved, the
│      problem has since been reborn twice.
╰──────────────────────────────────────────────────────────────
```

Every ghost has a persona, chosen from the *shape* of the crime:

| Persona | Summons when |
|---|---|
| 🕒 **The 3 AM Poltergeist** | commits made between 00:00 and 05:00 |
| 👹 **The Colossus** | single commits of 500+ changed lines |
| 🩹 **The Bearer of 'WIP'** | messages like `wip`, `fix`, `tmp`, `asdf` |
| 📅 **The Weekend Wraith** | Friday-and-later commits |
| 👻 **The Forgotten Contributor** | everything else |

### `git-spectre seance <file|commit>` — the digital séance

Light a candle, close the circle, and **interrogate the spirit of whoever
wrote a file or commit**. On a file, git-spectre reads `git blame`, finds the
dominant spirit, and puts the questions to *them*:

```
$ git-spectre seance cursed.py

🕯️ Candle lit. Summoning the spirit of Bob Cursed…

╭─ SÉANCE — Bob Cursed (departed 31 Oct 2024) on 'wip'
│   summoned via commit 9f2c1ab: "wip"
│
│   Q: Why did you write this?
│   A: It was 03:14. I thought I was brilliant. I was merely awake.
│   Q: What were you thinking at the time?
│   A: The build was broken. The coffee was gone. The code wrote itself
│      and I signed it.
│   Q: Do you repent?
│   A: I repent of nothing at 03:14. Repentance requires consciousness.
│   Q: Who else touched what you touched?
│   A: Top spirit: Bob Cursed holds 6 lines of 'cursed.py'.
│      Their fingerprints are everywhere. So are mine.
│   ✧ Go in peace. Do not refactor my work on a Friday.
╰──────────────────────────────────────────────────────────────

The candle is out. The spirit returns to the blame.
```

### `git-spectre graveyard` — Día de los Muertos for your dead code

Excavates the four kinds of remains and raises a **markdown ofrenda** —
`OFRENDA.md` — complete with ASCII tombstones, marigolds, and rites of
resurrection:

```
$ git-spectre graveyard

Exhumation complete: 5 soul(s) found in 'haunted'.

┌───────────────────────────── The Exhumed ──────────────────────────────┐
│ Kind                          │ Where          │ Remains                │
├───────────────────────────────┼────────────────┼────────────────────────┤
│ 🕯️ todo                       │ cursed.py:1    │ # TODO: fix this befo… │
│ 🥀 commented_code             │ cursed.py:2    │ # def old_summoning(): │
│ 🪦 deprecated                 │ cursed.py:4    │ @deprecated            │
│ 🧟 zombie_branch              │ doomed         │ doomed                 │
└────────────────────────────────────────────────────────────────────────┘

The altar has been raised: OFRENDA.md
Haunt Index: 62/100 — Séance Site 🔮 — spirits answer on every git pull
```

Sample of the generated altar:

```markdown
# 🕯️ OFRENDA.md — Altar for the Departed Code

> Built by **git-spectre** on 01 Nov 2025 at 09:00 for `haunted`.
> In this repository we honor the dead code: may it rest, or may it rise.

## 🧡 The Ofrenda
On this altar we place, in the tradition of Día de los Muertos:
- 🌼 **Marigolds** (*cempasúchil*), so the dead code can find its way home
- 🕯️ **Candles**, one for every TODO that was never a ticket
- 🧂 **Salt**, for preservation — see also: every commented-out function

        ╔═══════════════════════╗
        ║         R. I. P.      ║
        ║                       ║
        ║      TODO: fix th     ║
        ║                       ║
        ║   cursed.py:1         ║
        ╚═══════════════════════╝

> *"TODO: fix this before the demo"*

## ✝️ Rites of Resurrection
1. **TODO ghosts** — turn each candle into a ticket, or blow it out.
2. **Commented-out corpses** — version control already remembers them.
   Delete with dignity.
4. **Zombie branches** — merge, or close the crypt. A branch unmerged for
   90+ days is not resting, it is rotting.
```

### `git-spectre diagnose` — the Haunt Index

A single number for how haunted your repository is:

```
$ git-spectre diagnose

╭─ HAUNT INDEX — haunted ────────────────────────────────────────╮
│ 62 / 100 — Séance Site 🔮 — spirits answer on every git pull   │
╰────────────────────────────────────────────────────────────────╯

┌ Reading                            │ Value ┐
│ Total graves (commits)             │     2 │
│ Distinct spirits (authors)         │     2 │
│ Witching-hour commits (00–05)      │     1 │
│ Cursed brief messages              │     1 │
│ Colossal commits (500+ lines)      │     0 │
│ 🕯️ TODO ghosts                     │     1 │
│ 🥀 Commented-out corpses           │     1 │
│ 🪦 Deprecated tombstones           │     1 │
│ 🧟 Zombie branches                 │     1 │
└────────────────────────────────────────────┘
  ✦ 1 commit(s) made between midnight and dawn.
  ✦ 1 zombie branch(es) never merged, never mourned.
```

Grades: 🕯️ *Pristinely Poltergeist-Free* → 👻 *Lightly Haunted* → 😱 *Actively
Haunted* → 🔮 *Séance Site* → 💀 *Fully Possessed*.

---

## 📦 Installation

```bash
pip install git-spectre

# or from a clone of this repository:
pip install .
```

Python 3.9+ · no GPU required · no accounts, no API keys, no telemetry.

## 🚀 Usage

```bash
git-spectre haunt                     # let the ghosts of the last 3 commits speak
git-spectre haunt --last 5            # disturb more graves
git-spectre haunt --commit 9f2c1ab    # haunt one specific commit
git-spectre seance src/engine.py      # interrogate the dominant spirit of a file
git-spectre seance 9f2c1ab            # ...or of a single commit
git-spectre graveyard                 # raise the OFRENDA.md altar
git-spectre diagnose                  # measure the Haunt Index
git-spectre epitaph cursed.py:1       # one epitaph for one dead thing
```

Run it inside any repository, or point it elsewhere with `--repo /path/to/repo`.

## 🤖 AI: Gemma when you have it, hauntings when you don't

git-spectre is **dual-mode**, and both modes are local:

| Mode | Engine | How it works |
|---|---|---|
| **Gemma** 🧠 | `OllamaGemmaEngine` | If Ollama is installed and a Gemma-family open-weight model is pulled, git-spectre narrates hauntings and séances with it — Gemma reads the commit metadata and improvises in character. |
| **Standalone** 🔮 | `StandaloneHauntedEngine` | With no model present (or if Ollama ever fails), a deterministic, hash-seeded template engine takes over. It reads the *shape* of history — witching hours, lazy messages, colossi — and improvises a reproducible haunting. |

Detection is automatic (`git-spectre` prints the active engine), and the
fallback is seamless: **the CLI always works, fully offline**.

To summon with Gemma:

```bash
ollama pull gemma2:2b      # any Gemma-family model works
git-spectre haunt
```

Why this matters, in one paragraph: a commit log is a privacy asset. It
contains real names, emails, working habits, and the anatomy of proprietary
code. Pasting it into a hosted chat API to get "AI flavor" teaches your
entire team that leaking is the price of a nice demo. Open-weight models like
Gemma break that trade: you get the ghost, the wit, and the séance — and the
blame stays on your disk, where the ghosts belong.

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      cli.py (typer + rich)                 │
│        haunt · seance · graveyard · diagnose · epitaph     │
└───────────────┬────────────────────────────┬───────────────┘
                │                            │
┌───────────────▼──────────────┐  ┌──────────▼─────────────────────┐
│      git_scanner.py          │  │       ghost_engine.py          │
│  (read-only exhumation)      │  │  dual-mode voices of the dead  │
│  · commit log + numstat      │  │  ┌──────────────────────────┐  │
│  · line-porcelain blame      │  │  │ OllamaGemmaEngine        │  │
│  · branch merge-base check   │  │  │  (Gemma via ollama run)  │  │
│  · dead-code excavator:      │  │  ├──────────────────────────┤  │
│    TODO / FIXME / HACK / XXX │  │  │ StandaloneHauntedEngine  │  │
│    commented-out code        │  │  │  (hash-seeded personas,  │  │
│    @deprecated / tombstones  │  │  │   zero dependencies)     │  │
│    zombie branches (90d)     │  │  └──────────────────────────┘  │
└───────────────┬──────────────┘  └──────────┬─────────────────────┘
                │                            │
┌───────────────▼────────────────────────────▼───────────────┐
│                     graveyard.py                           │
│   Día de los Muertos renderer → OFRENDA.md + terminal wake │
└────────────────────────────────────────────────────────────┘
```

- **`git_scanner.py`** — read-only exhumation via the `git` binary: commits,
  numstat, porcelain blame, author stats, merge-base zombie detection, and a
  dead-code excavator (TODO ghosts, commented-out corpses, deprecated
  tombstones, zombie branches).
- **`ghost_engine.py`** — the voices. Dual-mode: Gemma through Ollama when
  available; otherwise the StandaloneHauntedEngine, whose personas are chosen
  from measurable crimes (hour, size, message laziness) and whose output is
  seeded by the commit sha, so the same ghost says the same thing every time.
- **`graveyard.py`** — turns excavated remains into an ofrenda: ASCII
  tombstones, a count of the dead, and rites of resurrection, in
  `OFRENDA.md`.
- **`cli.py`** — the séance room: a typer app wrapped in rich panels, gauges
  and tables.

git-spectre is strictly **read-only** against your repository: it never
commits, never rewrites, never touches a ref. The only file it writes is the
altar.

## ✅ Tests

```bash
pip install -e ".[test]"
pytest            # 38 tests, covering scanner, engine, altar, and CLI end-to-end
```

The test suite builds real temporary git repositories (a 3 AM `wip` commit, a
cursed file, a zombie branch from 2020) and runs every command against them.

## 🎃 How it connects to the theme

*Ghost in the Machine* asks what it means for the past to keep living in our
tools. Every repository already *is* a machine full of ghosts: the person who
wrote a function at 3 AM in 2021 is still in every line they touched, still
answering for it every time someone runs `git blame`. Halloween gives them a
voice; Día de los Muertos gives them an altar. git-spectre is both: a séance
for the code you inherited, and an ofrenda for the code you keep meaning to
delete. The ghost in the machine was never a metaphor — it was the blame.

## 📄 License

MIT — see [LICENSE](LICENSE). The ghosts, however, are eternal.

---

<div align="center">

🕯️ *light a candle before you run* `git blame` *next time* 🕯️

</div>