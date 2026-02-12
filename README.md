<div align="center">

# 🧵 Claude Beads

### *Stop drowning in context. Start building with beads.*

**Atomic task execution for AI-assisted development**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

[Features](#-core-concepts) • [Quick Start](#-quick-start) • [How It Works](#-how-it-works) • [Commands](#-commands) • [Documentation](#-documentation)

---

### 🎬 See It In Action

[![asciicast](https://asciinema.org/a/kVg8wSaH7eRQR8o1.svg)](https://asciinema.org/a/kVg8wSaH7eRQR8o1)

*Click to watch: `beads init` in 30 seconds*

</div>

---

## 🤔 The Problem

You're building a complex project with Claude. Three hours in, you hit the context window. Claude starts forgetting what happened in bead 1 while working on bead 47. You copy-paste the same project context every session. Your git history is a mess of "WIP" commits. **Sound familiar?**

## 💡 The Solution

**Claude Beads breaks your project into atomic "beads"** - small, verifiable tasks that build on each other. Each bead is self-contained with its own context, verification, and commit. The **ledger** becomes your single source of truth, replacing context window copy-paste hell.

**Think of it like this:** Instead of one massive 200K token conversation, you have 50 focused 4K conversations - each one crystal clear, fully verified, and permanently recorded.

---

## 🎯 Core Concepts

### 🔮 The Ledger - Your Single Source of Truth

The **ledger** (`.beads/ledger.md`) is a living document that tracks everything:
- ✅ Which beads are complete (with verification outcomes)
- 🎯 What's the active bead right now
- 📊 Project roadmap and progress
- 💰 Token costs and model routing

**Why it matters:** When you return to your project after a week, `/beads:resume` reads the ledger and Claude knows *exactly* where you left off. No more "let me read through our previous conversation..."

### 🧵 Beads - Atomic Units of Work

A **bead** is a 30min-2hr task with:
- **Clear goal**: "Add user authentication endpoint"
- **Context files**: Only what's needed (no bloat)
- **Verification**: Automated tests, manual checklist, or exploratory
- **One commit**: All-or-nothing atomicity

**Example bead flow:**
```
📝 Read bead spec → 💻 Execute tasks → ✅ Verify → 💾 Commit → ➡️ Next bead
```

If verification fails? The bead retries (up to 3 attempts) or rolls back. No broken commits.

### 🤖 The FSM - Your Execution Engine

The **Finite State Machine** (`.beads/bin/fsm.py`) enforces discipline:
- 🔒 **HARD LOCK**: Requires `/clear` before execution (no context pollution)
- 🛡️ **IRON LOCK**: Enforces verification before marking complete
- 🔄 **Circuit Breaker**: 3-attempt retry with soft/hard rollback
- ⏭️ **Auto-queue**: Suggests next bead after completion

**Why FSM?** Without it, you'd skip verification, forget to commit, or accidentally mix contexts. The FSM keeps you honest.

### 🎭 Model Routing - Right Brain for the Right Job

Not all tasks need Opus. **Claude Beads routes intelligently:**
- 🧠 **Opus**: Architecture, design, research, complex refactors
- ⚡ **Sonnet**: Implementation, bug fixes, standard features
- 🚀 **Haiku**: Formatting, typos, ledger updates, summaries

**Result:** 60-70% cost reduction while maintaining quality.

### 📦 Phase Freezing - Context Isolation

When Phase 1 is done, it gets **frozen** into `01-SUMMARY.md`. Future beads can't read the old files - only the summary.

**Why?** Prevents Claude from reading stale code, old APIs, or deprecated patterns. Only current context matters.

---

## 🚀 Quick Start

### Installation (30 seconds)

**Prerequisites:** Python 3.11+ and [pipx](https://pipx.pypa.io/) (if you don't have pipx: `brew install pipx` or `pip install pipx`)

```bash
# Install Claude Beads globally
pipx install git+https://github.com/badgateway505/CLAUDE-BEADS.git

# Verify installation
beads --version
# Output: beads, version 1.0.0
```

### Initialize Your Project (2 minutes)

```bash
# Go to your project directory
cd my-awesome-project/

# Initialize Beads
beads init

# Answer two questions:
#   Project name: My Awesome Project
#   Vision: Build an AI-powered task manager

# Done! ✨
```

**What just happened?**
- ✅ Created `.beads/` (framework config, protocols, templates)
- ✅ Created `.claude/` (Claude Code skills for `/beads:*` commands)
- ✅ Created `.planning/` (your PROJECT.md and planning docs)
- ✅ Added Beads section to `CLAUDE.md`
- ✅ Updated `.gitignore` with Beads entries

### Your First Bead (5 minutes)

**In Claude Code:**

```
/beads:plan phase-01

# Claude reads PROJECT.md and breaks Phase 1 into atomic beads
# Example output:
#   📝 Created 5 beads:
#   01-01-setup-venv
#   01-02-install-deps
#   01-03-create-db-schema
#   01-04-write-tests
#   01-05-deploy-staging

/clear  # REQUIRED! Clears context pollution

/beads:run

# Claude:
#   🎯 Executing bead: 01-01-setup-venv
#   📖 Reading context files...
#   💻 Creating virtual environment...
#   ✅ Verification passed!
#   💾 Committed: feat(01-01): setup Python virtual environment
#
#   ➡️ Next bead ready: 01-02-install-deps
```

**Continue with:**
```
/clear
/beads:run  # Executes 01-02

/clear
/beads:run  # Executes 01-03

# ...repeat until phase complete
```

**That's it!** You're building with beads. 🎉

---

## 🎮 How It Works

### The Workflow (Bird's Eye View)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. PLANNING PHASE                                              │
│  ────────────────────────────────────────────────────────────   │
│  You: /beads:plan phase-01                                      │
│  Claude: Reads PROJECT.md, breaks into 5 atomic beads           │
│  Output: .planning/phases/01-phase-name/01-01.md (x5)           │
└─────────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────────┐
│  2. EXECUTION LOOP (repeat for each bead)                       │
│  ────────────────────────────────────────────────────────────   │
│  You: /clear → /beads:run                                       │
│                                                                 │
│  Claude:                                                        │
│    1. Verifies /clear was run (HARD LOCK)                       │
│    2. Reads ONLY: active bead + context files                   │
│    3. Executes tasks sequentially                               │
│    4. Runs verification (tests/checklist/none)                  │
│    5. Creates atomic commit                                     │
│    6. Updates ledger with outcome                               │
│    7. Queues next bead                                          │
└─────────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────────┐
│  3. PHASE COMPLETION                                            │
│  ────────────────────────────────────────────────────────────   │
│  You: /beads:close-phase                                        │
│  Claude: Creates 01-SUMMARY.md, freezes old files               │
│  Result: Phase 1 context isolated, ready for Phase 2            │
└─────────────────────────────────────────────────────────────────┘
```

### Token Efficiency (The Magic)

**Without Beads:**
```
Session 1: 80K tokens (read entire codebase)
Session 2: 90K tokens (read entire codebase AGAIN + new context)
Session 3: 120K tokens (hit limit, start copy-pasting)
Total: 290K tokens 💸
```

**With Beads:**
```
Bead 1: 4K tokens (read ONLY: bead spec + auth.py)
Bead 2: 3K tokens (read ONLY: bead spec + db.py)
Bead 3: 5K tokens (read ONLY: bead spec + api.py + 01-SUMMARY.md)
...
Bead 50: 4K tokens (read ONLY: current context)
Total: ~200K tokens → 70% reduction! 💰
```

**Why?** Each bead has surgical context. No rereading old phases. No stale files.

---

## 📚 Commands

### Terminal Commands (run in your project directory)

#### `beads init`
Initialize Claude Beads in your project.

**What it does:**
- Creates `.beads/`, `.claude/`, `.planning/` directories
- Scaffolds ledger, config, and templates
- Updates `CLAUDE.md` and `.gitignore`

**When to use:** Once per project, at the start.

---

#### `beads status`
Show current project status and next actions.

**What it does:**
- Displays active bead (if any)
- Shows roadmap progress
- Suggests next command to run

**When to use:** Anytime you want to check "where am I?"

---

#### `beads help`
Show available commands and workflow guide.

**What it does:**
- Lists all commands (terminal + Claude)
- Explains workflow steps
- Links to documentation

**When to use:** When you forget the command syntax.

---

### Claude Code Commands (run in Claude Code, in your project directory)

#### `/beads:plan <phase-name>`
Plan a phase by breaking it into atomic beads.

**What it does:**
- Reads `.planning/PROJECT.md` for context
- Analyzes phase requirements
- Creates 3-8 atomic beads (30min-2hr each)
- Writes bead files to `.planning/phases/<phase>/`

**Example:**
```
/beads:plan phase-01-authentication

# Creates:
# .planning/phases/01-authentication/01-01-setup-db-schema.md
# .planning/phases/01-authentication/01-02-hash-password-util.md
# .planning/phases/01-authentication/01-03-login-endpoint.md
# .planning/phases/01-authentication/01-04-jwt-middleware.md
# .planning/phases/01-authentication/01-05-tests.md
```

**When to use:** Start of each phase, after updating PROJECT.md with goals.

---

#### `/beads:run`
Execute the next bead in the queue.

**What it does:**
- **Enforces `/clear` first** (HARD LOCK - prevents context pollution)
- Reads active bead from ledger
- Loads ONLY the context files specified in bead
- Executes tasks step-by-step
- Runs verification (automated tests, manual checklist, or none)
- Creates atomic git commit
- Updates ledger with results
- Suggests next bead

**Example flow:**
```
You: /clear
You: /beads:run

Claude:
  🎯 Executing bead: 01-03-login-endpoint
  📖 Context: src/auth/login.py, tests/test_auth.py

  ✅ Task 1: Create POST /login endpoint
  ✅ Task 2: Validate email/password
  ✅ Task 3: Return JWT token

  🧪 Verification: pytest tests/test_auth.py -v
  ✅ All tests passed!

  💾 Commit: feat(01-03): add login endpoint with JWT
  📝 Ledger updated

  ➡️ Next bead ready: 01-04-jwt-middleware
  Run: /clear then /beads:run
```

**When to use:** After planning, for each bead until phase complete. Always run `/clear` first!

---

#### `/beads:research <topic>`
Research a technical approach before planning.

**What it does:**
- Time-boxed exploration (1-3 hours)
- No code changes, no commits
- Produces finding document in `.planning/spikes/`
- Helps choose between alternatives (e.g., "Redis vs Memcached?")

**Example:**
```
/beads:research database-choice

# Claude investigates PostgreSQL vs MongoDB for your use case
# Creates: .planning/spikes/SPIKE-01-database-choice.md
# Contains: Pros/cons, performance comparison, recommendation
```

**When to use:** Before planning, when approach is unclear.

---

#### `/beads:resume`
Restore project context after a break.

**What it does:**
- Reads ledger history
- Shows completed beads
- Displays active bead (if any)
- Suggests next action

**Example output:**
```
📊 Project: My Awesome Project
📈 Progress: Phase 1 of 3 (33%)

✅ Completed Beads (5):
  01-01-setup-venv ✓
  01-02-install-deps ✓
  01-03-create-db-schema ✓
  01-04-write-tests ✓
  01-05-deploy-staging ✓

🎯 Active Bead: 02-01-user-registration

➡️ Next Action: /clear then /beads:run
```

**When to use:** Start of each session, or after long break.

---

#### `/beads:close-phase`
Close current phase and freeze context.

**What it does:**
- Verifies all beads in phase are complete
- Creates `XX-SUMMARY.md` (frozen context for future beads)
- Marks phase as complete in ledger
- Prevents future beads from reading old phase files (context isolation)

**Example:**
```
/beads:close-phase

# Creates: .planning/phases/01-authentication/01-SUMMARY.md
# Future beads can only read summary, not individual files
# Result: No stale context bleeding into Phase 2
```

**When to use:** After all beads in a phase are complete, before starting next phase.

---

#### `/beads:help`
Show framework help and available commands.

**What it does:**
- Lists all commands with descriptions
- Explains workflow
- Links to protocol and documentation

**When to use:** When you forget command syntax or workflow.

---

## 🧪 Verification Tiers (Honest Testing)

Claude Beads supports **three verification levels** - no more fake `echo "tests pass"` nonsense.

### 🤖 AUTO - Automated Tests
```yaml
verification_tier: AUTO
verification_cmd: "pytest tests/test_auth.py -v"
```
FSM runs the command. Exit code 0 = pass, non-zero = fail. No cheating.

**Use for:** Backend logic, APIs, data processing.

---

### ✅ MANUAL - Checklist Verification
```yaml
verification_tier: MANUAL
verification_checklist:
  - [ ] Dashboard loads without errors
  - [ ] Chart displays correct data
  - [ ] Responsive on mobile
```
Claude asks you to confirm each item. You test manually.

**Use for:** UI/UX, visual design, browser compatibility.

---

### 🔬 NONE - Exploratory Work
```yaml
verification_tier: NONE
type: spike
rationale: "Exploring Redis performance - no code to verify"
```
No verification needed. Produces findings document instead.

**Use for:** Research, spikes, proof-of-concepts.

---

## 📖 Documentation

After running `beads init`, check these files:

- **`.beads/README.md`** - Quick reference guide
- **`.beads/PROTOCOL.md`** - Full execution protocol (how beads work internally)
- **`.beads/VERIFICATION-TIERS.md`** - Testing strategy guide
- **`.beads/RATIONALE-EXAMPLES.md`** - When to document exceptions
- **`.planning/PROJECT.md`** - Your project vision and goals

---

## 🎨 Project Structure

After `beads init`, your project looks like:

```
my-project/
├── .beads/
│   ├── bin/
│   │   ├── fsm.py              # Finite state machine
│   │   └── router.py           # Model routing logic
│   ├── templates/
│   │   ├── bead.md             # Implementation bead template
│   │   ├── spike-bead.md       # Research bead template
│   │   └── examples/           # Example beads
│   ├── PROTOCOL.md             # Execution protocol
│   ├── README.md               # Quick reference
│   ├── VERIFICATION-TIERS.md   # Testing guide
│   ├── config.yaml             # FSM settings, model routing
│   └── ledger.md               # 📜 THE SINGLE SOURCE OF TRUTH
│
├── .claude/
│   ├── skills.yaml             # Skill definitions
│   └── skills/
│       ├── beads-run.md        # /beads:run implementation
│       ├── beads-plan.md       # /beads:plan implementation
│       └── ...                 # Other skills
│
├── .planning/
│   ├── PROJECT.md              # Your vision, goals, phases
│   ├── phases/                 # Bead files (created during planning)
│   │   ├── 01-phase-name/
│   │   │   ├── 01-01-task.md
│   │   │   ├── 01-02-task.md
│   │   │   └── 01-SUMMARY.md   # (created on phase close)
│   │   └── 02-phase-name/
│   └── spikes/                 # Research findings
│
├── CLAUDE.md                   # Claude context (Beads section added)
└── .gitignore                  # (Beads entries added)
```

---

## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Please:** Follow the existing code style (ruff), add tests, update docs.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Star Us!

If Claude Beads helps you build better projects, **give us a star!** ⭐

It helps others discover the framework and motivates us to keep improving it.

---

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/badgateway505/CLAUDE-BEADS/issues)
- **Discussions:** [GitHub Discussions](https://github.com/badgateway505/CLAUDE-BEADS/discussions)

---

<div align="center">

**Built with ❤️ for the Claude community**

[⬆ Back to Top](#-claude-beads)

</div>
