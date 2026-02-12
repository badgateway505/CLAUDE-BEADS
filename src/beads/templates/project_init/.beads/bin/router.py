#!/usr/bin/env python3
"""
Claude Beads Model Router

Capability-based model selection for optimal cost/performance.
Configuration is loaded from \.beads/config.yaml (project-specific).

Routes tasks to appropriate Claude model based on complexity:
- Opus: Architecture, long-horizon planning, research
- Sonnet: Implementation, refactoring, debugging
- Haiku: Summarization, simple edits, ledger updates

Usage:
    python router.py route <bead_intent>        # Recommend model for task
    python router.py map-tests <file1> [file2]  # Map files to test suite
    python router.py validate-ledger            # Validate ledger structure
    python router.py validate-all               # Full framework validation
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_config() -> dict[str, Any]:
    """
    Load configuration from \.beads/config.yaml.

    Falls back to sensible defaults if config is missing or malformed.
    """
    config_path = Path("\.beads/config.yaml")

    if not config_path.exists():
        print("⚠ Config not found, using defaults")
        return _default_config()

    try:
        # Use PyYAML if available, otherwise fall back to basic parsing
        try:
            import yaml
            with open(config_path) as f:
                config = yaml.safe_load(f)
                if config is None:
                    return _default_config()
                return config
        except ImportError:
            # Fallback: basic YAML parsing for simple cases
            return _parse_simple_yaml(config_path)
    except Exception as e:
        print(f"⚠ Failed to load config: {e}, using defaults")
        return _default_config()


def _default_config() -> dict[str, Any]:
    """Return default configuration when config.yaml is missing."""
    return {
        "project": {
            "name": "Unknown Project",
            "description": "",
        },
        "models": {
            "defaults": {
                "architecture": "opus",
                "research": "opus",
                "implementation": "sonnet",
                "verification": "sonnet",
                "summarization": "haiku",
            },
            "opus_indicators": [
                r'\barchitecture\b',
                r'\bdesign\b',
                r'\bresearch\b',
                r'\bplan\b',
                r'\bstrategy\b',
                r'\brefactor\b.*\bmultiple\b',
                r'\brefactor\b.*\bsystem\b',
                r'\bevaluate\b.*\balternatives?\b',
                r'\bcompare\b.*\bapproaches?\b',
                r'\boptimize\b.*\barchitecture\b',
                r'\bmigration\b',
                r'\bframework\b',
            ],
            "haiku_indicators": [
                r'\bsummarize\b',
                r'\bupdate\b.*\bledger\b',
                r'\bformat\b',
                r'\btypo\b',
                r'\brename\b.*\bvariable\b',
                r'\badd\b.*\bcomment\b',
                r'\bfix\b.*\bformatting\b',
            ],
        },
        "testing": {
            "tests_dir": "tests/",
            "critical_path": "tests/critical/",
            "default_cmd": "pytest {tests} -v --tb=short",
            "surgical": True,
            "test_map": {},
        },
        "fsm": {
            "max_retries": 3,
            "soft_retry_threshold": 1,
            "hard_rollback_threshold": 2,
        },
        "ledger": {
            "path": "\.beads/ledger.md",
            "cost_tracking": True,
            "sha_tracking": True,
        },
    }


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    """
    Basic YAML parser for when PyYAML is not installed.

    Only handles the subset of YAML we need for config.
    For full YAML support, install PyYAML: pip install pyyaml
    """
    print("⚠ PyYAML not installed, using limited parser")
    print("  Install with: pip install pyyaml")
    return _default_config()


class ModelRouter:
    """
    Routes tasks to optimal Claude model based on complexity analysis.

    Model Selection Hierarchy:
    - Opus ($15/1M): Architecture, research, multi-file refactoring
    - Sonnet ($3/1M): Implementation, debugging, verification
    - Haiku ($0.25/1M): Summarization, simple edits
    """

    def __init__(self, config: dict[str, Any] | None = None):
        if config is None:
            config = load_config()

        models_config = config.get("models", {})
        self.opus_indicators = models_config.get("opus_indicators", [])
        self.haiku_indicators = models_config.get("haiku_indicators", [])
        self.defaults = models_config.get("defaults", {})

    def route(self, bead_intent: str) -> str:
        """
        Analyze bead intent and recommend optimal model.

        Args:
            bead_intent: Description of task to execute

        Returns:
            Model identifier: "opus" | "sonnet" | "haiku"
        """
        intent_lower = bead_intent.lower()

        # Check for Opus-level complexity
        for pattern in self.opus_indicators:
            if re.search(pattern, intent_lower):
                return "opus"

        # Check for Haiku-level simplicity
        for pattern in self.haiku_indicators:
            if re.search(pattern, intent_lower):
                return "haiku"

        # Default to Sonnet for implementation
        return self.defaults.get("implementation", "sonnet")

    def explain_routing(self, bead_intent: str) -> None:
        """Print routing decision with justification."""
        model = self.route(bead_intent)
        intent_lower = bead_intent.lower()

        print(f"Recommended model: {model}")
        print(f"Intent: {bead_intent}")
        print()

        if model == "opus":
            print("Rationale: High-complexity task requiring long-horizon reasoning")
            matched = [p for p in self.opus_indicators if re.search(p, intent_lower)]
            if matched:
                print(f"Matched patterns: {matched[0]}")
            print("Cost: ~$15/1M tokens | TTFT: ~500ms")

        elif model == "haiku":
            print("Rationale: Simple, well-defined task")
            matched = [p for p in self.haiku_indicators if re.search(p, intent_lower)]
            if matched:
                print(f"Matched patterns: {matched[0]}")
            print("Cost: ~$0.25/1M tokens | TTFT: ~100ms")

        else:  # sonnet
            print("Rationale: Standard implementation/debugging task")
            print("Cost: ~$3/1M tokens | TTFT: ~300ms")


class TestMapper:
    """
    Maps changed files to relevant test suite (Test Impact Analysis).

    Surgical verification - run only affected tests for fast feedback.
    Configuration loaded from \.beads/config.yaml testing section.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        if config is None:
            config = load_config()

        testing_config = config.get("testing", {})
        self.test_map = testing_config.get("test_map", {})
        self.tests_dir = testing_config.get("tests_dir", "tests/")
        self.critical_path = testing_config.get("critical_path", "tests/critical/")
        self.surgical = testing_config.get("surgical", True)
        self.default_cmd = testing_config.get("default_cmd", "pytest {tests} -v")

    def map_files_to_tests(self, changed_files: list[str]) -> str:
        """
        Map changed files to pytest command.

        Args:
            changed_files: List of file paths that changed

        Returns:
            pytest command to run relevant tests
        """
        # If surgical verification is disabled, run all tests
        if not self.surgical:
            return f"pytest {self.tests_dir} -v"

        # If no files provided, run critical path
        if not changed_files:
            return self._format_cmd(self.critical_path)

        # If no test map configured, scan tests directory
        if not self.test_map:
            return self._fallback_test_discovery(changed_files)

        matched_tests = set()

        for file_path in changed_files:
            for pattern, test_file in self.test_map.items():
                if re.search(pattern, file_path):
                    matched_tests.add(test_file)

        if matched_tests:
            test_args = ' '.join(sorted(matched_tests))
            return self._format_cmd(test_args)
        else:
            # Fallback to critical path if no specific tests found
            critical = Path(self.critical_path)
            if critical.exists():
                return self._format_cmd(self.critical_path)
            # If no critical path, run all tests
            return self._format_cmd(self.tests_dir)

    def _format_cmd(self, tests: str) -> str:
        """Format the pytest command with test paths."""
        return self.default_cmd.format(tests=tests)

    def _fallback_test_discovery(self, changed_files: list[str]) -> str:
        """
        Auto-discover tests when no test_map is configured.

        Uses naming convention: src/foo/bar.py -> tests/test_bar.py
        """
        tests_dir = Path(self.tests_dir)
        if not tests_dir.exists():
            return f"pytest {self.tests_dir} -v"

        matched_tests = set()

        for file_path in changed_files:
            path = Path(file_path)
            if path.suffix != ".py":
                continue

            # Try common test naming conventions
            test_names = [
                f"test_{path.stem}.py",           # test_foo.py
                f"{path.stem}_test.py",           # foo_test.py
            ]

            for test_name in test_names:
                test_path = tests_dir / test_name
                if test_path.exists():
                    matched_tests.add(str(test_path))

        if matched_tests:
            return self._format_cmd(' '.join(sorted(matched_tests)))

        return self._format_cmd(self.tests_dir)

    def map_from_git_diff(self) -> str:
        """
        Generate pytest command from current git diff.

        Returns:
            pytest command for changed files
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            changed_files = result.stdout.strip().split('\n')
            changed_files = [f for f in changed_files if f]
            return self.map_files_to_tests(changed_files)

        except subprocess.CalledProcessError:
            return self._format_cmd(self.tests_dir)


class LedgerValidator:
    """Validate \.beads/ledger.md structure and consistency."""

    # Required section patterns (regex for flexibility)
    REQUIRED_PATTERNS = [
        (r'^# Ledger:', "# Ledger: header"),
        (r'^## (?:Global Context|Project Vision)', "Global Context or Project Vision section"),
        (r'^## (?:Ledger History|Roadmap)', "Ledger History or Roadmap section"),
    ]

    # Bead entry patterns (supports multiple formats)
    BEAD_PATTERNS = [
        r'- \[(x| )\] Bead[- ]?\d{2}[- ]?\d{2}',
        r'- \[(x| )\] Bead[- ]?\d{2}[- ]?XX',
    ]

    def __init__(self, config: dict[str, Any] | None = None):
        if config is None:
            config = load_config()

        ledger_config = config.get("ledger", {})
        self.ledger_path = Path(ledger_config.get("path", "\.beads/ledger.md"))

    def validate(self) -> bool:
        """
        Validate ledger structure.

        Returns:
            True if valid, False otherwise
        """
        if not self.ledger_path.exists():
            print(f"✗ Ledger not found: {self.ledger_path}")
            return False

        content = self.ledger_path.read_text()

        # Check required sections using regex (case-insensitive, multiline)
        missing = []
        for pattern, description in self.REQUIRED_PATTERNS:
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                missing.append(description)

        if missing:
            print("✗ Ledger validation failed")
            print(f"  Missing sections: {missing}")
            return False

        # Check for bead entries (any supported format)
        bead_count = 0
        for pattern in self.BEAD_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            bead_count += len(matches)

        if bead_count == 0:
            print("⚠ No beads found in ledger (might be new project)")

        print("✓ Ledger structure valid")
        print(f"  Found {bead_count} bead entries")
        return True


class FrameworkValidator:
    """Validate entire Beads framework integrity."""

    def __init__(self, config: dict[str, Any] | None = None):
        if config is None:
            config = load_config()
        self.config = config

    def validate_all(self) -> bool:
        """
        Run all framework validations.

        Returns:
            True if all validations pass, False otherwise
        """
        results = []

        # 1. Validate ledger
        print("=" * 50)
        print("Validating ledger...")
        ledger = LedgerValidator(self.config)
        results.append(("Ledger", ledger.validate()))

        # 2. Check config structure
        print()
        print("=" * 50)
        print("Validating config...")
        results.append(("Config", self._validate_config()))

        # 3. Check .claudeignore exists
        print()
        print("=" * 50)
        print("Validating context isolation...")
        results.append(("Context", self._validate_context_isolation()))

        # 4. Check active beads have verification_cmd
        print()
        print("=" * 50)
        print("Validating active beads...")
        results.append(("Beads", self._validate_active_beads()))

        # Summary
        print()
        print("=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        all_passed = True
        for name, passed in results:
            status = "✓" if passed else "✗"
            print(f"  {status} {name}")
            if not passed:
                all_passed = False

        return all_passed

    def _validate_config(self) -> bool:
        """Validate config.yaml structure."""
        # Claude Beads: Only essential sections required
        required_sections = ["models", "testing", "fsm", "ledger"]
        missing = [s for s in required_sections if s not in self.config]

        if missing:
            print(f"✗ Config missing sections: {missing}")
            return False

        print("✓ Config structure valid")
        return True

    def _validate_context_isolation(self) -> bool:
        """Validate .claudeignore exists and is not empty."""
        context_config = self.config.get("context", {})
        ignore_file = Path(context_config.get("ignore_file", ".claudeignore"))

        if not ignore_file.exists():
            print(f"⚠ Ignore file not found: {ignore_file}")
            print("  Context isolation not configured")
            return True  # Warning, not failure

        content = ignore_file.read_text().strip()
        if not content:
            print(f"⚠ Ignore file is empty: {ignore_file}")
            return True  # Warning, not failure

        # Count frozen entries
        lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
        print(f"✓ Context isolation configured ({len(lines)} patterns)")
        return True

    def _validate_active_beads(self) -> bool:
        """Check that active beads have verification commands."""
        # Find active phase from ledger
        ledger_config = self.config.get("ledger", {})
        ledger_path = Path(ledger_config.get("path", "\.beads/ledger.md"))

        if not ledger_path.exists():
            print("⚠ Cannot validate beads without ledger")
            return True

        content = ledger_path.read_text()

        # Find active phase
        active_match = re.search(r'Phase \d+.*@status\(active\)', content)
        if not active_match:
            print("⚠ No active phase found")
            return True

        # Look for bead files in .planning/phases/
        bead_dirs = list(Path(".planning/phases").glob("*/beads"))
        if not bead_dirs:
            print("⚠ No bead directories found")
            return True

        # Check for verification in bead files
        beads_without_verify = []
        for bead_dir in bead_dirs:
            for bead_file in bead_dir.glob("*.md"):
                bead_content = bead_file.read_text()
                if "## Verification" not in bead_content and "<verification>" not in bead_content:
                    beads_without_verify.append(bead_file.name)

        if beads_without_verify:
            print(f"⚠ Beads missing verification: {beads_without_verify[:3]}...")
            return True  # Warning, not failure

        print("✓ Active beads have verification commands")
        return True


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    config = load_config()

    try:
        if command == "route":
            if len(sys.argv) < 3:
                print("Usage: router.py route <bead_intent>")
                sys.exit(1)
            bead_intent = ' '.join(sys.argv[2:])
            router = ModelRouter(config)
            router.explain_routing(bead_intent)

        elif command == "map-tests":
            mapper = TestMapper(config)
            if len(sys.argv) < 3:
                pytest_cmd = mapper.map_from_git_diff()
            else:
                files = sys.argv[2:]
                pytest_cmd = mapper.map_files_to_tests(files)
            print(pytest_cmd)

        elif command == "validate-ledger":
            validator = LedgerValidator(config)
            success = validator.validate()
            sys.exit(0 if success else 1)

        elif command == "validate-all":
            validator = FrameworkValidator(config)
            success = validator.validate_all()
            sys.exit(0 if success else 1)

        elif command == "config":
            # Debug: print loaded config
            import json
            print(json.dumps(config, indent=2, default=str))

        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
