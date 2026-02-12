"""Claude Beads - Atomic task execution for AI projects."""

__version__ = "1.0.0"
__author__ = "Beads Contributors"
__license__ = "MIT"

from .fsm import BeadFSM, FSMContext, State

__all__ = ["BeadFSM", "FSMContext", "State", "__version__"]
