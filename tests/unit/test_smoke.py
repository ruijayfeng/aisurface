def test_imports_work():
    """Verify the scripts package imports cleanly."""
    import scripts

    assert scripts is not None


def test_scripts_is_package():
    """Verify scripts is a proper package, not a module."""
    import scripts

    assert hasattr(scripts, "__path__"), "scripts should be a package (have __path__)"
