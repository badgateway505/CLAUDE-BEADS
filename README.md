<div align="center">

# 🧵 Claude Beads v1.1

### Build real projects with Claude — without losing context, burning tokens, or hoping the AI follows your rules.

**Physical enforcement framework for atomic AI-assisted development**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Version: 1.1.0](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/badgateway505/CLAUDE-BEADS/releases/tag/v1.1.0)

[Why Beads?](#-beads) · [TL;DR](#️-tldr-the-sequence) · [Get Started](#-get-started) · [Architecture](#03-technical-architecture) · [Interface](#05-interface)

---

<!-- Replace with your terminal screenshot showing beads commands -->
<img src="docs/terminal-preview.png" alt="Claude Beads terminal output" width="700">

*`beads init` → `/beads:plan` → `/beads:run` — that's the whole workflow*

</div>

---


## 🧊 Beads

### Deterministic engineering for Claude.

Claude is an incredible collaborator, until it isn't. It forgets the plan, edits the wrong files, and burns your token budget on context it already saw an hour ago.

Existing frameworks try to fix this with more instructions. They ask Claude to be disciplined. We think that’s the wrong approach. You don't ask a machine to follow rules; you build the rules into the machine.

---

### The Core Idea

Beads is a framework that treats AI development as a series of atomic, verifiable steps. It moves the authority from the prompt to the runtime.

- **Physical Enforcement.** We don't use prompts to set boundaries. We use shell hooks. If Claude tries to touch a protected file or skip a step, the system blocks the tool call before it even starts. It’s not a suggestion; it’s a hard lock.

- **Token Efficiency by Design.** Most frameworks drown Claude in the entire codebase. Beads isolates context. Each "bead" (task) only sees the files it needs. You get faster responses and save up to 70% on tokens.

- **The Ledger.** A persistent, deterministic source of truth. The Finite State Machine (FSM) tracks every move. If you stop today and come back in a week, `/beads:resume` puts you exactly where you left off. No memory drift. No context fatigue.

---

### How it works

1. **Plan.** Define your phases in the Ledger.
2. **Initialize.** Activate a bead. The FSM locks the scope and validates the environment.
3. **Execute.** Build within the guardrails.
4. **Verify & Commit.** The system runs your tests. If they pass, it stages your changes and commits. Automatically.

---

### Why this?

Because "vibes" aren't a version control system.

Beads is for developers who want the speed of AI with the reliability of traditional engineering. It's about shipping clean code without the yapping, the drift, or the waste.

---

## ⚡️ TL;DR: The Sequence

Beads replaces long, drifting AI chats with a series of atomic work sessions. Each session (a **Bead**) is isolated — no guessing, no drift. Every bead follows a hard-coded sequence:

- **🪧 Isolate:** Mount only the required files.
- **⚙️ Execute:** Build the feature.
- **✅ Verify:** Run tests automatically.
- **💾 Commit:** Save progress to Git.
- **🧹 Clear:** Reset context for the next task (recommended, not enforced).

You run two commands: `/clear` (recommended) and `/beads:run`. The system handles the rest.

---

### The System Architecture

| Component         | Function                       | Result                                           |
|-------------------|--------------------------------|--------------------------------------------------|
| **Ledger**        | Persistent state file          | Total project memory. No drift.                  |
| **FSM**           | Workflow controller            | Tasks happen in the correct order. Always.       |
| **Guard**         | Tool-level blocking hooks      | Claude physically cannot break the protocol.     |
| **Smart Routing** | Dynamic model switching        | Opus for logic, Sonnet for speed. Lower costs.   |
| **Phase Freeze**  | Read-only summaries            | Completed work stays completed. Zero noise.      |

---

### The Operator's Loop

- **Init:** `beads init` to prime the environment.
- **Plan:** `/beads:plan` to map the milestones.
- **Run:** `/beads:run` to execute a task.
- **Repeat:** Repeat until the phase is sealed.

---

## ◆ Get Started

### 01 Installation

Requires pipx for global binary isolation.

```bash
pipx install git+https://github.com/badgateway505/CLAUDE-BEADS.git
```

No `pipx`? ● `brew install pipx` or `pip install pipx`

### 02 Setup

Initialize the framework within your repository.

```bash
cd your-project/
beads init
```

The framework generates three primary layers:
- `.beads/` ● The Engine (FSM, Ledger, Templates)
- `.claude/` ● The Perimeter (Skills and Enforcement Hooks)
- `.planning/` ● The Roadmap (Phase and Bead definitions)

### 03 Execution Flow

1. **Plan**: Instruct Claude to map the phase boundaries.

    ```bash
    /beads:plan phase-01
    ```

2. **Isolate** (recommended): Clear the context to maintain token efficiency.

    ```bash
    /clear
    ```

3. **Run**: Execute the active bead.

    ```bash
    /beads:run
    ```

**Expected Output:**

```text
╔═══════════════════════════════════════════════════════════════╗
║  ✓ BEAD READY: 01-01 — Project Architecture                 ║
╚═══════════════════════════════════════════════════════════════╝
  Intent  : Initialize project with core dependencies
  Scope   : pyproject.toml, src/__init__.py
  Verify  : pytest tests/ -v
  Phase   : 1 of 3  |  Model: sonnet  |  Tier: AUTO

  ● Executing...
  ✓ Verification passed
  🔒 Committed: beads(01-01): Setup project structure
  → Next: 01-02-database-schema
```


### 04 The Cycle

Repeat the Clear → Run loop for each task. Once the phase is complete, seal it and move to the next milestone.

```bash
/beads:close-phase
/beads:plan phase-02
```

### ◆ Security Notice

Beads operates at the tool-call level. If the FSM is not initialized or a verification fails, all write operations are physically rejected by the shell. This is a deterministic lock on your project’s integrity.

---

---

## 03. Technical Architecture

### 03.1 The Ledger ● ledger.md

The Source of Truth for the entire project lifecycle. It is a structured Markdown database that the FSM uses to synchronize state between sessions.

* Roadmap: A high-level registry of Phases and their current status (OPEN | CLOSED).

* Bead Checklist: A deterministic list of tasks.

* Persistence: By reading the Ledger, Claude can /beads:resume any project after a break with zero context reconstruction.

### 03.2 The Finite State Machine ● fsm.py

A deterministic controller that manages the bead lifecycle through a rigid state transition model.

```
DRAFT → EXECUTE → VERIFY → COMPLETE
                    ↓
                 RECOVER → EXECUTE (retry)
                    ↓
                  FAILED (after 3 attempts)
```

Core Guardrails:

* Phase Guard: Blocks initialization of any bead if the previous Phase is not marked as CLOSED.

* IRON LOCK: Model-level enforcement. If a bead is tagged for Opus, the FSM physically blocks execution if the active model is Sonnet.

* Verified Commit: Success is impossible without an exit 0 from the verification command and a successful git commit.

* Circuit Breaker: Maximum 3 retries per bead. After failure, the system triggers a mandatory rollback to the last known stable SHA.

---

### 03.3 Physical Enforcement ● The Guard

Beads does not rely on prompts for security. It operates via Claude Code PreToolUse hooks — shell scripts that validate intents before the tool executes.

| Hook               | Target Tools      | Function                                                         |
|--------------------|-------------------|------------------------------------------------------------------|
| protect-files.sh   | Edit, Write, NotebookEdit | Immutability for Ledger, FSM, Protocol, and CLAUDE.md.           |
| guard-bash.sh      | Bash                      | Blocks shell-level tampering (sed, rm, echo) on protected paths. |
| workflow-guard.sh  | Edit, Write, NotebookEdit | Blocks source code edits unless the FSM is in EXECUTE state.     |

> Logic: Hooks return exit 2 upon protocol violation. In the Beads ecosystem, this is the standard signal to the shell to terminate the tool execution immediately. This creates a hardware-level boundary: Claude cannot rewrite its instructions or bypass the state machine because it lacks the authority to "unplug" the underlying environment hooks.

---

### 03.4 Token Economy

Efficiency is achieved through Context Isolation. Instead of feeding the entire codebase into the window, Beads uses a granular injection model.

* Mandatory Scope: Only files defined in the bead metadata are read.

* Context Reset: Running `/clear` between beads is recommended to flush the window and maximize token savings.

* Phase Freezing: Closed phases are compressed into XX-SUMMARY.md. Claude references the summary, never the raw source of completed phases.

Performance Curve:

* Standard AI Work: Context grows exponentially (4K → 40K → 120K+).

* Beads Workflow: Context stays flat (approx. 4K tokens per bead).

---

### 03.5 Model Routing

Beads optimizes the cost-to-performance ratio by assigning specific models to task complexities:

* Opus ● Architecture and complex refactoring.

* Sonnet ● Feature implementation and logic.

* Haiku ● Formatting, documentation, and boilerplate.

---

## 04. System Specs

* Runtime: Python 3.11+

* Interface: Claude Code CLI

* Storage: Local JSON/Markdown

* VCS: Git (Atomic Commit protocol)

---

## 05. Interface

### 05.1 Terminal

Standard CLI tools for environment management.

| Command        | Function                                                                  |
|----------------|---------------------------------------------------------------------------|
| `beads init`   | Scaffold project structure, install skills, and register hooks.           |
| `beads status` | Display active state, roadmap progress, and next pending task.            |
| `beads help`   | Show manual for CLI commands.                                             |

### 05.2 Claude Code

High-level skills for workflow execution.

| Command            | Function                                                                          |
|--------------------|-----------------------------------------------------------------------------------|
| `/beads:plan`      | Decompose a phase into atomic, verifiable beads.                                  |
| `/beads:run`       | Execute the next task. Enforces guards, runs verification, and commits.           |
| `/beads:research`  | Time-boxed research spike. Outputs findings to `.planning/spikes/`.               |
| `/beads:resume`    | Synchronize Claude's context with the current Ledger state.                       |
| `/beads:close-phase`| Seal current phase and generate `XX-SUMMARY.md`.                                 |

---

## 06. Hierarchy

```
my-project/
├── .beads/
│   ├── bin/                 ● FSM Engine and Routing logic
│   ├── templates/           ● Implementation and Research templates
│   ├── PROTOCOL.md          ● Full execution specification
│   ├── config.yaml          ● System configuration
│   └── ledger.md            ● Project Source of Truth
│
├── .claude/
│   ├── hooks/               ● Physical Enforcement Layer (Shell)
│   ├── settings.json        ● Hook registration
│   └── skills/              ● Claude-native skill definitions
│
├── .planning/
│   ├── PROJECT.md           ● Vision and high-level requirements
│   ├── phases/              ● Detailed bead specifications
│   └── spikes/              ● Research and architectural findings
│
├── CLAUDE.md                ● Protected project context (Immutable)
└── .gitignore
```

---

## 07. Development

### 07.1 Contributing

- Fork the repository.
- Create a feature branch (`git checkout -b feat/id`).
- Commit changes following the feat/fix convention.
- Open a Pull Request.

**Note:** All code must adhere to the ruff style guide and include relevant tests.

### 07.2 License

Distributed under the MIT License. See LICENSE for details.

---

## 08. FAQ

**How is this different from GSD Beads or other AI workflow frameworks?**
Most frameworks rely on prompts to guide the AI. Beads uses physical shell hooks that block tool calls before they execute. Claude can't bypass the workflow, edit protected files, or skip verification — the infrastructure prevents it, not the instructions.

**Does this work with ChatGPT, Copilot, or other AI assistants?**
No. Beads is built specifically for Claude Code's PreToolUse hook system. The physical enforcement layer depends on Claude Code's architecture.

**How much does it save on tokens?**
Typically 60-70%. Each bead reads only its scoped files (~4K tokens) instead of the entire codebase (80-120K+). Phase freezing prevents re-reading completed work.

**Can Claude bypass the guards?**
Direct tool calls (Edit, Write, Bash) are fully enforced — Claude cannot bypass them. The one known limitation is Claude Code's Task subagent (background agents), which is a Claude Code architectural constraint.

**Do I need to run /clear between every bead?**
It's recommended for optimal token efficiency, but not enforced. Beads works without it — you just use more tokens per session.

**Is this only for big projects?**
Beads shines on multi-phase projects, but even a 5-bead single-phase project benefits from verified commits, context isolation, and model routing.

**Can I use this for vibe coding?**
That's exactly what it's for. All the structure and safety of traditional engineering, none of the ceremony. Two commands: `/clear` and `/beads:run`.

---

<!-- LLM-readable metadata: see llms.txt in repo root for structured summary -->

<div align="center">

Built for developers who value precision over noise.

[Issues](https://github.com/badgateway505/CLAUDE-BEADS/issues) ● [Discussions](https://github.com/badgateway505/CLAUDE-BEADS/discussions)

</div>
