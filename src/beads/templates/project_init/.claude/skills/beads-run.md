# Run Active Bead

Execute the currently active bead from the ledger.

**Usage:** `/beads:run`

**Tip:** Run `/clear` before each bead for optimal token efficiency (not enforced).

**What it does:**
1. Reads `.beads/ledger.json` for active bead
2. Runs FSM init (validates model, dependencies)
3. Executes bead tasks
4. Runs FSM verify (tests/checklist per verification tier)
5. Commits atomically

**FSM Commands:**
```bash
# Initialize (model guard enforced, dependencies checked)
python3 .beads/bin/fsm.py init <bead-id> --active-model <model> --bead <path>

# After completing tasks, verify
python3 .beads/bin/fsm.py verify "<verification_cmd>"
```

**If FSM blocks you:** STOP. Show user the error. Do not attempt to bypass.
The BEADS State Guard prevents direct manipulation of framework files.

**Related:** `/beads:plan`, `/beads:resume`
