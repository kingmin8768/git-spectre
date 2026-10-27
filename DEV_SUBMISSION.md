# Ghost in the Machine: git-spectre — Local AI Digital Séances for Your Haunted Git History

> **DEV Hacktoberfest Open-Source AI Challenge — Week 4: "Ghost in the Machine"** 🎃👻
> A submission for the Overall category and **Best Use of Gemma**.

**Repo:** https://github.com/kingmin8768/git-spectre · **License:** MIT · **Language:** Python · **AI:** Google Gemma (open-weight, via Ollama) with a zero-dependency Standalone Haunted Engine fallback

---

## 👻 The Motivation: Your Commit History Is a Diary. Why Are You Pasting It Into a Chatbot?

Before we get to the ghosts, let's talk about the *actual* monster under the bed.

Every developer's git history is an intimate document. It contains your real
name, your email, the hour you actually go to bed, the functions you were
ashamed of, the `wip` confessions you never cleaned up, and the anatomy of
proprietary code your company would rather not see pasted into a hosted LLM's
training pipeline "anonymized or otherwise."

And what does the AI-hype era tell us to do with that history? Paste it into a
cloud chatbot for "AI-powered commit insights." That's not a feature; that's a
data-leak dressed up in a Halloween costume.

**git-spectre takes the opposite deal.** It summons the ghosts of your
repository using a **local, open-weight model — Google's Gemma, served
on-device through Ollama** — and, when no model is installed, a built-in
**Standalone Haunted Engine** that needs nothing but Python. The consequence
is the whole point:

- 🔒 **Codebase privacy**: commit messages, authors, diffs, and blame never
  leave the machine. Not once, not anonymized, not "just the metadata."
- 🌐 **Zero-leakage by architecture**: there is no API call to make, no
  endpoint to misconfigure, no vendor to trust. Privacy here is not a policy —
  it is physics.
- ✈️ **Offline dev**: airplane, bunker, cabin in the woods — the séance works
  anywhere git works.
- 💸 **No keys, no costs, no rate limits**: no API token in your CI, no meter
  running on every haunting.

Open-weight models like Gemma are what make this trade possible: you get the
ghost, the wit, and the personality — and the blame stays on your disk, where
the ghosts belong.

## 🪦 What I Built

**git-spectre** — *"the haunted git history & digital séance CLI"* — treats
every repository as what it truly is: a graveyard. Commits are graves,
branches are crypts, TODO comments are voices still whispering under the
floorboards. Four rites let you interact with the dead:

### 1. `git-spectre haunt` — the ghosts review their own code

It reads recent commits (or one you point at), profiles the *crime* behind
each one, and summons the departed developer's spirit to comment on it. Ghost
personas are chosen from measurable sins:

| Persona | Summons when |
|---|---|
| 🕒 **The 3 AM Poltergeist** | commits made between 00:00 and 05:00 |
| 👹 **The Colossus** | a single commit of 500+ changed lines |
| 🩹 **The Bearer of 'WIP'** | messages like `wip`, `fix`, `tmp`, `asdf` |
| 📅 **The Weekend Wraith** | Friday-and-later commits |
| 👻 **The Forgotten Contributor** | everything else |

Real output from the demo repository:

```
╭───── 834f3bf · Bob Cursed · 31 Oct 2024 03:14 · "wip" 1 file(s), +6/-0 ──────╮
│ The 3 AM Poltergeist 🕒                                                      │
│    ✦ This was written at 03:14 AM-ish. The dead keep those hours. So,        │
│ apparently, did Bob Cursed.                                                  │
│    ✦ The commit message reads 'wip'. Archaeologists of the future will weep. │
│    ✦ This grave dates to 31 Oct 2024. Whatever problem it solved, the        │
│ problem has since been reborn twice.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 2. `git-spectre seance <file|commit>` — the digital séance

Light a candle, close the circle, and **interrogate the spirit of whoever
wrote a file**. On a file, git-spectre runs `git blame`, identifies the
dominant spirit, and puts the questions to *them* — with the blame summary
entered into evidence. This is the feature that hits hardest in code review
culture: before you refactor someone's function, hear them explain
themselves.

```
🕯️ Candle lit. Summoning the spirit of Bob Cursed…

╭───────────────── SÉANCE — Bob Cursed (departed 31 Oct 2024) ─────────────────╮
│ summoned via commit 834f3bf: "wip"                                           │
│                                                                              │
│   Q: Why did you write this?                                                 │
│   A: It was 03:14. I thought I was brilliant. I was merely awake.            │
│   Q: What were you thinking at the time?                                     │
│   A: The build was broken. The coffee was gone. The code wrote itself and I  │
│ signed it.                                                                   │
│   Q: Do you repent?                                                          │
│   A: I repent of nothing at 03:14. Repentance requires consciousness.        │
│   Q: Who else touched what you touched?                                      │
│   A: Top spirit: Bob Cursed holds 6 lines of 'cursed.py'. Their fingerprints │
│ are everywhere. So are mine.                                                 │
╰──────────────────────────────────────────────────────────────────────────────╯

The candle is out. The spirit returns to the blame.
```

### 3. `git-spectre graveyard` — Día de los Muertos for your dead code

For the Day of the Dead side of the challenge window, `graveyard` excavates
four kinds of remains — **TODO ghosts** 🕯️, **commented-out corpses** 🥀,
**deprecated tombstones** 🪦, and **zombie branches** 🧟 (unmerged, 90+ days
cold, found via `merge-base --is-ancestor`) — and raises an actual **ofrenda**:
a markdown altar, `OFRENDA.md`, with ASCII tombstones, marigolds, pan de
código, and *Rites of Resurrection* that tell you how each kind of dead can
either cross over or be laid to rest.

```
Exhumation complete: 6 soul(s) found in 'demo-spectre'.

┃ 🕯️ todo           │ cursed.py:1 │ # TODO: fix this before the demo
┃ 🥀 commented_code │ cursed.py:2 │ # def old_summoning():
┃ 🪦 deprecated     │ cursed.py:4 │ @deprecated
┃ 🧟 zombie_branch  │ doomed      │ doomed

The altar has been raised: OFRENDA.md
Haunt Index: 34/100 — Actively Haunted 😱 — cold spots in the blame
```

And in the generated `OFRENDA.md`:

```
        ╔═══════════════════════╗
        ║         R. I. P.      ║
        ║                       ║
        ║      TODO: fix th     ║
        ║                       ║
        ║   cursed.py:1         ║
        ╚═══════════════════════╝

> *"TODO: fix this before the demo"*
```

### 4. `git-spectre diagnose` — the Haunt Index

One number for how haunted your repository is, from 🕯️ *Pristinely
Poltergeist-Free* to 💀 *Fully Possessed*. It weighs witching-hour commits,
cursed brief messages, colossal commits, all four kinds of dead code, and
sole-author graveyards (a repository haunted by exactly one restless soul is
its own kind of sad).

## 🧠 Tech Stack & Architecture

**Python 3.9+ · Typer · Rich · the `git` binary · Google Gemma (open-weight)
via Ollama · a hash-seedable Standalone engine · pytest**

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
│  · dead-code excavator       │  │  ├──────────────────────────┤  │
│    TODO / FIXME / HACK / XXX │  │  │ StandaloneHauntedEngine  │  │
│    commented-out code        │  │  │  (hash-seeded personas,  │  │
│    @deprecated tombstones    │  │  │   zero dependencies)     │  │
│    zombie branches (90d)     │  │  └──────────────────────────┘  │
└───────────────┬──────────────┘  └──────────┬─────────────────────┘
                │                            │
┌───────────────▼────────────────────────────▼───────────────┐
│                     graveyard.py                           │
│   Día de los Muertos renderer → OFRENDA.md + terminal wake │
└────────────────────────────────────────────────────────────┘
```

**The dual-mode engine is the technical heart.** `ghost_engine.py` exposes one
interface with two implementations:

- **`OllamaGemmaEngine`** — detects any pulled Gemma-family model with
  `ollama list` (no network), builds a character prompt from commit metadata
  (author, hour, size, message) and lets Gemma improvise the ghost. When it
  narrates, the panel is stamped `via gemma2:2b` so you always know whose
  voice you're hearing.
- **`StandaloneHauntedEngine`** — a deterministic, hash-seeded template
  engine. Each persona is selected from measurable properties of the commit
  (hour band, size band, message laziness, weekday), and the flavor lines are
  chosen with a RNG seeded by the commit sha — so the same ghost always says
  the same thing, which makes output reproducible for docs, demos, and CI.

The fallback is seamless and automatic: if Ollama exists but has no Gemma, or
fails mid-séance, the standalone engine finishes the haunting and nobody
notices the curtain move.

**The scanner is strictly read-only.** git-spectre never commits, never
rewrites history, never touches a ref. The only file it creates is the altar.

**Testing:** 38 pytest tests build *real* temporary git repositories — a 3 AM
`wip` commit, a cursed file, a zombie branch abandoned in 2020 — and run
every command end-to-end against them, scanner to altar. All 38 pass.

## 🎬 Demo

```bash
pip install git-spectre    # or: pip install . from a clone
ollama pull gemma2:2b      # optional — the standalone engine works without it

cd your-most-haunted-repo

git-spectre haunt          # the dead review their own diffs
git-spectre seance src/    # interrogate the spirit of a file's author
git-spectre graveyard      # raise the OFRENDA.md altar for Día de los Muertos
git-spectre diagnose       # how haunted is this repository, really?
```

Full captured terminal sessions, including a complete `OFRENDA.md` altar, are
in the repository under [`demo/`](https://github.com/kingmin8768/git-spectre/tree/main/demo).
The README carries an extended, copy-pasteable transcript of every rite.

## 🎃 How It Connects to the Theme

*Ghost in the Machine* asks what it means for the past to keep living inside
our tools. Here's the thing: it already does.

The person who wrote a function at 3 AM in 2021 is still in every line they
touched. They answer for it every single time someone runs `git blame`. Their
habits, their shortcuts, their one terrible Friday — all of it persists in the
machine, silent, until summoned.

Halloween gives those ghosts a **voice**: `haunt` and `seance` let the
departed explain, deflect, and complain about your refactoring plans. Día de
los Muertos gives them an **altar**: `graveyard` treats dead code not as
garbage to delete in shame but as *familiares* worth honoring before you let
them cross over — with marigolds, candles, and rites of resurrection instead
of `rm -rf`.

And the AI twist that makes it all work: the ghost in the machine is running
*in* the machine. A local Gemma model channels your repository's actual dead
without a single byte of them leaving the séance room. The ghost was never a
metaphor. It was the blame.

## 📄 Repository & License

- **GitHub:** https://github.com/kingmin8768/git-spectre
- **License:** MIT

---

> 🕯️ *Light a candle before you run `git blame` next time.* 🕯️
