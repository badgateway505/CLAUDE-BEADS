# Claude Beads PRO - Execution Protocol

**Purpose**: Minimize token burn, maximize precision, maintain context over long projects.

---

## Execution Protocol

**⚠️ HARD LOCK MUST BE FIRST — NO FILE READS BEFORE VERIFICATION ⚠️**

0. **Context Clear (HARD LOCK)**:
   - **FIRST ACTION**: Check if user ran `/clear` command
   - Look for `<command-name>/clear</command-name>` tag in current conversation turn
   - If NOT found → **HALT IMMEDIATELY**. Report: "⚠️ Run `/clear` before executing new bead"
   - DO NOT read any files before this check
   - DO NOT check FSM state before this check
   - DO NOT proceed to any other step before this check

1. **Load Context**: Read `.beads/ledger.md` ONLY for project state
   - Check "Active Bead" section in ledger
   - DO NOT read `.beads/fsm-state.json` yet (only exists during active bead execution)
   - FSM state file is created by `init` and deleted when bead completes

2. **Auto-Queue Check**: Active Bead is automatically set by fsm.py (see Next-In-Line Protocol)
   - If shows **PENDING** → Proceed immediately to step 3
   - If shows **None** → Check if project complete or manually scan for next bead

3. **FSM Init (auto-transitions to EXECUTE)**: Execute silently. Report: "✅ Initialized & ready"
   - Model guard check (IRON LOCK) - halts if model mismatch
   - Auto-transitions to EXECUTE state (no manual transition needed)
   - Ledger auto-synced
   - After init, `.beads/fsm-state.json` exists and state is EXECUTE

4. **Context Isolation**: NEVER read frozen phases - use `XX-SUMMARY.md` instead.

5. **Execute Tasks**: Complete tasks in order. One atomic commit per logical change.
   - **CRITICAL**: Execute Edit operations SEQUENTIALLY, not in parallel, to prevent UI hangs
   - Multiple edits on the same file MUST be sequential (wait for first to complete before second)
   - Parallel tool calls are OK for independent Read/Grep operations only

6. **Verify (auto-transitions to COMPLETE)**: Execute silently. Report: "✅ Verified" or "❌ Failed"
   - Runs verification command
   - On success: auto-transitions to COMPLETE, marks bead [x] in ledger, queues next bead
   - On failure: retry logic (circuit breaker after 3 attempts)

7. **Freeze**: When phase completes, add detailed files to `.claudeignore`

---

## Spike Bead Protocol (Exploration Mode)

**Spike beads** are time-boxed explorations that produce findings, not production code.

### When to Use Spikes

- Evaluating new libraries/APIs before committing
- Investigating feasibility of an approach
- Debugging complex issues where root cause is unclear
- Prototyping to inform architecture decisions

### Spike Execution Flow

1. **Init** - Same as implementation beads (auto-transitions to EXECUTE)
2. **Explore** - Time-boxed investigation (1-3 hours max)
3. **Document Finding** - Create finding document (`.planning/spikes/SPIKE-XX-YY-topic.md`)
4. **Complete** - Direct transition from EXECUTE to COMPLETE (no verification needed)

```bash
# Spike workflow
fsm.py init spike-06-05 --confirm-clear --active-model sonnet --bead <path>
# [do exploration work]
# [create finding document]
fsm.py transition complete  # No verify step for spikes
```

### Spike Characteristics

| Attribute | Implementation Bead | Spike Bead |
|-----------|-------------------|------------|
| Type | `implementation` | `spike` |
| Verification | Required | None (`verification_tier: NONE`) |
| Time limit | Until done | 1-3 hours (time-boxed) |
| Output | Production code | Finding document |
| Failure allowed | No (circuit breaker) | Yes (learning is valuable) |
| Commit required | Yes | Optional (finding is deliverable) |

### Finding Document Template

See `.beads/templates/spike-bead.md` for full template. Key sections:
- **Question** - What are we trying to learn?
- **Outcome** - ✅ Works / ❌ Doesn't work / ⚠️ Blocked / ❓ Inconclusive
- **Evidence** - Observations, test results, error messages
- **Recommendation** - Next steps based on outcome

---

## Next-In-Line Protocol (AUTOMATED)

**Beads are automatically queued by `fsm.py` to eliminate workflow friction.**

**When you read the ledger:**
1. If Active Bead shows **Bead-XX-YY: PENDING** → Immediately proceed with execution (step 3)
2. If Active Bead shows **None** with "Next Actions" → Tell user to choose an option (plan next phase, transition, etc.)
3. If Active Bead shows **None** with no pending beads → Phase/project complete, suggest transition or congratulate

**Auto-queue behavior:**
- When a bead completes (via `fsm.py verify` success), next pending bead is automatically set as Active
- This eliminates the extra "suggest → confirm → execute" round-trip
- User runs `/clear` + `/beads:run` and agent immediately starts next bead

**CRITICAL**: No user confirmation needed if Active Bead is already set to PENDING.

---

## Verification Tiers (Honest Testing)

**Philosophy:** Don't fake verification. Choose the appropriate tier for your bead.

| Tier | When | How |
|------|------|-----|
| **AUTO** | Automated tests exist | FSM runs verification_cmd (pytest, mypy, ruff) |
| **MANUAL** | Human verification needed | Agent confirms checklist items (hardware, visual) |
| **NONE** | Exploratory work | No verification (spike beads, research) |

**Examples:**

```yaml
# AUTO tier (default) - Automated test command
verification_tier: AUTO
verification_cmd: "pytest tests/test_foo.py -v"
```

```yaml
# MANUAL tier - Checklist confirmation
verification_tier: MANUAL
verification_checklist:
  - [ ] Dashboard displays correctly in browser
  - [ ] User clicks filter button and chart updates
  - [ ] Data refreshes automatically every 30 seconds
```

```yaml
# NONE tier - No verification
verification_tier: NONE
rationale: "Spike bead - produces finding document, not verified code"
```

**See:** `.beads/VERIFICATION-TIERS.md` for full documentation and examples.

---

## Context Clear (HARD LOCK) — ENFORCED

**Before executing ANY bead, the user MUST run `/clear` to reset conversation context.**

**⚠️ CRITICAL: This check MUST happen BEFORE any file reads or state checks ⚠️**

**Verification Steps (in exact order):**
1. **FIRST**: Look for `<command-name>/clear</command-name>` in the current conversation turn
2. If NOT found → **STOP**. Report: "⚠️ Run `/clear` before executing new bead"
3. If found → Continue to read ledger and proceed with execution

**Enforcement:**
- `fsm.py init` requires `--confirm-clear` flag
- If flag missing → **EXIT WITH ERROR** (human intervention required)
- Agent MUST pass this flag to confirm user ran `/clear`
- Agent MUST verify `/clear` was run BEFORE reading any project files

**Why this matters:**
- Prevents context pollution from previous beads
- Ensures token efficiency (fresh start per bead)
- Maintains protocol integrity across long projects
- Avoids wasting tokens on file reads if context isn't clear

**Exception:** Planning and research phases (`/beads:plan-phase`, `/beads:research-phase`) do NOT require `/clear`.

**Technical Implementation:**
```bash
# REQUIRED: Agent must confirm user ran /clear
python3 .beads/bin/fsm.py init 06-01 \
  --confirm-clear \
  --active-model sonnet \
  --bead .planning/phases/06-client-implementation/beads/06-01-audio-capture-websocket-client.md

# If --confirm-clear is missing, FSM exits with error
```

---

## Model Guard (IRON LOCK) — ENFORCED

The `--active-model` flag in fsm.py init is the hard lock:

```bash
# Execute silently. If this exits 1, NO state is created.
python3 .beads/bin/fsm.py init 04-01 \
  --confirm-clear \
  --active-model opus \
  --bead .planning/phases/04-server-voice-loop/beads/04-01-ipc-foundation.md
```

- Exit 0: Report "✅ Model guard passed" and continue
- Exit 1: **STOP IMMEDIATELY**. Report: "❌ IRON LOCK: Bead requires [X], running [Y]"

---

## Silent FSM Protocol

**Execute FSM commands silently. Report outcomes only, NEVER the commands.**

| Step | Command (execute silently) | Report to user |
|------|---------------------------|----------------|
| Init | `fsm.py init <id> --confirm-clear --active-model <m> --bead <path>` | "✅ Initialized & ready" |
| Verify | `fsm.py verify "<cmd>"` (auto-prefixes `uv run` if needed) | "✅ Verified" or "❌ Verification failed (attempt N/3)" |

**Simplified workflow (ceremony reduced):**
- `init` now auto-transitions to EXECUTE state (no manual transition needed)
- `verify` already auto-transitions to COMPLETE on success
- Manual transitions removed from normal workflow

**Auto-sync feature:** Ledger is automatically synchronized after `init` and `verify` commands. No manual `sync-ledger` step needed.

**Auto-prefix feature:** `fsm.py verify` automatically adds `uv run` prefix for Python commands (pytest, python, mypy, ruff, coverage) if not already present. This prevents common environment errors.

---

## Actions Requiring Rationale

**Philosophy:** Strong conventions, not rigid rules. Deviations are permitted with documented rationale.

### Hard Locks (No Exceptions)

These are enforced by the FSM and cannot be bypassed:

- 🔒 **Execute bead without `/clear`** — HARD LOCK enforced by FSM (--confirm-clear required)
- 🔒 **Skip model guard** — IRON LOCK enforced by FSM (--active-model must match)

### Actions Requiring Documented Rationale

These should be avoided by default, but exceptions are permitted when documented in bead metadata or ledger session notes:

- ⚠️ **Manual ledger edit** — Requires rationale (e.g., "Emergency architecture pivot", "Fixing FSM sync bug")
- ⚠️ **Manual fsm-state.json edit** — Requires rationale (e.g., "Recovering from corrupted state")
- ⚠️ **Reading frozen phase files** — Requires rationale (e.g., "Debugging regression", "Understanding legacy design")
- ⚠️ **Skipping verification** — Requires rationale (e.g., "Spike bead exploration", "Manual testing only")
- ⚠️ **Announcing FSM commands** — Requires rationale (e.g., "Debugging workflow", "Teaching protocol")

### How to Document Rationale

**In bead metadata:**
```yaml
<meta>
verification_tier: NONE
rationale: "Spike bead - exploratory work, produces finding not code"
```

**In ledger session notes:**
```markdown
## Session Notes
- Manual ledger edit authorized: 2026-01-21
  Rationale: Architecture pivot from RPi5+UDP to Cloud VPS+WebSocket
  Required updating Phase 5 description and bead list
```

**In commit messages:**
```
docs: manual ledger sync after cloud pivot

Rationale: Emergency architecture change required updating
active phase description. FSM sync would not capture
the scope of changes needed.
```

---

## Failure Handling (Circuit Breaker)

- **Attempt 1**: Soft retry — self-correction, same approach
- **Attempt 2**: Hard rollback — `git reset --hard [initial_sha]` + strategic pivot
- **Attempt 3**: Circuit breaker — STOP and request human intervention

---

## Token Efficiency Rules

- READ `.beads/ledger.md` for context (NOT full conversation history)
- READ ONLY active bead + files in `<context_files>` section
- NEVER read `.claudeignore` files (frozen phases)
- DISCARD internal reasoning after bead completion
- SUMMARIZE outcomes in ≤3 sentences for ledger

---

## Research Protocol

**When starting research, ALWAYS use `.beads/templates/research-schema.md` as a blueprint.**

Research files (XX-RESEARCH.md) MUST follow strict XML-anchored structure:
- `<research_meta>` — Topic, model, date, phase
- `<objective>` — Single sentence question to answer
- `<constraints>` — YAML with performance/compatibility/resource limits
- `<pattern>` — Technical patterns with tradeoff tables + verification
- `<alternatives>` — Concrete options with quantified comparisons
- `<verify_cmd>` — Deterministic command proving findings

**Prohibited**: Narrative fluff, subjective language, unquantified claims.
**Required**: Technical specifications, verification commands, tradeoff analysis.

See `.planning/framework/V2-SPEC.md` for reference implementation.

---

## Model Routing

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Architecture/Planning | Opus | Superior long-horizon reasoning |
| Research | Opus | Deep analysis, SOTA exploration |
| Implementation | Sonnet | Best code quality + speed/cost balance |
| Verification | Sonnet | Fast feedback loops |
| Summarization | Haiku | Cheap, fast, sufficient for context compression |

---

## File Priority (Read Order)

**⚠️ BEFORE READING ANYTHING: Verify HARD LOCK (`/clear` command) ⚠️**

**When starting execution (before init):**
1. `.beads/ledger.md` — Current project state (check "Active Bead" section)
2. DO NOT read `.beads/fsm-state.json` (doesn't exist between beads)

**During bead execution (after init):**
1. `.beads/fsm-state.json` — Runtime state (retry count, verification status)
2. Active bead file — `XX-YY-name.md`
3. `XX-SUMMARY.md` files — Frozen phase context
4. `XX-RESEARCH.md` — If referenced in bead
5. Source files — Only those in bead's `<context_files>`

**NEVER read:** Files in `.claudeignore`, completed beads from frozen phases, other phases' PLAN/CONTEXT files

---

## State Management (Single Source of Truth)

**Authoritative Sources:**
- **Runtime State**: `.beads/fsm-state.json` — Current bead, state, retry count (only exists during active bead)
- **Historical Record**: `.beads/ledger.md` — Completed work (checkboxes: `[x]` = done, `[ ]` = pending) + active bead status
- **Templates**: Bead files (`.planning/phases/XX-*/beads/XX-YY-*.md`) — Task specifications (static)

**FSM State File Lifecycle:**
- Does NOT exist between beads (clean slate)
- Created by `fsm.py init` when bead starts
- Updated during execution (`transition`, `verify`)
- Deleted by `fsm.py transition complete` when bead finishes
- If missing at execution start → normal (check ledger "Active Bead" section instead)

**State Flow:**
```
[Bead Template] → FSM init → [fsm-state.json] → FSM sync-ledger → [ledger.md]
    (static)         (runtime)                      (history)
```

**Critical Rules:**
1. Bead files are templates — they NEVER change during execution
2. `fsm-state.json` owns current execution state
3. Ledger is write-only from FSM (no manual edits)
4. Ledger checkboxes (`[x]`/`[ ]`) are authoritative for completion status
5. Phase-level `@status()` annotations are metadata (human-readable, not used by FSM)
6. **ONLY list beads in ledger AFTER bead files exist** — Never list planned beads before files are created

**How State is Synchronized:**
- FSM `init`: Creates `fsm-state.json`, extracts `model` and `verification_cmd` from bead file
- FSM `verify`: Updates `last_verification_passed` flag in `fsm-state.json`
- FSM `transition complete`: Marks bead as `[x]` in ledger, clears active bead
- FSM `sync-ledger`: Writes FSM state to ledger's "Active Bead" section

**What's NOT synchronized:**
- Bead file `<meta>` sections don't contain runtime state (status field removed)
- Phase `@status()` annotations are decorative (manually updated during /transition)
- Cost estimates are approximations, not tracked by FSM
