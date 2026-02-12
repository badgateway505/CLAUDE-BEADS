# Verification Tiers - Honest Testing

**Problem:** "echo" verification pretends to test but doesn't. This system replaces fake checks with honest tiering.

---

## The Three Tiers

| Tier | When | How | Example |
|------|------|-----|---------|
| **AUTO** | Automated tests exist | Run test command | `pytest tests/test_foo.py -v` |
| **MANUAL** | Human verification needed | Agent confirms checklist | Hardware tests, visual checks |
| **NONE** | Exploratory work | No verification | Spike beads, research |

---

## AUTO Tier (Automated Testing)

**Use when:** You have automated tests (pytest, mypy, ruff, etc.)

**Bead metadata:**
```yaml
verification_tier: AUTO
verification_cmd: "pytest tests/test_feature.py -v --cov=src/app/module"
```

**Verification process:**
1. FSM runs `verification_cmd` via subprocess
2. Exit code 0 = pass, non-zero = fail
3. Agent reports results (no human confirmation needed)

**Best for:**
- Unit tests
- Integration tests
- Linting (ruff check)
- Type checking (mypy)
- Code coverage

**Example:**
```bash
# FSM automatically runs:
uv run pytest tests/test_voice_loop.py -v

# Output:
✓ Verification PASSED
✓ Transition: verify -> complete
```

---

## MANUAL Tier (Checklist Verification)

**Use when:** Verification requires human observation or hardware

**Bead metadata:**
```yaml
verification_tier: MANUAL
verification_checklist:
  - [ ] Dashboard displays correctly on page load
  - [ ] Clicking filter button updates chart data
  - [ ] Data refreshes every 30 seconds
  - [ ] No errors in browser console
```

**Verification process:**
1. Agent reads checklist from bead metadata
2. Agent asks user to confirm each item OR
3. Agent reviews evidence (screenshots, logs) and confirms
4. All items checked = verification passes

**Best for:**
- Hardware tests (LED blinks, buzzer sounds)
- Visual checks (UI displays correctly)
- Manual testing workflows
- Integration with physical devices

**Example workflow:**
```
Agent: "Please verify the following checklist:"
Agent: "1. Dashboard displays correctly on page load - can you confirm?"
User: "Yes, all widgets render properly"
Agent: "✓ Item 1 confirmed"
Agent: "2. Clicking filter button updates chart data - can you confirm?"
User: "Yes, chart updates with filtered data"
Agent: "✓ Item 2 confirmed"
... (continues for all items)
Agent: "✓ All checklist items confirmed - marking verification passed"
```

**Alternative (evidence-based):**
```
Agent: "I see from the serial console log you provided:"
Agent: "- Boot message: 'READY' displayed"
Agent: "- Button A press triggers state change to RECORDING"
Agent: "- Audio output confirmed via waveform"
Agent: "✓ Manual verification complete based on evidence"
```

---

## NONE Tier (No Verification)

**Use when:** Verification doesn't make sense (exploration, research)

**Bead metadata:**
```yaml
verification_tier: NONE
rationale: "Spike bead - produces finding document, not verified code"
```

**Verification process:**
1. No verification command run
2. No checklist confirmation
3. Agent can transition directly to COMPLETE after work is done

**Best for:**
- Spike beads (time-boxed exploration)
- Research beads (produces finding, not code)
- Documentation-only beads (where "verification" is just reading)

**Example:**
```bash
# No verification needed:
fsm.py transition complete
# ✓ Verification tier NONE - skipping verification requirement
# ✓ Transition: execute -> complete
```

---

## Migration Guide

### Before (Fake Verification)
```yaml
verification_cmd: "echo 'Hardware tested manually'"  # ❌ Dishonest
```

### After (Honest Tiering)
```yaml
verification_tier: MANUAL
verification_checklist:
  - [ ] Hardware tested: Boot sequence works
  - [ ] Hardware tested: Button triggers expected action
```

---

## Common Patterns

### Pattern 1: Unit Tests (AUTO)
```yaml
verification_tier: AUTO
verification_cmd: "pytest tests/test_module.py -v"
```

### Pattern 2: Hardware + Software (MANUAL)
```yaml
verification_tier: MANUAL
verification_checklist:
  - [ ] Code: Unit tests pass (pytest tests/test_api.py)
  - [ ] Server: API endpoint responds correctly
  - [ ] Integration: WebSocket connection established
```

### Pattern 3: Documentation Changes (NONE with Rationale)
```yaml
verification_tier: NONE
rationale: "Documentation-only bead - verification is review of clarity and completeness"
```

### Pattern 4: Spike Investigation (NONE)
```yaml
type: spike
verification_tier: NONE  # Auto-set for spike beads
finding_file: .planning/spikes/SPIKE-XX-YY-topic.md
```

---

## FAQ

**Q: Can I mix tiers in one bead?**
A: No. Choose the most appropriate tier. If you have both automated tests AND manual checks, use MANUAL and include the automated test in the checklist.

**Q: What if I have no tests yet?**
A: Use MANUAL tier and add "Write automated tests" as a TODO. Don't fake it with AUTO tier.

**Q: Can verification_tier change during execution?**
A: No. It's set in bead metadata before execution starts. If you realize the tier is wrong, update the bead file and note the change in session notes.

**Q: Do MANUAL checks require user interaction every time?**
A: Not necessarily. The agent can review evidence (logs, screenshots, test results) and confirm the checklist. Human interaction is only needed when evidence is unclear.

**Q: What's the difference between NONE tier and spike beads?**
A: Spike beads automatically get NONE tier. But you can also use NONE tier for implementation beads when verification doesn't apply (e.g., pure documentation changes).

---

## See Also

- `.beads/templates/examples/bead-AUTO-example.md` - Automated test verification
- `.beads/templates/examples/bead-MANUAL-example.md` - Hardware checklist verification
- `.beads/templates/examples/bead-NONE-example.md` - Spike bead (no verification)
