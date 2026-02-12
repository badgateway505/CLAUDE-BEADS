# Changelog

All notable changes to the Claude Beads package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-12

### Added
- Initial release of Claude Beads as standalone package
- CLI commands: `beads init`, `beads status`, `beads help`
- Project initialization with `.beads/`, `.claude/`, `.planning/` scaffolding
- Finite State Machine (FSM) for bead lifecycle management
- Three verification tiers: AUTO (automated tests), MANUAL (checklist), NONE (exploratory)
- Spike bead type for time-boxed exploration
- Rationale-based exceptions to standard protocol
- Comprehensive documentation templates
- Claude Code skills integration: `/beads:run`, `/beads:plan`, `/beads:research`, etc.

### Features
- **Atomic Execution**: Break complex work into verifiable, 30min-2hr tasks
- **Token Efficiency**: 70-85% reduction via ledger-based context handoff
- **Model Routing**: Automatic Opus/Sonnet/Haiku selection per bead
- **Circuit Breaker**: 3-attempt retry strategy with soft/hard rollback
- **Context Isolation**: Phase freezing prevents stale context bleeding
- **HARD LOCK**: Requires `/clear` before bead execution to prevent context pollution
- **IRON LOCK**: Enforces model guard verification before execution

### Documentation
- `.beads/PROTOCOL.md` - Complete execution protocol
- `.beads/README.md` - Quick reference guide
- `.beads/VERIFICATION-TIERS.md` - Testing strategy guide
- `.beads/RATIONALE-EXAMPLES.md` - Exception documentation examples
- Templates for implementation beads, spike beads, and research

## [Unreleased]

Nothing yet.
