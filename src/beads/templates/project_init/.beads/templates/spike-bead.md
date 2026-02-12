# Spike XX-YY: [Question to Answer]

<meta>
```yaml
id: spike-XX-YY-[slug]
type: spike
phase: [XX-phase-name]
model: [opus | sonnet | haiku]
time_box: [1-3 hours]
verification_tier: NONE
rationale: "Spike bead - time-boxed exploration to answer specific question"
finding_file: .planning/spikes/SPIKE-XX-YY-[topic].md
depends_on: []
```
</meta>

---

<objective>
**Question**: [Single clear question to answer]

**Possible Outcomes**:
- ✅ Works - [what success looks like]
- ❌ Doesn't work - [what failure looks like]
- ⚠️ Blocked - [what blockers look like]
- ❓ Inconclusive - [when we can't determine]
</objective>

---

<context_files>
```yaml
mandatory:
  - .beads/ledger.md
  - [relevant source/config files to examine]

reference:
  - [XX-RESEARCH.md]  # If applicable
  - [XX-SUMMARY.md]   # Frozen phase context
```
</context_files>

---

<exploration_plan>
Execute in time-boxed manner. Abort if blocked or time exceeds limit.

### 1. Setup/Prerequisites
- **What**: [Environment setup, dependencies, etc.]
- **Check**: [How to verify setup is ready]

### 2. Experiment
- **What**: [Core experiment/test to run]
- **Check**: [How to evaluate result]

### 3. Document Finding
- **What**: Write finding to `finding_file`
- **Include**: Outcome, evidence, recommendation
</exploration_plan>

---

<finding_template>
Create file at path specified in `finding_file`:

```markdown
# Spike Finding: [Topic]

**Date**: YYYY-MM-DD
**Bead**: spike-XX-YY
**Time Spent**: [actual time]

## Question
[Restate the question from objective]

## Outcome
**Result**: [✅ Works | ❌ Doesn't work | ⚠️ Blocked | ❓ Inconclusive]

## Evidence
[Specific observations, test results, error messages, etc.]

## Analysis
[Why did we get this result? What does it mean?]

## Recommendation
- **If Works**: [Next steps - create implementation bead?]
- **If Doesn't Work**: [Alternative approaches to consider]
- **If Blocked**: [What needs to be resolved first]
- **If Inconclusive**: [What additional information is needed]

## Code Artifacts
[Any test code, config snippets, or proof-of-concept code created during spike]
```
</finding_template>

---

<notes>
**Spike beads differ from implementation beads:**
- No production code requirement
- No verification command (tier: NONE)
- Output is knowledge, not working software
- Failure is acceptable (learning what doesn't work is valuable)
- Time-boxed to prevent over-investigation
- Finding document is the deliverable

**When to use spikes:**
- Evaluating new libraries/APIs before committing
- Investigating feasibility of an approach
- Debugging complex issues where root cause is unclear
- Prototyping to inform architecture decisions
</notes>
