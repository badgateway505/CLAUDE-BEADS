#!/usr/bin/env python3
"""
Claude Beads Finite State Machine

Manages bead execution lifecycle with deterministic rollback.
States: DRAFT -> EXECUTE -> VERIFY -> COMPLETE/FAILED

Core responsibilities:
  - Track active bead
  - Enforce verification before completion
  - Auto-queue next pending bead
  - Circuit breaker retry strategy

Usage:
    python fsm.py init <bead_id> [--active-model MODEL] [--bead PATH]
    python fsm.py transition <state>
    python fsm.py verify <verification_cmd>
    python fsm.py rollback
    python fsm.py status
    python fsm.py sync-ledger
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


class State(Enum):
    """FSM states for bead execution."""
    DRAFT = "draft"
    EXECUTE = "execute"
    VERIFY = "verify"
    RECOVER = "recover"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class FSMContext:
    """Persistent FSM state."""
    bead_id: str
    current_state: str
    retry_count: int
    initial_commit_sha: str
    verification_cmd: Optional[str] = None
    model: Optional[str] = None
    last_verification_passed: bool = False
    bead_type: str = "implementation"  # "implementation" or "spike"
    verification_tier: str = "AUTO"  # "AUTO" | "MANUAL" | "NONE"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'FSMContext':
        filtered_data = {k: v for k, v in data.items() if not k.startswith('_')}
        if 'model' not in filtered_data:
            filtered_data['model'] = None
        if 'last_verification_passed' not in filtered_data:
            filtered_data['last_verification_passed'] = False
        if 'bead_type' not in filtered_data:
            filtered_data['bead_type'] = 'implementation'
        if 'verification_tier' not in filtered_data:
            # Auto-detect: spike beads default to NONE, others to AUTO
            filtered_data['verification_tier'] = 'NONE' if filtered_data.get('bead_type') == 'spike' else 'AUTO'
        return cls(**filtered_data)


class BeadFSM:
    """Finite State Machine for atomic bead execution."""

    # Hardcoded defaults (no config file ceremony)
    MAX_RETRIES = 3
    STATE_FILE = Path(".beads/fsm-state.json")
    LEDGER_FILE = Path(".beads/ledger.md")

    def __init__(self):
        self.context: Optional[FSMContext] = None
        self._load_state()

    def _load_state(self) -> None:
        """Load FSM state from disk."""
        if self.STATE_FILE.exists():
            try:
                data = json.loads(self.STATE_FILE.read_text())
                self.context = FSMContext.from_dict(data)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠ State file corrupted: {e}")

    def _save_state(self) -> None:
        """Persist FSM state to disk."""
        if self.context:
            self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            state_dict = {
                "_WARNING": "⚠️ NEVER MANUALLY EDIT - Managed by fsm.py only",
                **self.context.to_dict()
            }
            self.STATE_FILE.write_text(json.dumps(state_dict, indent=2))

    def _get_current_commit_sha(self) -> str:
        """Get current git HEAD commit SHA."""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def _check_dependencies_simple(self, bead_path: str) -> bool:
        """
        Simple dependency check - verify depends_on beads are marked [x] in ledger.
        Returns True if all dependencies satisfied.
        """
        bead_file = Path(bead_path)
        if not bead_file.exists():
            return True

        content = bead_file.read_text()
        depends_match = re.search(r'depends_on:\s*\[([^\]]*)\]', content, re.IGNORECASE)
        if not depends_match:
            return True

        depends_str = depends_match.group(1).strip()
        if not depends_str:
            return True

        dependencies = [d.strip().strip('"\'') for d in depends_str.split(',')]
        if not self.LEDGER_FILE.exists():
            print(f"⚠ Cannot validate dependencies - ledger not found")
            return True

        ledger_content = self.LEDGER_FILE.read_text()
        incomplete = []
        for dep in dependencies:
            dep_id = '-'.join(dep.split('-')[:2])
            if not re.search(rf'\[x\]\s+Bead[- ]{dep_id}', ledger_content, re.IGNORECASE):
                incomplete.append(dep_id)

        if incomplete:
            print(f"✗ Incomplete dependencies: {', '.join(f'Bead-{d}' for d in incomplete)}")
            print(f"  Complete these beads first.")
            return False

        print(f"✓ Dependencies satisfied ({len(dependencies)} beads)")
        return True

    def init(
        self,
        bead_id: str,
        verification_cmd: Optional[str] = None,
        model: Optional[str] = None,
        active_model: Optional[str] = None,
        bead_path: Optional[str] = None,
    ) -> None:
        """
        Initialize FSM for new bead execution.

        IRON LOCK: active_model must match bead's required model.
        """
        # Check dependencies
        if bead_path and not self._check_dependencies_simple(bead_path):
            sys.exit(1)

        # Extract model, verification_cmd, bead_type, and verification_tier from bead file
        bead_type = "implementation"  # default
        verification_tier = "AUTO"  # default
        if bead_path:
            bead_file = Path(bead_path)
            if bead_file.exists():
                content = bead_file.read_text()
                model_match = re.search(r'model:\s*(\w+)', content, re.IGNORECASE)
                if model_match:
                    model = model_match.group(1).lower()
                verify_match = re.search(r'verification_cmd:\s*["\'](.+?)["\']', content)
                if verify_match:
                    verification_cmd = verify_match.group(1)
                # Extract bead type (spike or implementation)
                type_match = re.search(r'type:\s*(\w+)', content, re.IGNORECASE)
                if type_match:
                    bead_type = type_match.group(1).lower()
                # Extract verification tier (AUTO, MANUAL, NONE)
                tier_match = re.search(r'verification_tier:\s*(\w+)', content, re.IGNORECASE)
                if tier_match:
                    verification_tier = tier_match.group(1).upper()
                elif bead_type == "spike":
                    verification_tier = "NONE"  # Spike beads default to NONE

        # IRON LOCK: Model guard
        if active_model and model:
            actual = active_model.lower()
            expected = model.lower()
            for base in ['opus', 'sonnet', 'haiku']:
                if base in actual:
                    actual = base
                if base in expected:
                    expected = base

            if actual != expected:
                print(f"✗ IRON LOCK: Bead requires {expected.upper()}, running {actual.upper()}")
                print(f"  Switch models before proceeding.")
                sys.exit(1)

        initial_sha = self._get_current_commit_sha()
        self.context = FSMContext(
            bead_id=bead_id,
            current_state=State.DRAFT.value,
            retry_count=0,
            initial_commit_sha=initial_sha,
            verification_cmd=verification_cmd,
            model=model,
            last_verification_passed=False,
            bead_type=bead_type,
            verification_tier=verification_tier
        )
        self._save_state()
        print(f"✓ FSM initialized: Bead-{bead_id} ({initial_sha[:8]})")
        if bead_type == "spike":
            print(f"  ⚡ Spike bead (exploration mode - no verification required)")
        if verification_tier != "AUTO":
            tier_msg = {
                "MANUAL": "📋 Manual checklist verification required",
                "NONE": "⚠️  No verification required"
            }.get(verification_tier, "")
            if tier_msg:
                print(f"  {tier_msg}")
        if active_model:
            print(f"  ✓ Model guard passed: {active_model}")

        # Auto-transition to EXECUTE (ceremony reduction)
        self.context.current_state = State.EXECUTE.value
        self._save_state()
        print(f"✓ Auto-transitioned to EXECUTE")

        self.sync_ledger()

    def _find_next_pending_bead(self, ledger_content: str) -> Optional[str]:
        """Find first pending bead in ledger."""
        pattern = r'- \[ \] Bead[- ](\d{2}[- ]\d{2})'
        match = re.search(pattern, ledger_content, re.IGNORECASE)
        if match:
            return match.group(1).replace(' ', '-')
        return None

    def sync_ledger(self) -> bool:
        """
        Sync FSM state to ledger.md.
        Updates Active Bead section and marks completed beads with [x].
        Auto-queues next pending bead when current completes.
        """
        if not self.context:
            print("✗ FSM not initialized")
            return False

        if not self.LEDGER_FILE.exists():
            print(f"✗ Ledger not found: {self.LEDGER_FILE}")
            return False

        content = self.LEDGER_FILE.read_text()
        bead_id = self.context.bead_id
        state = self.context.current_state

        # Mark current bead complete in ledger history
        if state == 'complete':
            already_complete = re.search(rf'\[x\] Bead[- ]{bead_id}[:\s]', content, re.IGNORECASE)
            if not already_complete:
                pattern = rf'(- )\[ \]( Bead[- ]{bead_id}[:\s])'
                content, n = re.subn(pattern, r'\1[x]\2', content, count=1, flags=re.IGNORECASE)
                if n > 0:
                    print(f"✓ Marked Bead-{bead_id} complete in ledger")

        # Update Active Bead section
        if state in ['complete', 'failed']:
            next_bead = self._find_next_pending_bead(content)
            if next_bead:
                new_active = f"## Active Bead\n\n**Bead-{next_bead}**: PENDING\n"
                print(f"✓ Auto-queued: Bead-{next_bead}")
            else:
                new_active = f"## Active Bead\n\n**None** — All beads complete\n"
        else:
            new_active = f"## Active Bead\n\n**Bead-{bead_id}**: {state.upper()}\n"
            if self.context.retry_count > 0:
                new_active += f"- Retry: {self.context.retry_count}/{self.MAX_RETRIES}\n"

        # Replace Active Bead section
        pattern = r'## Active Bead\n+.*?(?=\n---|\n## |\Z)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_active.rstrip(), content, flags=re.DOTALL)
        else:
            content += f"\n---\n\n{new_active}"

        self.LEDGER_FILE.write_text(content)
        print(f"✓ Ledger synced: Bead-{bead_id} → {state}")
        return True

    def transition(self, target_state: str) -> None:
        """
        Transition to target state.
        INTEGRITY GATE: Cannot complete without passing verification.
        """
        if not self.context:
            raise RuntimeError("FSM not initialized. Run 'fsm.py init <bead_id>' first.")

        try:
            new_state = State(target_state)
        except ValueError:
            raise ValueError(f"Invalid state: {target_state}")

        current = State(self.context.current_state)

        # Validate transition
        valid_transitions = {
            State.DRAFT: [State.EXECUTE],
            State.EXECUTE: [State.VERIFY, State.COMPLETE],  # COMPLETE allowed for spike beads
            State.VERIFY: [State.COMPLETE, State.RECOVER],
            State.RECOVER: [State.EXECUTE, State.FAILED],
            State.COMPLETE: [],
            State.FAILED: []
        }

        # For spike beads, allow direct EXECUTE -> COMPLETE
        if current == State.EXECUTE and new_state == State.COMPLETE:
            if self.context.bead_type != "spike":
                raise RuntimeError(f"Cannot transition EXECUTE -> COMPLETE for implementation beads (must verify first)")
        elif new_state not in valid_transitions.get(current, []):
            raise RuntimeError(f"Invalid transition: {current.value} -> {new_state.value}")

        # INTEGRITY GATE (skip for NONE tier)
        if new_state == State.COMPLETE and not self.context.last_verification_passed:
            if self.context.verification_tier == "NONE":
                print(f"✓ Verification tier NONE - skipping verification requirement")
            else:
                print(f"✗ Cannot complete: verification not passed")
                print(f"  Tier: {self.context.verification_tier}")
                print(f"  Run: fsm.py verify \"<cmd>\"")
                sys.exit(1)

        self.context.current_state = new_state.value
        self._save_state()
        print(f"✓ Transition: {current.value} -> {new_state.value}")

        self.sync_ledger()

    def verify(self, verification_cmd: Optional[str] = None) -> bool:
        """
        Run verification command.
        Only this method can set last_verification_passed=True.
        Auto-prefixes python commands with 'uv run'.
        """
        if not self.context:
            raise RuntimeError("FSM not initialized.")

        cmd = verification_cmd or self.context.verification_cmd
        if not cmd:
            raise ValueError("No verification command provided.")

        # Auto-prefix python commands with 'uv run'
        python_commands = ['pytest', 'python', 'mypy', 'ruff', 'coverage']
        needs_prefix = any(cmd.strip().startswith(tool) for tool in python_commands)
        if needs_prefix and not cmd.strip().startswith('uv run'):
            cmd = f"uv run {cmd}"
            print(f"⚙ Auto-prefixed: {cmd}")

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.context.last_verification_passed = True
            self._save_state()
            print("✓ Verification PASSED")
            if State(self.context.current_state) == State.EXECUTE:
                self.transition(State.VERIFY.value)
            self.transition(State.COMPLETE.value)
            return True

        # Exit code 127 = command not found (environment error, don't retry)
        if result.returncode == 127:
            print(f"✗ Command not found (exit 127): {cmd}")
            if result.stderr:
                print(f"  {result.stderr.strip()}")
            print(f"  Install missing tool or check environment")
            return False

        print(f"✗ Verification FAILED (exit {result.returncode})")
        if result.stderr:
            print(f"  {result.stderr.strip()}")

        # Circuit breaker retry logic
        self.context.retry_count += 1
        self.context.last_verification_passed = False
        self._save_state()

        if self.context.retry_count >= self.MAX_RETRIES:
            print(f"✗ Circuit breaker: {self.context.retry_count}/{self.MAX_RETRIES} attempts")
            self.transition(State.FAILED.value)
        else:
            print(f"⚠ Retry {self.context.retry_count}/{self.MAX_RETRIES} - entering RECOVER")
            self.transition(State.RECOVER.value)
            if self.context.retry_count >= 2:
                print("⚠ Consider rollback: fsm.py rollback")

        return False

    def rollback(self) -> None:
        """Hard rollback to initial commit state."""
        if not self.context:
            raise RuntimeError("FSM not initialized.")

        initial_sha = self.context.initial_commit_sha
        print(f"⚠ Rolling back to {initial_sha[:8]}")

        # Save context before rollback
        saved_context = FSMContext(
            bead_id=self.context.bead_id,
            current_state=State.DRAFT.value,
            retry_count=self.context.retry_count,
            initial_commit_sha=self.context.initial_commit_sha,
            verification_cmd=self.context.verification_cmd,
            model=self.context.model
        )

        try:
            subprocess.run(["git", "reset", "--hard", initial_sha], check=True, capture_output=True)
            subprocess.run(
                ["git", "clean", "-fd", "--exclude=.beads/", "--exclude=.planning/"],
                check=True,
                capture_output=True
            )

            # Restore FSM state
            self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            self.STATE_FILE.write_text(json.dumps(saved_context.to_dict(), indent=2))
            self.context = saved_context

            print("✓ Rollback complete - state reset to DRAFT")

        except subprocess.CalledProcessError as e:
            print(f"✗ Rollback failed: {e}")
            sys.exit(1)

    def status(self) -> None:
        """Display current FSM status."""
        if not self.context:
            print("FSM not initialized")
            return

        print(f"Bead: {self.context.bead_id}")
        print(f"State: {self.context.current_state}")
        print(f"Retry: {self.context.retry_count}/{self.MAX_RETRIES}")
        print(f"Initial commit: {self.context.initial_commit_sha[:8]}")
        if self.context.model:
            print(f"Model: {self.context.model}")
        if self.context.verification_cmd:
            print(f"Verification: {self.context.verification_cmd}")

    def reset(self) -> None:
        """Clear FSM state."""
        if self.STATE_FILE.exists():
            self.STATE_FILE.unlink()
        self.context = None
        print("✓ FSM state cleared")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    fsm = BeadFSM()

    try:
        if command == "init":
            if len(sys.argv) < 3:
                print("Usage: fsm.py init <bead_id> [--active-model MODEL] [--bead PATH]")
                sys.exit(1)

            bead_id = sys.argv[2]
            verification_cmd = None
            model = None
            active_model = None
            bead_path = None

            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--model" and i + 1 < len(sys.argv):
                    model = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == "--verify" and i + 1 < len(sys.argv):
                    verification_cmd = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == "--active-model" and i + 1 < len(sys.argv):
                    active_model = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == "--bead" and i + 1 < len(sys.argv):
                    bead_path = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1

            fsm.init(bead_id, verification_cmd, model, active_model, bead_path)

        elif command == "transition":
            if len(sys.argv) < 3:
                print("Usage: fsm.py transition <state>")
                sys.exit(1)
            fsm.transition(sys.argv[2])

        elif command == "verify":
            verification_cmd = sys.argv[2] if len(sys.argv) > 2 else None
            success = fsm.verify(verification_cmd)
            sys.exit(0 if success else 1)

        elif command == "rollback":
            fsm.rollback()

        elif command == "status":
            fsm.status()

        elif command == "reset":
            fsm.reset()

        elif command == "sync-ledger":
            success = fsm.sync_ledger()
            sys.exit(0 if success else 1)

        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
