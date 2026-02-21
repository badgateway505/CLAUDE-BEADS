<div align="center">

# Beads

Test ideas quickly. Build only what survived.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

[Philosophy](#-philosophy) · [The Authority](#-the-authority) · [The Protocol](#-the-protocol) · [Get Started](#-get-started) · [Infrastructure](#-infrastructure) · [Commands](#-commands)

</div>

---

Most developers spend hours "prompting" Claude to follow rules, hoping it won't drift or over-engineer. Hope is not a strategy. Claude is a probabilistic engine; if there is a way to fail the architecture or skip a step, it will find it.

Beads stops the yapping and starts the shipping.

---

## 🧊 Philosophy

### Kill your darlings early.

Most AI projects fail because you spend three days building architecture for an idea that doesn't actually work. Phase 01 is a firing squad for your bad ideas.

**Phase 01 is always a proof-of-concept.** Minimal code. No infrastructure. No "proper" way. If the core function doesn't work, we kill the project and save the tokens. Architecture is for ideas that survive.

---

## 🛠 The Authority

Prompting "please follow the workflow" is pathetic. Rules aren't suggestions. Beads replaces "please" with physical enforcement.

* **Hard Hooks.** I used Claude Code `PreToolUse` hooks to build a perimeter. If Claude tries to touch a protected file or bypass the protocol, the system returns a hard `Permission Denied`. The AI doesn't have a choice.
* **Validation Supremacy.** We move fast, build the core logic, and see it work. Don't build foundations before validating the idea. Don't add error handling before the feature works. Don't optimize before the user is happy.
* **Token Isolation.** Drowning Claude in your entire codebase is a rookie mistake. Beads isolates context at the "bead" level. You get flat 4K token costs because the AI only sees what I allow it to see.
* **The Ledger.** A persistent, deterministic source of truth. The FSM tracks every move. Stop today, come back in a week — `/beads:resume` puts you exactly where you left off. No memory drift.

---

## ⚡ The Protocol

My workflow is a closed loop. No drift, no excuses.

**01. The Plan.** `/beads:plan-project`. Evaluate the idea. If it's trash, stop here.
**02. The Proof.** `/beads:plan-phase 01`. Build the "paperboard engine." Minimal beads, maximum risk.
**03. The Execute.** `/beads:run`. Atomically build, verify, and commit.
**04. The Gate.** `/beads:close-phase`. The moment of truth: **Continue, Pivot, or Kill.**
**05. The Scale.** If (and only if) validated, move to features and infrastructure.

---

## ◆ Get Started

### Installation

If you have `pipx`, use it. If not, get it.

```bash
pipx install git+https://github.com/badgateway505/CLAUDE-BEADS.git
beads init
```

### The Cycle

Plan the move. Clear the noise. Run the task.

```text
/beads:plan-project
/beads:plan-phase 01
/clear
/beads:run
```

---

## 🔧 Infrastructure

### The Ledger · `ledger.json`

The project's memory. It's the only thing Claude needs to read to know exactly where we are.

### The FSM · `fsm.py`

A deterministic state machine. No "vibes," just transitions:
`INIT → EXECUTE → VERIFY → COMPLETE`.

* **IRON LOCK:** Opus tasks don't run on Sonnet. I don't let cheap models handle complex logic.
* **Verified Commit:** No `DONE` status without a passing test and a git commit.
* **Circuit Breaker:** 3 failures and the bead is dead. Roll back and rethink.

### The Guard · Physical Hooks

Infrastructure-level enforcement. Not prompt-level requests.

| Hook | Function |
| --- | --- |
| `protect-files.sh` | Immutability for the brain (Ledger, FSM, Protocol). |
| `guard-bash.sh` | Stops Claude from using `sed` or `rm` to bypass my rules. |
| `workflow-guard.sh` | No editing source code unless a bead is active. |
| `error-lock.sh` | Hard-locks the session after 2 consecutive failures. |

---

## 📋 Commands

### Terminal

* `beads init` — Scaffold the cage.
* `beads status` — Show me the progress.

### Claude Code

* `/beads:plan-project` — Map the milestones.
* `/beads:run` — Execute. Verify. Commit.
* `/beads:close-phase` — The evaluation gate.
* `/beads:resume` — Restore context. Stop yapping.

---

## 📂 Hierarchy

```text
my-project/
├── .beads/
│   ├── bin/                 ● The FSM Engine
│   └── ledger.json          ● The Source of Truth
├── .claude/
│   ├── hooks/               ● The Cage (Physical Enforcement)
│   └── skills/              ● Claude-native skill definitions
├── .planning/
│   ├── PROJECT.md           ● The Vision
│   └── phases/              ● The Specs
└── CLAUDE.md                ● Protected context
```

---

## ❓ Reality Check

**"How is this different?"**
Most frameworks ask for permission. Beads takes it. It uses shell hooks to block tool calls. Claude *physically cannot* bypass the workflow.

**"Why 'validation-first'?"**
Because building an infrastructure for a failed idea is a waste of my time and your money. Prove the core function works in Phase 01 or kill the repo.

**"Token savings?"**
60-70%. We keep the context flat. 4K tokens per bead. Every time.

---

I built this for vibe-coders who actually want to finish their projects. If you want to spend your life writing markdown tables and asking Claude for permission, use something else.

[Issues](https://github.com/badgateway505/CLAUDE-BEADS/issues) · [MIT License](https://opensource.org/licenses/MIT)
