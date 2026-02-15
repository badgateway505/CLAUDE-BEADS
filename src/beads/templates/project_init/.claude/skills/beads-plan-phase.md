# Plan Phase Into Beads

Decompose a phase into atomic, model-optimized beads.

**Usage:** `/beads:plan-phase XX`

---

## Execution Protocol

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

**Bead file format:**
```markdown
# Bead XX-YY: [Task title]

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

## Task

[Clear description of what to build]

## Acceptance Criteria

- [ ] [Specific, verifiable criterion]
- [ ] [Specific, verifiable criterion]

## Context Files

- `path/to/relevant/file`

## Notes

[Any implementation hints]
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
