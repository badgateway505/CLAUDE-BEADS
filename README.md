<div align="center">

# 🧵 Claude Beads v2.0

### Validate first. Build only what survives.

**Atomic task execution framework for AI-assisted development**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

[Philosophy](#-philosophy) · [How It Works](#-how-it-works) · [Get Started](#-get-started) · [Architecture](#-architecture) · [Commands](#-commands)

</div>

---

## 🧊 Philosophy

### Prove the idea before building the product.

Most AI projects fail the same way: you build the architecture, wire up the config, set up CI — then discover the core idea doesn't work. Beads inverts this.

**Phase 01 is always a proof-of-concept.** Minimal code. No infrastructure. Just enough to answer: *does the core function actually work?*

After Phase 01, you evaluate honestly: **Continue**, **Pivot**, or **Kill**. Only validated ideas get architecture. Only proven concepts get polish.

This isn't just project philosophy — it's enforced by the framework. Beads structures your work so the riskiest assumption gets tested first, cheaply, before you invest.

---

### The Core Idea

Beads treats AI development as a series of atomic, verifiable steps with physical enforcement at the runtime level.

- **Validation-First.** Phase 01 proves the concept. After it completes, a structured evaluation asks: was the core idea validated? Continue, pivot, or kill — before investing in architecture.

- **Physical Enforcement.** Shell hooks block tool calls before they execute. Claude can't touch protected files, skip verification, or break the workflow. It's not a suggestion; it's a hard lock.

- **Token Efficiency.** Each bead only sees the files it needs (~4K tokens instead of 80-120K). Phase freezing compresses completed work into summaries. Context stays flat.

- **The Ledger.** A persistent, deterministic source of truth. The FSM tracks every move. Stop today, come back in a week — `/beads:resume` puts you exactly where you left off.

---

## ⚡ How It Works

### The Validation Loop

```
1. /beads:plan-project       Evaluate the idea, create phase roadmap
2. /beads:plan-phase 01      Decompose proof-of-concept (1-3 beads, minimal)
3. /beads:run                Execute beads (/clear between each)
4. /beads:close-phase        Evaluate: continue, pivot, or kill?
5. /beads:plan-phase 02+     If validated — proceed with features
```

### Phase Ordering

```
Phase 01 → Prove the core function ("paperboard engine")
Phase 02 → User-facing features (things people interact with)
Phase N  → Infrastructure (error handling, config, auth)
Phase N+ → Polish and deployment (optimization, CI, docs)
```

Don't build foundations before validating the idea. Don't add error handling before the feature works. Don't optimize before the user is happy.

### The Bead Cycle

Each bead is an atomic work session — isolated context, clear deliverable, verified outcome.

```
Initialize → Challenge approach → Execute → Verify → Commit → Next
```

You run `/clear` then `/beads:run`. The FSM handles the rest.

---

## ◆ Get Started

### Installation

```bash
pipx install git+https://github.com/badgateway505/CLAUDE-BEADS.git
```

No `pipx`? Install with `brew install pipx` or `pip install pipx`.

### Setup

```bash
cd your-project/
beads init
```

This generates three layers:
- `.beads/` — Engine (FSM, Ledger, Templates)
- `.claude/` — Perimeter (Skills and Enforcement Hooks)
- `.planning/` — Roadmap (Phase and Bead definitions)

### First Run

```
/beads:plan-project          # Evaluate idea, define core function, create roadmap
/beads:plan-phase 01         # Decompose Phase 01 into 1-3 proof-of-concept beads
/clear
/beads:run                   # Execute first bead
```

After Phase 01, close and evaluate:

```
/beads:close-phase           # Creates summary, triggers evaluation gate
                             # → Continue (proceed to Phase 02)
                             # → Pivot (adjust idea, re-plan)
                             # → Kill (shelve project)
```

---

## 🔧 Architecture

### The Ledger · `ledger.json`

Single source of truth for the project lifecycle. The FSM synchronizes state between sessions — completed beads, active phase, roadmap progress. `/beads:resume` reads the ledger to restore full context after any break.

### The FSM · `fsm.py`

Deterministic workflow controller with rigid state transitions:

```
INIT → EXECUTE → VERIFY → COMPLETE
                   ↓
                RECOVER → EXECUTE (retry)
                   ↓
                 FAILED (circuit breaker after 3 attempts)
```

**Guardrails:**
- **Phase Guard** — blocks bead init if previous phase isn't closed
- **IRON LOCK** — enforces model assignment (opus bead can't run on sonnet)
- **Verified Commit** — no completion without passing verification + git commit
- **Circuit Breaker** — 3 retries max, then mandatory rollback

### Physical Enforcement · Hooks

Shell hooks that validate tool calls before execution. Not prompts — infrastructure.

| Hook | Target | Function |
|------|--------|----------|
| `protect-files.sh` | Edit, Write | Immutability for ledger, FSM, protocol files |
| `guard-bash.sh` | Bash | Blocks shell tampering on protected paths |
| `workflow-guard.sh` | Edit, Write | Blocks source edits unless FSM is in EXECUTE state |
| `error-lock.sh` | All tools | Hard-locks everything after 2 consecutive errors |

### Token Economy

Context isolation keeps token usage flat:

- **Scoped reads** — only files defined in bead metadata
- **Phase freezing** — closed phases compressed to `XX-SUMMARY.md`
- **Context reset** — `/clear` between beads flushes the window
- ~4K tokens per bead vs 80-120K+ for whole-codebase approaches

### Model Routing

| Task | Model | Rationale |
|------|-------|-----------|
| Architecture, planning | Opus | Superior long-horizon reasoning |
| Implementation | Sonnet | Best code quality + speed balance |
| Boilerplate, docs | Haiku | Fast and cheap |

---

## 📋 Commands

### Terminal (CLI)

| Command | Function |
|---------|----------|
| `beads init` | Scaffold project structure, install skills and hooks |
| `beads status` | Display active state and roadmap progress |
| `beads help` | Show CLI manual |

### Claude Code (Skills)

| Command | Function |
|---------|----------|
| `/beads:plan-project` | Evaluate idea, create validation-first phase roadmap |
| `/beads:plan-phase` | Decompose phase into atomic beads |
| `/beads:run` | Execute active bead (verify + commit) |
| `/beads:close-phase` | Close phase (Phase 01: evaluation gate) |
| `/beads:research` | Research feasibility or technical approach |
| `/beads:resume` | Restore project context and recommend next action |
| `/beads:help` | Show available commands and workflow |

---

## 📂 Project Structure

```
my-project/
├── .beads/
│   ├── bin/                 # FSM engine
│   ├── templates/           # Bead and research templates
│   ├── PROTOCOL.md          # Full execution specification
│   └── ledger.json          # Project source of truth
│
├── .claude/
│   ├── hooks/               # Physical enforcement (shell)
│   ├── skills/              # Claude-native skill definitions
│   └── settings.json        # Hook registration
│
├── .planning/
│   ├── PROJECT.md           # Vision, core function, tech stack
│   ├── DECISIONS.md         # Architectural decisions log
│   └── phases/              # Phase overviews and bead specs
│
├── CLAUDE.md                # Protected project context
└── .gitignore
```

---

## ❓ FAQ

**How is this different from other AI workflow frameworks?**
Most frameworks rely on prompts to guide the AI. Beads uses physical shell hooks that block tool calls before they execute. Claude can't bypass the workflow, edit protected files, or skip verification — the infrastructure prevents it, not the instructions.

**What's "validation-first"?**
Phase 01 is always a minimal proof-of-concept. After it completes, you evaluate: continue, pivot, or kill. No architecture investment until the core idea is proven. This saves days of wasted work on ideas that don't survive contact with reality.

**Does this work with other AI assistants?**
No. Beads is built for Claude Code's PreToolUse hook system. The physical enforcement layer depends on Claude Code's architecture.

**How much does it save on tokens?**
Typically 60-70%. Each bead reads only its scoped files (~4K tokens) instead of the entire codebase (80-120K+). Phase freezing prevents re-reading completed work.

**Can Claude bypass the guards?**
Direct tool calls (Edit, Write, Bash) are fully enforced. The one limitation is Claude Code's Task subagent (background agents), which is a Claude Code architectural constraint.

**Is this only for big projects?**
Beads shines on multi-phase projects, but even a single-phase project benefits from verified commits, context isolation, and the evaluation gate.

---

## Development

### Contributing

- Fork the repository
- Create a feature branch (`git checkout -b feat/id`)
- Commit following feat/fix convention
- Open a Pull Request

All code must pass ruff and include relevant tests.

### License

MIT License. See LICENSE for details.

---

<div align="center">

Built for developers who validate before they invest.

[Issues](https://github.com/badgateway505/CLAUDE-BEADS/issues) · [Discussions](https://github.com/badgateway505/CLAUDE-BEADS/discussions)

</div>
