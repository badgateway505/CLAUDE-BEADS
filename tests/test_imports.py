"""Basic import tests for claude-beads package."""


def test_package_import():
    """Test that the beads package can be imported."""
    import beads
    assert beads.__version__ == "1.0.0"


def test_fsm_import():
    """Test that FSM classes can be imported."""
    from beads import BeadFSM, FSMContext, State
    assert BeadFSM is not None
    assert FSMContext is not None
    assert State is not None


def test_cli_import():
    """Test that CLI module can be imported."""
    from beads.cli.main import cli
    assert cli is not None


def test_init_import():
    """Test that initialization module can be imported."""
    from beads.init import initialize_project
    assert initialize_project is not None


def test_status_import():
    """Test that status module can be imported."""
    from beads.status import show_status
    assert show_status is not None
