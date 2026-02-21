# Plan Phase Into Beads

Decompose a phase into atomic, model-optimized beads.

**Usage:** `/beads:plan-phase XX`

**Why Decomposition Matters:** A phase is too large for a single context window to hold reliably. Decomposing into beads creates atomic units where the model can focus deeply, verify independently, and recover from failure without losing prior work. Each bead carries its own intent and pitfalls — the executor never has to guess WHY a task exists or what traps to avoid.

---

## Execution Protocol

### Step 0: Check Previous Phase is Closed (MANDATORY)

Run this FIRST before doing anything else:

```bash
python3 .beads/bin/fsm.py check-phase-closed XX
```

Where `XX` is the phase number you're planning (e.g. `02` for Phase 02).

If it exits with an error — STOP. Tell the user to run `/beads:close-phase` first.

### Step 0b: Phase 01 Guidance (if planning Phase 01)

**If `XX` is `01`, apply these constraints throughout decomposition:**

- **Fewer beads** — 1-3 instead of 3-7. Speed over thoroughness.
- **Minimal code** — just enough to prove the core function works. No project structure, config scaffolding, or error handling beyond what's needed to run the proof-of-concept.
- **Verification tests the IDEA** — "does the concept work?" not "is the code clean?" Verification commands should prove the core function delivers its intended value.
- **Skip infrastructure** — no logging setup, no CI, no deployment config, no abstractions. The "paperboard engine" principle: prove it runs before building it properly.
- **Model: sonnet** — Phase 01 is execution, not architecture. Sonnet is the right tool.

These constraints do NOT apply to Phase 02+. Later phases use standard decomposition rules.

### Step 1: Read Phase Context

Use the Read tool to read:
1. `.planning/phases/XX-*/XX-OVERVIEW.md` — phase goal and deliverables
2. `.beads/ledger.json` — project context and global stack
3. `CLAUDE.md` — any project-specific constraints

### Step 2: Decompose Into Beads

Create 3-7 atomic beads. Each bead must be:
- Completable in 30min–2hrs
- Have a single clear deliverable
- Have a verifiable outcome (test, command, or manual check)

**Bead file location:** `.planning/phases/XX-phase-name/beads/XX-YY-bead-name.md`

**Bead file format** (must match `.beads/templates/bead.md` structure):
```markdown
# Bead XX-YY: [Concise Action Title]

<meta>
```yaml
id: XX-YY-short-name
phase: XX-phase-name
model: sonnet
verification_tier: AUTO
verification_cmd: "command that exits 0 on success"
depends_on: []
```
</meta>

---

<intent>
**Goal**: [Single sentence — what must be accomplished]

**Why**: [Business or architectural reason — what breaks or stalls without this]

**Success Criteria**:
- [ ] [Specific, measurable outcome]
- [ ] [Specific, measurable outcome]
- [ ] Verification command passes
</intent>

---

<context_files>
```yaml
mandatory:
  - .beads/ledger.json
  - [path/to/implementation/target]

reference:
  - .planning/DECISIONS.md
  - [XX-SUMMARY.md or XX-RESEARCH.md if applicable]
```
</context_files>

---

<pitfalls>
- [Risk #1 — what could go wrong and why]
- [Risk #2 — common wrong assumption]
</pitfalls>

---

<tasks>
Execute sequentially. Each step is atomic.

### 1. [Action Verb + Target]
- **What**: [Concise description]
- **Verify**: `[quick check command]`

### 2. [Action Verb + Target]
- **What**: [Concise description]
- **Verify**: `[quick check command]`

### 3. Commit
- **Message**: `[type](XX-YY): [description]`
- **Files**: [list changed files]
</tasks>

---

<verification>
**Tier**: AUTO
**Command**:
```bash
[verification command]
```
**Expected**: [what success looks like]
</verification>
```

**Model selection:**
- `haiku` — config files, boilerplate, simple edits
- `sonnet` — most implementation work (default)
- `opus` — complex algorithms, architecture decisions

### Step 3: Initialize First Bead

After writing all bead files, initialize the first bead with the FSM:

```bash
python3 .beads/bin/fsm.py init XX-YY \
  --active-model sonnet \
  --bead .planning/phases/XX-phase-name/beads/XX-01-bead-name.md
```

If this fails with "Git repository not initialized", run:
```bash
git init && git add . && git commit -m "chore: initial commit"
```
Then retry the `fsm.py init` command.

**Do NOT call `register-phase`, `sync-ledger`, or any other FSM command here.** Only `fsm.py init` is needed.

### Step 4: Update OVERVIEW.md

Update the phase OVERVIEW.md to fill in deliverables and list the beads:

```markdown
## Deliverables
- [concrete output from bead 1]
- [concrete output from bead 2]

## Beads
- [ ] XX-01: [title]
- [ ] XX-02: [title]
```

### Step 5: Report

Print summary:
```
Phase XX decomposed — N beads created

  Bead XX-01 : [title] (sonnet, AUTO verification)
  Bead XX-02 : [title] (sonnet, AUTO verification)
  ...

  Active: XX-01 — ready to execute
  Next: Run `/beads:run` to start the first bead
```

---

## Important Rules

- **NEVER call `fsm.py register-phase`** — this command does not exist
- **NEVER call `fsm.py sync-ledger`** — requires an active bead, not needed here
- **NEVER skip `fsm.py init`** — it registers the bead and enables rollback
- **ONLY call `fsm.py init`** for the first bead in the phase; remaining beads are queued automatically

---

**Related commands:**
- `/beads:research` — Research technical approach before planning
- `/beads:run` — Execute beads after planning
- `/beads:plan-project` — Generate full phase roadmap first
