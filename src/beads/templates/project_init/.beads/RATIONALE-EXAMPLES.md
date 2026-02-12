# Rationale Examples

**Philosophy:** Strong conventions, not rigid rules. Document your reasoning when deviating.

## When Rationale is Required

Any deviation from standard protocol should include a brief rationale explaining why it's necessary.

---

## Example 1: Spike Bead (No Verification)

**Standard:** All beads require verification command
**Deviation:** Spike bead with `verification_tier: NONE`

```yaml
<meta>
id: spike-06-05-pdm-firmware-test
type: spike
verification_tier: NONE
rationale: "Time-boxed exploration to determine if PDM firmware resolves I2S audio issue. Output is finding document, not production code."
```

---

## Example 2: Manual Ledger Edit

**Standard:** Ledger only modified via FSM sync
**Deviation:** Manual edit to ledger.md

**Ledger session notes:**
```markdown
## Session Notes
- Manual ledger edit authorized: 2026-01-21
  Rationale: Architecture pivot from RPi5+UDP to Cloud VPS+WebSocket
  Required updating Phase 5 description and renaming beads.
  FSM sync handles individual bead status, not phase-level refactoring.
```

---

## Example 3: Reading Frozen Phase

**Standard:** Use XX-SUMMARY.md for frozen phases
**Deviation:** Reading detailed files from .claudeignore phase

```markdown
## Bead Notes
Reading frozen Phase 2 implementation files (normally .claudeignore)

Rationale: Debugging regression in Phase 6C audio output. Need to
understand original I2S configuration from Phase 2 implementation
to identify what changed. SUMMARY.md doesn't include I2S timing details.
```

---

## Example 4: Skipping Model Guard

**Standard:** Bead specifies model, must match active model
**Deviation:** Running Sonnet bead with Haiku (NOT RECOMMENDED)

**Note:** Model guard is IRON LOCK - cannot be bypassed via FSM.
Would require manual fsm-state.json edit.

```yaml
# This would require documented rationale:
rationale: "Emergency production hotfix. Opus unavailable due to API outage.
Haiku acceptable for simple variable rename in config file.
Full verification tests still required."
```

**Better approach:** Update bead metadata to accept multiple models or mark as haiku-compatible.

---

## Example 5: Extended Time Box for Spike

**Standard:** Spike beads are 1-3 hours
**Deviation:** 4-hour spike for complex investigation

```yaml
<meta>
type: spike
time_box: 4 hours
rationale: "Complex database performance investigation requires:
- Profiling slow queries (1 hour)
- Index optimization analysis (1.5 hours)
- Alternative database engine evaluation (1.5 hours)
Standard 3-hour limit insufficient for thorough investigation."
```

---

## Example 6: No Commit for Implementation Bead

**Standard:** Implementation beads commit working code
**Deviation:** Bead produces only documentation changes

```yaml
<meta>
verification_cmd: "echo 'Documentation updated'"
rationale: "Bead updates CLAUDE.md and PROTOCOL.md based on lessons
learned from Phase 6. No code changes. Verification confirms
documentation is readable and complete."
```

---

## Anti-Patterns (DON'T DO THIS)

### ❌ Weak Rationale
```yaml
rationale: "Just testing" # Too vague
rationale: "Quick fix" # Doesn't explain why
rationale: "Temporary" # Everything is temporary
```

### ✅ Strong Rationale
```yaml
rationale: "Testing spike bead workflow before documenting in PROTOCOL.md"
rationale: "Emergency hotfix for production audio bug - bypassing normal verification to deploy within 1-hour SLA"
rationale: "Temporary workaround until M5Stack releases fixed I2S driver (expected v1.13)"
```

---

## When NOT to Use Rationale

**Hard locks cannot be bypassed** (even with rationale):
- Executing bead without `/clear` (HARD LOCK)
- Model mismatch when FSM enforces model guard (IRON LOCK)

These are enforced by FSM code and require code changes to bypass, not just rationale documentation.

---

## Summary

**Rationale is not permission to break rules carelessly.**

It's acknowledgment that:
1. Context matters
2. Emergencies happen
3. Learning requires experimentation
4. One size doesn't fit all situations

Document your reasoning so future you (or others) understand the tradeoffs made.
