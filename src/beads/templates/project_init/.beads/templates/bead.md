# Bead XX-YY: [Concise Action Title]

<meta>
```yaml
id: XX-YY-[slug]
phase: [XX-phase-name]
model: [opus | sonnet | haiku]
cost_estimate: [0.XX USD]
verification_tier: AUTO  # AUTO | MANUAL | NONE
verification_cmd: "pytest tests/test_foo.py -v"  # Required for AUTO tier
# verification_checklist:  # Required for MANUAL tier
#   - [ ] Feature renders correctly in browser
#   - [ ] User interaction works as expected
depends_on: []  # Optional: prerequisite bead IDs
# rationale: ""  # Optional: Document why this bead deviates from standard protocol
# NOTE: Status is NOT stored here. Runtime state lives in .beads/fsm-state.json
```
</meta>

---

<intent>
**Goal**: [Single sentence describing what must be accomplished]

**Success Criteria**:
- [ ] [Specific, measurable outcome #1]
- [ ] [Specific, measurable outcome #2]
- [ ] Verification command passes
</intent>

---

<context_files>
```yaml
mandatory:
  - .beads/ledger.md
  - [path/to/implementation/target.py]
  - [XX-RESEARCH.md]  # If applicable

reference:
  - [XX-SUMMARY.md]   # Frozen phase context
```
</context_files>

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
**Tier**: [AUTO | MANUAL | NONE]

---

### AUTO Tier (Automated Tests)
**Command**:
```bash
pytest tests/test_foo.py -v
```

**Expected**: All tests pass, coverage ≥80%

**On Failure**:
| Symptom | Fix |
|---------|-----|
| ImportError | Check module path, run `uv sync` |
| AssertionError | Review test expectations vs actual behavior |

---

### MANUAL Tier (Checklist Verification)
**Checklist** (agent confirms each item):
- [ ] Feature renders correctly in browser
- [ ] User interaction works as expected
- [ ] Data displays accurately
- [ ] No errors in console output

**How to Verify**: Run hardware, observe behavior, check off items

---

### NONE Tier (No Verification)
**Rationale**: Spike bead - exploratory work produces finding document, not verified code

**Completion Criteria**: Finding document created at `.planning/spikes/SPIKE-XX-YY-topic.md`
</verification>

---

<commit_template>
```
[type](XX-YY): [description]

[Optional body with bullet points]

Part of Phase XX: [Phase Name]
```
</commit_template>
