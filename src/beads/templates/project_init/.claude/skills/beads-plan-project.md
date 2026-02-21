# Plan Project Roadmap

Generate a validation-first phase roadmap: prove the core idea works before investing in architecture.

**Usage:** `/beads:plan-project`

**Why This Matters:** Most project ideas don't survive contact with reality. Building foundations before validating the core function wastes tokens and time. This skill structures work so the riskiest assumption — "does the core idea actually work?" — gets tested first.

**What it does:**
This skill reads `.planning/PROJECT.md`, runs an honest evaluation dialogue with the user, and creates a phase roadmap ordered by validation priority: core function first, user-facing features next, infrastructure last. It does NOT decompose phases into beads (that's `/beads:plan-phase XX`).

---

## Execution Protocol

### Step 0: Validate Project (MANDATORY)

Run this FIRST — the hook will block all phase writes without it:

```bash
python3 .beads/bin/fsm.py validate-project
```

This validates PROJECT.md has real content and unlocks `.planning/phases/` for writing.
If it fails, fix PROJECT.md before proceeding.

### Step 1: Read Context

Use the **Read tool** (not bash cat) to read these files:
1. `.planning/PROJECT.md` — vision and goals from `beads init`
2. `.beads/ledger.json` — current state
3. `CLAUDE.md` — any existing project context

**Key check:** Does PROJECT.md have a `## Current State` section?
- **YES** → Existing project. Only plan phases for remaining work.
- **NO** → New project. Plan everything from scratch.

### Step 2: Understand the Idea

Go one topic at a time. Wait for the user's response before moving on.

**1. Core function**
Identify THE one thing this app does. Strip everything else away.
> "Based on your description, the core function is:
> [one sentence — the essential thing the app does]
>
> If we could only build ONE thing to test whether this idea works, it would be:
> [the minimal proof-of-concept]
>
> **1** — That's it exactly
> **2** — Adjust: [correct me]"

Wait for reply.

**2. Why it's worth building**
Ask the user to articulate the value. This forces clarity and gives you context for the evaluation.
> "Help me understand the value:
> - **Who needs this?** (what kind of person, in what situation?)
> - **Why would they use YOUR version?** (what's different from doing it manually or using something that exists?)
>
> Just a few sentences is fine."

Wait for reply.

### Step 3: Honest Evaluation

Be objective — not a cheerleader, not a critic. The goal is to see the idea clearly so the user can make an informed decision.

Present a brief, honest assessment covering:

1. **What's strong** — genuine advantages of this idea (unique angle, underserved audience, technical feasibility)
2. **What already exists** — known competitors or alternatives. Be specific (name tools, apps, libraries). If nothing close exists, say so.
3. **Real challenges** — technical difficulty, market saturation, maintenance burden, or fundamental limitations. Not hypothetical fears — concrete issues.
4. **Verdict** — one sentence: is this worth a Phase 01 prototype? Almost always yes — the point of Phase 01 is to find out cheaply.

> "Here's my honest take:
> [assessment]
>
> **1** — Makes sense, let's build the prototype
> **2** — I want to discuss: [concerns]
> **3** — Kill it, not worth pursuing"

If the user picks **3**, respect it. Print "Project shelved. No phases created." and stop.

Wait for reply, then proceed.

**4. Tech stack**
Only ask this after the idea survives evaluation. Recommend the simplest stack that can prove the core function:
> "For the prototype, I'd use:
> - [tool/library] for [purpose]
> - [tool/library] for [purpose]
>
> This is the minimum to prove the core function. We can upgrade later if the idea validates.
>
> **1** — Works for me
> **2** — Use a different stack: [describe]"

Wait for reply.

**5. Constraints** (optional, ask only if relevant)
> "Any hard constraints I should know about?
> (e.g. must use specific language, budget limits, deployment target)
>
> **1** — None
> **2** — Yes: [describe]"

Wait for reply, then proceed to Step 4.

### Step 4: Generate Phase Roadmap

Create the phase roadmap following validation-first ordering.

**Phase ordering principle — core function first, polish last:**

```
Phase 01: Prove the core function (ALWAYS first)
  → Minimal code. Just the essential feature. "Paperboard car engine."
  → Ends with: does the core idea work? User evaluates.

Phase 02-N: User-facing features (ordered by what user can interact with)
  → Each phase adds something the user can see, touch, test.
  → No behind-the-scenes work until user-visible features are solid.

Phase N+1: Infrastructure & architecture
  → Error handling, proper structure, database, auth — only after features validate.

Phase N+2: Polish & deployment
  → Optimization, UI refinement, deployment — only when we're sure this project lives.
```

**For existing projects (has `## Current State`):**
- Mark already-built features as `Complete` phases
- Only create `Pending` phases for remaining work
- Phase numbering continues from where the project is

**Rules (both cases):**
- Phase 01 is ALWAYS the core function proof-of-concept — even for existing projects, if the core hasn't been validated yet
- Each phase should be 3-10 beads worth of work (roughly 1-3 days)
- Be specific to this project — no generic "Setup" or "Testing" phases
- User-facing features come before infrastructure in phase ordering
- Include a natural evaluation point after Phase 01

**Phase format:**
```
Phase XX: [Name]
Goal: [One clear sentence — what this phase delivers]
Status: ✅ Complete | ⏳ Pending
```

### Step 5: Confirm with User

Present the roadmap and ask:
> "Does this look right? Any phases missing, out of order, or that should be split/merged?
>
> **1** — Looks good, create the phases
> **2** — Adjust: [describe changes]"

Wait for approval before writing.

### Step 6: Create Phase Directories

For each phase, create:
```
.planning/phases/XX-phase-name/
  XX-OVERVIEW.md
```

Each OVERVIEW.md contains:
```markdown
# Phase XX: [Name]

## Goal
[One sentence from roadmap]

## Deliverables
- [TODO — filled during /beads:plan-phase XX]

## Dependencies
- [Previous phase if applicable]

## Status
Pending
```

### Step 7: Update PROJECT.md

Update `.planning/PROJECT.md` with the confirmed info from the dialogue:
- Fill in `## Goals / MVP Target` with the confirmed goals
- Add `## Core Function` section — the one thing being validated
- Add `## Value Proposition` section — who needs it, why this version
- Add `## Tech Stack` section with the confirmed stack
- Add `## Constraints` section if any were specified

Use the Write tool to update the file. This is the source of truth for planning.

### Step 7b: Record Decisions

Append every tech stack and architectural choice from the dialogue to `.planning/DECISIONS.md`.

Each row captures WHY the choice was made plus what was rejected:

```markdown
| FastAPI for server | Native WebSocket + async; simpler VPS deploy than Django Channels | 01 | Django Channels, Flask |
| uv for packages | Single tool, faster than pip/poetry | 01 | pip, poetry |
```

This file persists across all phases. Future beads reference it before making architectural choices.

### Step 8: Cleanup and Report

Remove the plan-ready flag (one-time use):
```bash
rm -f .beads/.plan-ready
```

Print summary using this exact format (wrap commands in backticks so they stand out):
```
Roadmap complete

  Project : {name}
  Core    : {core function in one line}
  Phases  : {complete} complete, {pending} pending
  Next    : Phase {first_pending} — {name}

  Next steps:
  1. Run `/beads:plan-phase {first_pending}` to decompose into beads
  2. Then run `/beads:run` to execute the first bead
```

---

## Important Rules

- **NEVER create bead files.** Phase decomposition into beads is done via `/beads:plan-phase XX`.
- **NEVER modify existing source code.** This is a planning-only skill.
- **NEVER skip user confirmation.** Always present the roadmap for approval before writing files.
- **NEVER call `fsm.py sync-ledger` here** — the FSM has no active bead at this stage. The ledger is populated when you run `/beads:plan-phase XX`.
- **NEVER skip the honest evaluation.** The user deserves an objective assessment before investing time.
- **DO update PROJECT.md** with all confirmed context from the dialogue.
- **DO mark already-completed work** as `Complete` if the project has existing code (check git log).
- **DO order phases by validation priority** — core function first, infrastructure later, polish last.

---

**When to use:**
- After `beads init` for new projects — to create the full phase plan
- When starting fresh and PROJECT.md has TODO placeholders
- When you want to re-plan the entire project roadmap

**Related commands:**
- `/beads:plan-phase XX` — Decompose a specific phase into atomic beads (run after this)
- `/beads:onboard` — For existing projects, scan codebase and analyze before planning
- `/beads:run` — Execute beads after planning
