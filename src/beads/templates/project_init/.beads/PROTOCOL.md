
📄 Complete PROTOCOL.md (State Guard Version)

# Claude Beads PRO – Execution Protocol

**Purpose:** Minimize token burn, maximize precision, maintain context over long projects.

---

## State Guard (Hook-Based Enforcement)

Framework files are physically protected by Claude Code hooks.  
Claude CANNOT modify `ledger.md`, `fsm-state.json`, or hook scripts directly.

**Protected by hooks:**
- `.beads/ledger.md` — Edit/Write blocked
- `.beads/fsm-state.json` — Edit/Write blocked
- `.beads/bin/*` — Edit/Write blocked
- `.claude/hooks/*` — Edit/Write blocked (anti-tamper)
- `.claude/settings.json` — Edit/Write blocked (anti-tamper)

**Shell commands also guarded:**
- Direct file manipulation via Bash is blocked
- Only authorized FSM commands pass through

**Authorized access:**
- `python3 .beads/bin/fsm.py <command>` — the **only** way to modify workflow state
- FSM validates model, dependencies, and state transitions internally

**Context clear:** Run `/clear` before each bead for token efficiency. (Recommended, not enforced.)

---

## Execution Protocol

1. **Load Context:** Read `.beads/ledger.md` **only** for project state  
    &nbsp;&nbsp;- Check "Active Bead" section in ledger  
    &nbsp;&nbsp;- **Do not** read `.beads/fsm-state.json` yet (only exists during active bead execution)  
    &nbsp;&nbsp;- FSM state file created by `init`; deleted when bead completes

2. **Auto-Queue Check:** Active Bead is automatically set by `fsm.py` (see Next-In-Line Protocol)  
    &nbsp;&nbsp;- If shows **PENDING** → Proceed immediately to step 3  
    &nbsp;&nbsp;- If shows **None** → Check if project is complete, or manually scan for next bead

3. **FSM Init (auto-transitions to EXECUTE):** Execute silently. Report: "✅ Initialized & ready"
    &nbsp;&nbsp;- Model guard check (**IRON LOCK**) — halts if model mismatch
    &nbsp;&nbsp;- Phase boundary checks (**Phase Guard**) — halts if phase not closed or unplanned
    &nbsp;&nbsp;- Auto-transitions to EXECUTE (no manual transition needed)

    **⛔ ERROR CHECKING REQUIRED:**
    After running FSM command, check output for error markers:
    &nbsp;&nbsp;- `🛡️ Phase Guard` → STOP IMMEDIATELY, show user error, do not continue
    &nbsp;&nbsp;- `🔒 IRON LOCK` → STOP IMMEDIATELY, show user error, do not continue
    &nbsp;&nbsp;- `⛔ Execution BLOCKED` → STOP IMMEDIATELY, show user error, do not continue
    &nbsp;&nbsp;- Exit code non-zero → read error, STOP, show user what's required

    If blocked: Copy FSM error to user, explain required action, STOP execution.  
    &nbsp;&nbsp;- Ledger auto-synced  
    &nbsp;&nbsp;- After init, `.beads/fsm-state.json` exists and state is EXECUTE

4. **Context Isolation:** **Never** read frozen phases – use `XX-SUMMARY.md` instead.

5. **Execute Tasks:** Complete tasks in order. One atomic commit per logical change.  
    &nbsp;&nbsp;- **CRITICAL:** Execute Edit operations **sequentially**, never in parallel (prevent UI hangs)  
    &nbsp;&nbsp;- Multiple edits on the same file **must** be sequential (wait for first to complete before the second)  
    &nbsp;&nbsp;- Parallel tool calls are allowed only for independent Read/Grep operations

6. **Verify (auto-transitions to COMPLETE):** Execute silently. Report: "✅ Verified" or "❌ Failed"  
    &nbsp;&nbsp;- Runs verification command  
    &nbsp;&nbsp;- On success: auto-transitions to COMPLETE, marks bead [x] in ledger, queues next bead  
    &nbsp;&nbsp;- On failure: retry logic (circuit breaker after 3 attempts)

7. **Freeze:** When phase completes, add detailed files to `.claudeignore`

---

## Spike Bead Protocol (Exploration Mode)

**Spike beads** are time-boxed explorations that produce findings, not production code.

### When to Use Spikes

- Evaluating new libraries/APIs before committing
- Investigating feasibility of an approach
- Debugging complex issues with unclear root cause
- Prototyping to inform architecture decisions

### Spike Execution Flow

1. **Init** – Same as implementation beads (auto-transitions to EXECUTE)
2. **Explore** – Time-boxed investigation (1-3 hours max)
3. **Document Finding** – Create finding document (`.planning/spikes/SPIKE-XX-YY-topic.md`)
4. **Complete** – Direct transition from EXECUTE to COMPLETE (no verification step)

```bash
# Spike workflow
fsm.py init spike-06-05 --active-model sonnet --bead <path>
# [do exploration work]
# [create finding document]
fsm.py transition complete  # No verify step for spikes
```

**Spike Characteristics**

| Attribute         | Implementation Bead    | Spike Bead                        |
|-------------------|-----------------------|------------------------------------|
| Type              | implementation        | spike                              |
| Verification      | Required              | None (verification_tier: NONE)     |
| Time limit        | Until done            | 1-3 hours (time-boxed)             |
| Output            | Production code       | Finding document                   |
| Failure allowed   | No (circuit breaker)  | Yes (learning is valuable)         |
| Commit required   | Yes                   | Optional (finding is deliverable)  |

**Finding Document Template**

See `.beads/templates/spike-bead.md` for full template. Key sections:
- Question — What are we trying to learn?
- Outcome — ✅ Works / ❌ Doesn't work / ⚠️ Blocked / ❓ Inconclusive
- Evidence — Observations, test results, error messages
- Recommendation — Next steps based on outcome

---

## Next-In-Line Protocol (AUTOMATED)

Beads are automatically queued by `fsm.py` to eliminate workflow friction.

When you read the ledger:
1. If Active Bead shows Bead-XX-YY: **PENDING** → Immediately proceed with execution (step 3)
2. If Active Bead shows None with "Next Actions" → Tell user to choose an option (plan next phase, transition, etc.)
3. If Active Bead shows None with no pending beads → Phase/project complete, suggest transition or congratulate

**Auto-queue behavior:**
- When a bead completes (via `fsm.py verify` success), next pending bead is automatically set as Active
- Eliminates the extra "suggest → confirm → execute" round-trip
- User runs `/clear` + `/beads:run` and agent immediately starts next bead

**CRITICAL:** No user confirmation needed if Active Bead is already set to PENDING.

**Phase Completion Detection:**  
When last bead in a phase completes, FSM will display:  
🎉🎉🎉 PHASE XX COMPLETE! 🎉🎉🎉

✅ All beads verified and committed  
📦 Phase ready to freeze

➡️   REQUIRED NEXT STEP: `/beads:close-phase`

⚠️   **Do not** proceed to next phase without freezing!

**Phase Boundary Protection (Phase Guard):**
- Cannot execute Phase N+1 if Phase N is not CLOSED in ledger
- Cannot execute Phase N if bead files don't exist in `.planning/phases/XX-*/`
- FSM will BLOCK execution with a clear error message

---

## Verification Tiers (Honest Testing)

**Philosophy:** Don’t fake verification. Choose the appropriate tier for your bead.

| Tier   | When                       | How                                                 |
|--------|----------------------------|-----------------------------------------------------|
| AUTO   | Automated tests exist      | FSM runs verification_cmd (pytest, mypy, ruff)      |
| MANUAL | Human verification needed  | Agent confirms checklist items (hardware, visual)   |
| NONE   | Exploratory work           | No verification (spike beads, research)             |

**Examples:**

_Auto tier (default) – automated test command:_
```yaml
verification_tier: AUTO
verification_cmd: "pytest tests/test_foo.py -v"
```

_Manual tier – checklist confirmation:_
```yaml
verification_tier: MANUAL
verification_checklist:
  - [ ] Dashboard displays correctly in browser
  - [ ] User clicks filter button and chart updates
  - [ ] Data refreshes automatically every 30 seconds
```

_None tier – no verification:_
```yaml
verification_tier: NONE
rationale: "Spike bead – produces finding document, not verified code"
```

> See `.beads/VERIFICATION-TIERS.md` for full documentation and examples.

---

## Model Guard (IRON LOCK) — ENFORCED

The `--active-model` flag in `fsm.py init` is an enforced hard lock:

```bash
# Execute silently. If this exits 1, NO state is created.
python3 .beads/bin/fsm.py init 04-01 \
  --active-model opus \
  --bead .planning/phases/04-server-voice-loop/beads/04-01-ipc-foundation.md
```

- Exit 0: Report "✅ Model guard passed" and continue
- Exit 1: STOP IMMEDIATELY. Report: "❌ IRON LOCK: Bead requires [X], running [Y]"

---

## Silent FSM Protocol

- **Execute FSM commands silently.** Report outcomes **only**; never the commands themselves.

**Step:** Init  
Command (silent): `fsm.py init <id> --active-model <m> --bead <path>`  
User sees: "✅ Initialized & ready"  
────────────────────────────────────────  
**Step:** Verify  
Command (silent): `fsm.py verify "<cmd>"` (auto-prefixes `uv run` if needed)  
User sees: "✅ Verified" or "❌ Verification failed (attempt N/3)"

_Simplified workflow (reduced ceremony):_
- `init` auto-transitions to EXECUTE (no manual transitions)
- `verify` auto-transitions to COMPLETE on success
- All manual transitions removed from normal workflow

**Auto-sync:** Ledger is auto-synced after init and verify. No manual sync step needed.

**Auto-prefix:** `fsm.py verify` auto-adds `uv run` for Python commands if missing (prevents environment errors).

---

## Actions Requiring Rationale

**Philosophy:** Strong conventions, not rigid rules. Deviations are allowed **if** rationale is documented.

**Hard Locks – No Exceptions**  
Enforced by FSM and hooks; cannot be bypassed:
- 🔒 Modify framework files directly — **STATE GUARD** (Edit/Write/Bash blocked)
- 🔒 Skip model guard — **IRON LOCK** (--active-model must match)
- 🔒 Execute next phase without closing previous — **Phase Guard** (prior phase must be CLOSED)
- 🔒 Execute unplanned phase — **Phase Guard** (bead files must exist)

**Actions Requiring Documented Rationale**  
Avoid by default; exception allowed if rationale is documented:

- ⚠️  Manual ledger edit — e.g., "Emergency architecture pivot," "Fixing FSM sync bug"
- ⚠️  Manual `fsm-state.json` edit — e.g., "Recovering from corrupted state"
- ⚠️  Reading frozen phase files — e.g., "Debugging regression," "Understanding legacy design"
- ⚠️  Skipping verification — e.g., "Spike bead exploration," "Manual testing only"
- ⚠️  Announcing FSM commands — e.g., "Debugging workflow," "Teaching protocol"

**How to Document Rationale**

_In bead metadata:_
```yaml
<meta>
verification_tier: NONE
rationale: "Spike bead – exploratory work, produces finding not code"
```

_In ledger session notes:_
```
## Session Notes
- Manual ledger edit authorized: 2026-01-21
  Rationale: Architecture pivot from RPi5+UDP to Cloud VPS+WebSocket
  Required updating Phase 5 description and bead list
```

_In commit messages:_
```
docs: manual ledger sync after cloud pivot

Rationale: Emergency architecture change required updating
active phase description. FSM sync would not capture
the scope of changes needed.
```

---

## Failure Handling (Circuit Breaker)

- **Attempt 1:** Soft retry – self-correction, same approach
- **Attempt 2:** Hard rollback – `git reset --hard [initial_sha]` + strategic pivot
- **Attempt 3:** Circuit breaker — STOP and request human intervention

---

## Token Efficiency Rules

- **Read** `.beads/ledger.md` for context (NOT full conversation history)
- **Read ONLY** active bead + files in `<context_files>` section
- **Never read** `.claudeignore` files (frozen phases)
- **Discard** internal reasoning after bead completion
- **Summarize** outcomes in ≤3 sentences for the ledger

---

## Research Protocol

When starting research, **always** use `.beads/templates/research-schema.md` as blueprint.

**Research files (`XX-RESEARCH.md`) must follow strict XML-anchored structure:**
- `<research_meta>` — Topic, model, date, phase
- `<objective>` — Single sentence question to answer
- `<constraints>` — YAML listing performance/compatibility/resource limits
- `<pattern>` — Technical patterns with tradeoff tables + verification
- `<alternatives>` — Concrete options with quantified comparisons
- `<verify_cmd>` — Deterministic command proving findings

**Prohibited:** Narrative fluff, subjective language, unquantified claims  
**Required:** Technical specs, verification commands, tradeoff analysis

See `.planning/framework/V2-SPEC.md` for reference.

---

## Model Routing

| Task Type              | Model  | Rationale                                         |
|------------------------|--------|---------------------------------------------------|
| Architecture/Planning  | Opus   | Superior long-horizon reasoning                   |
| Research               | Opus   | Deep analysis, SOTA exploration                   |
| Implementation         | Sonnet | Best code quality + speed/cost balance            |
| Verification           | Sonnet | Fast feedback loops                               |
| Summarization          | Haiku  | Cheap, fast, sufficient for context compression   |

---

## File Priority (Read Order)

**When starting execution (before `init`):**
1. `.beads/ledger.md` — Current project state (check "Active Bead" section)
2. **Do not** read `.beads/fsm-state.json` (doesn’t exist between beads)

**During bead execution (after `init`):**
1. `.beads/fsm-state.json` — Runtime state (retry count, verification status)
2. Active bead file – `XX-YY-name.md`
3. `XX-SUMMARY.md` files – Frozen phase context
4. `XX-RESEARCH.md` — If referenced in bead
5. Source files — Only those in bead's `<context_files>`

**Never read:** Files in `.claudeignore`, completed beads from frozen phases, or other phases’ PLAN/CONTEXT files.

---

## State Management (Single Source of Truth)

**Authoritative Sources:**
- Runtime: `.beads/fsm-state.json` — Current bead, state, retry count (exists only during active bead)
- History: `.beads/ledger.md` — Completed work (`[x]` = done, `[ ]` = pending) + active bead
- Templates: `.planning/phases/XX-*/beads/XX-YY-*.md` — Task specs (static)

**FSM State File Lifecycle:**
- Does **not** exist between beads (clean slate)
- Created by `fsm.py init` when bead starts
- Updated during execution (transition, verify)
- Deleted by `fsm.py transition complete` when bead finishes
- If missing at execution start: normal (check ledger "Active Bead" section)

**State Flow:**

```
[Bead Template] → FSM init → [fsm-state.json] → FSM sync-ledger → [ledger.md]
    (static)        (runtime)                   (history)
```

**Critical Rules:**
1. Bead files are templates – they **never** change during execution
2. `fsm-state.json` owns current execution state
3. Ledger is write-only from FSM (**no manual edits**)
4. Ledger checkboxes (`[x]` / `[ ]`) are authoritative for completion status
5. Phase-level `@status()` annotations are metadata (human-readable, not used by FSM)
6. **Only** list beads in ledger **after** bead files exist – Never list planned beads before files are created

**How State Is Synchronized:**
- `FSM init`: Creates `fsm-state.json`, extracts model and verification_cmd from bead file
- `FSM verify`: Updates `last_verification_passed` flag in `fsm-state.json`
- `FSM transition complete`: Marks bead as `[x]` in ledger, clears active bead
- `FSM sync-ledger`: Writes FSM state to ledger’s "Active Bead" section

**What’s NOT synchronized:**
- Bead file `<meta>` sections don’t contain runtime state (status field removed)
- Phase `@status()` annotations are decorative (manually updated during `/transition`)
- Cost estimates are approximations, not tracked by FSM

---