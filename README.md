<div align="center">

# 🧵 Claude Beads v1.1

### STOP context loss, token burn, rules bypass.

**Physical enforcement framework for atomic AI-assisted development**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Version: 1.1.0](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/badgateway505/CLAUDE-BEADS/releases/tag/v1.1.0)

[Why Beads?](#-why-beads) · [TL;DR](#-tldr-how-it-works) · [Get Started](#-get-started) · [Deep Dive](#-deep-dive-for-developers) · [Commands](#-commands)

---

<!-- Replace with your terminal screenshot showing beads commands -->
<img src="docs/terminal-preview.png" alt="Claude Beads terminal output" width="700">

*`beads init` → `/beads:plan` → `/beads:run` — that's the whole workflow*

</div>

---

## 🤔 Why Beads?

### The problem every Claude developer hits

You start a project with Claude. First hour is magic. By hour three, the context window fills up. Claude forgets what it did earlier. You copy-paste the same context every session. Your git history is a graveyard of "WIP" and "fix" commits. **And the worst part?** Claude silently skips steps, edits files it shouldn't touch, and drifts from the plan — and you don't notice until something breaks.

Prompt-based frameworks (like GSD and similar workflow systems) try to solve this by writing elaborate instructions and hoping the AI follows them. Sometimes it does. Sometimes it doesn't. You have no way to know until it's too late.

### Why existing frameworks fall short

Most AI workflow frameworks share the same fundamental flaw: **they rely on prompts for compliance.** They tell the model "please follow these steps" and "please don't edit this file" — but there's nothing stopping the model from ignoring those instructions. No enforcement. No guardrails. Just trust.

They also tend to be built for enterprise workflows — heavy on ceremony, formal approvals, status meetings in markdown form. That's great if you're coordinating a team of 10. But if you're a **solo developer** or a **vibe-coder** who just wants to ship, all that overhead is friction that slows you down without adding value.

And token economy? Most frameworks don't even think about it. They let Claude read your entire codebase every session, burning through your API budget while the model drowns in irrelevant context.

### What Beads does differently

**Claude Beads doesn't ask. It enforces.**

Instead of prompting Claude to follow rules, Beads uses **physical hooks** (Claude Code PreToolUse hooks) that fire before every tool call. Claude literally *cannot* edit protected files, skip verification, or work outside an active bead — the infrastructure blocks it at the tool level, regardless of what the model decides to do.

Three things make Beads fundamentally different:

1. **Physical enforcement** — Shell hooks block unauthorized actions before they execute. Claude can't rewrite its own instructions, skip workflow steps, or edit files outside the active scope. Not "shouldn't" — *can't*.

2. **Token economy built in** — Each bead gets its own context window with only the files it needs. No rereading the entire codebase. No stale context from 3 phases ago. Typical savings: **60-70% fewer tokens** compared to working without Beads.

3. **Nothing gets lost** — The FSM (finite state machine) tracks every bead's state. The ledger records every outcome. Come back after a week and `/beads:resume` puts you right where you left off.

---

## ⚡ TL;DR: How It Works

*For everyone — no deep technical knowledge required.*

### The idea is simple

Instead of one massive conversation where Claude tries to build your whole project (and inevitably loses the plot), **Beads breaks your work into small, isolated tasks called "beads."**

Each bead is like a focused 30-minute work session:
- It knows exactly what files to read
- It knows exactly what to build
- It verifies its own work (runs tests)
- It commits the code automatically
- Then it hands off to the next bead

**You just type two commands: `/clear` and `/beads:run`. Repeat until done.**

### The five modules

| Module | What it does | In plain English |
|--------|-------------|-----------------|
| **Ledger** | Tracks all progress in one file | Your project's memory — who did what, what's next, what's done |
| **FSM** | Controls the workflow steps | A traffic cop that ensures steps happen in the right order |
| **State Guard** | Blocks unauthorized actions | A bouncer — Claude physically can't touch files it shouldn't |
| **Model Routing** | Picks the right Claude model | Uses Opus for hard stuff, Sonnet for normal work, Haiku for simple tasks. Saves money. |
| **Phase Freezing** | Isolates completed work | When a phase is done, it's sealed off. No stale context leaking into new work. |

### What you actually do

```
1. Install Beads and run `beads init` in your project
2. Tell Claude to plan: /beads:plan phase-01
3. Execute beads one by one: /clear → /beads:run → repeat
4. Close the phase: /beads:close-phase
5. Plan next phase, repeat
```

That's it. Beads handles verification, commits, context management, and progress tracking automatically.

---

## 🚀 Get Started

### Step 1: Install

```bash
pipx install git+https://github.com/badgateway505/CLAUDE-BEADS.git
```

No `pipx`? → `brew install pipx` or `pip install pipx`

### Step 2: Initialize your project

```bash
cd your-project/
beads init
```

It asks two questions (project name, vision), then scaffolds everything:
- `.beads/` — framework engine (FSM, ledger, templates)
- `.claude/` — skills + enforcement hooks
- `.planning/` — your project roadmap

### Step 3: Plan your first phase

In Claude Code:
```
/beads:plan phase-01
```

Claude reads your PROJECT.md and breaks Phase 1 into 3-8 atomic beads.

### Step 4: Execute

```
/clear
/beads:run
```

Output:
```
╔═══════════════════════════════════════════════════════════════╗
║  ✅ BEAD READY: 01-01 — Setup project structure                ║
╚═══════════════════════════════════════════════════════════════╝
  Goal    : Initialize project with dependencies and config
  Scope   : pyproject.toml, src/__init__.py
  Verify  : pytest tests/ -v
  Phase   : 1 of 3  |  Model: sonnet  |  Tier: AUTO

  💻 Executing...
  ✓ Verification PASSED
  ✓ Committed: beads(01-01): Setup project structure (a1b2c3d)
  ➡️ Next: 01-02-add-database-schema
```

Repeat `/clear` → `/beads:run` for each bead.

### Step 5: Close phase, move on

```
/beads:close-phase
/beads:plan phase-02
```

---

## 🔬 Deep Dive (For Developers)

### The Ledger

`.beads/ledger.md` — a markdown file that serves as the single source of truth for the entire project. Contains:

- **Roadmap overview** — phase table with status (OPEN/CLOSED)
- **Bead checklist** — `[ ]` pending, `[x]` complete, with each bead ID
- **Active bead section** — what's currently running, retry count if applicable

The FSM writes to the ledger automatically. When you run `/beads:resume` after a break, Claude reads the ledger and knows exactly where you are — no context reconstruction needed.

### The FSM (Finite State Machine)

`.beads/bin/fsm.py` — a deterministic state machine that controls bead execution lifecycle:

```
DRAFT → EXECUTE → VERIFY → COMPLETE
                    ↓
                 RECOVER → EXECUTE (retry)
                    ↓
                  FAILED (after 3 attempts)
```

**Key enforcement points:**

- **Phase Guard** — `fsm.py init` checks that the previous phase is CLOSED before allowing a new phase's bead to start. Also blocks execution if bead files don't exist (can't execute unplanned work).
- **IRON LOCK (Model Guard)** — Bead metadata specifies `model: opus|sonnet|haiku`. The FSM compares this against the active Claude model and blocks mismatches. Prevents using cheap models for complex tasks.
- **Verified Commit** — When `fsm.py verify` runs the verification command and it passes (exit 0), it automatically stages scope files from the bead's `<context_files>` block, commits with `beads(<id>): <title>`, and only then transitions to COMPLETE. If the git commit fails, the bead stays in EXECUTE — no DONE without a real commit.
- **Circuit Breaker** — 3 retries max. After that, the bead is marked FAILED and you can rollback to the initial commit SHA.
- **State Summary** — On init, the FSM prints a compact block with goal, scope files, verification command, and phase progress. This eliminates the need for Claude to re-read the ledger at the start of each bead.

State is persisted in `.beads/fsm-state.json` (protected from manual editing by hooks).

### State Guard (Physical Enforcement Layer)

Three shell scripts registered as Claude Code `PreToolUse` hooks in `.claude/settings.json`:

**`protect-files.sh`** — Matcher: `Edit|Write|NotebookEdit`
- Blocks modifications to: `ledger.md`, `fsm-state.json`, `PROTOCOL.md`, `.beads/bin/`, `.claude/hooks/`, `.claude/settings.json`, `CLAUDE.md`
- Why `CLAUDE.md`? Without this, Claude can rewrite its own instructions to bypass the workflow.

**`guard-bash.sh`** — Matcher: `Bash`
- Parses the bash command and blocks anything referencing protected paths
- Whitelists only `fsm.py` and `router.py` CLI invocations
- Prevents workarounds like `sed -i`, `echo >`, `rm`, `cat <<EOF >` on protected files

**`workflow-guard.sh`** — Matcher: `Edit|Write|NotebookEdit`
- Blocks edits to project source files unless `fsm-state.json` exists AND `current_state == "execute"`
- Validates state content, not just file existence (prevents stale state bypass)
- Skips framework paths (`.beads/`, `.claude/`, `.planning/`) so planning and framework operations still work

**How hooks work:** They fire before the tool executes. Exit code 2 = BLOCK (Claude sees a rejection message). Exit code 0 = ALLOW. The model cannot disable, modify, or bypass hooks — they're infrastructure-level, not prompt-level.

**Known limitation:** Claude Code's Task subagent (background agents) can bypass hooks. This is a Claude Code architectural constraint. All direct tool calls are fully enforced.

### Token Economy

Each bead specifies exactly which files Claude should read in `<context_files>`:

```markdown
<context_files>
mandatory:
  - src/auth/login.py
  - tests/test_auth.py
reference:
  - 01-SUMMARY.md
</context_files>
```

Claude reads **only these files** — not the whole codebase. Combined with `/clear` between beads (which resets the context window), this means:

- Bead 1: ~4K tokens (bead spec + 2 files)
- Bead 2: ~3K tokens (different bead, different files)
- Bead 50: still ~4K tokens

**Without Beads:** 80K → 90K → 120K → context limit. **With Beads:** flat ~4K per bead.

Phase freezing amplifies this: when Phase 1 closes, all its files get compressed into `01-SUMMARY.md`. Future beads reference the summary, never the original files.

### Model Routing

Bead metadata specifies the required model:

```yaml
model: sonnet       # Implementation work
model: opus         # Architecture, complex refactoring
model: haiku        # Formatting, typos, simple updates
```

IRON LOCK in the FSM enforces this at init time. If you're running Sonnet and the bead requires Opus, execution is blocked with a clear message.

**Typical cost breakdown:** ~70% of beads use Sonnet, ~20% use Haiku, ~10% use Opus. Compared to running everything on Opus, this yields **60-70% cost reduction**.

---

## 📚 Commands

### Terminal

| Command | What it does |
|---------|-------------|
| `beads init` | Initialize Beads in your project. Creates `.beads/`, `.claude/`, `.planning/`, enforcement hooks. Validates structure. |
| `beads status` | Show active bead, roadmap progress, next action. |
| `beads help` | Show available commands. |

### Claude Code

| Command | What it does |
|---------|-------------|
| `/beads:plan <phase>` | Break a phase into 3-8 atomic beads with specs, context files, and verification. |
| `/beads:run` | Execute the next pending bead. Enforces model guard, phase boundaries, runs verification, auto-commits. |
| `/beads:research <topic>` | Time-boxed research spike. No code changes. Produces findings in `.planning/spikes/`. |
| `/beads:resume` | Restore context after a break. Reads ledger, shows progress, suggests next action. |
| `/beads:close-phase` | Freeze current phase into `XX-SUMMARY.md`. Blocks next phase until this runs. |
| `/beads:help` | Show framework help. |

---

## 🎨 Project Structure

```
my-project/
├── .beads/
│   ├── bin/
│   │   ├── fsm.py              # Execution engine (state machine)
│   │   └── router.py           # Model routing logic
│   ├── templates/              # Bead templates (implementation, spike, examples)
│   ├── PROTOCOL.md             # Full execution protocol
│   ├── config.yaml             # FSM and routing config
│   └── ledger.md               # Single source of truth
│
├── .claude/
│   ├── hooks/
│   │   ├── protect-files.sh    # State Guard: file protection
│   │   ├── guard-bash.sh       # State Guard: bash filtering
│   │   └── workflow-guard.sh   # State Guard: active bead enforcement
│   ├── settings.json           # Hook registration
│   └── skills/                 # /beads:* skill implementations
│
├── .planning/
│   ├── PROJECT.md              # Project vision and goals
│   ├── phases/                 # Bead specs per phase
│   └── spikes/                 # Research findings
│
├── CLAUDE.md                   # Project context (protected)
└── .gitignore
```

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/thing`)
3. Commit (`git commit -m 'feat: add thing'`)
4. Push and open a PR

Follow ruff style. Add tests. Update docs.

---

## 📜 License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Built for solo developers and vibe-coders who ship.**

⭐ Star if Beads helps you build better.

[Issues](https://github.com/badgateway505/CLAUDE-BEADS/issues) · [Discussions](https://github.com/badgateway505/CLAUDE-BEADS/discussions)

</div>
