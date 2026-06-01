from scripts.distribution import AWESOME_LISTS, check_signals


def test_check_signals_no_signals():
    result = check_signals(
        project_name="unknown-xyz-project",
        description="A test",
        github_stars=5,
        has_npm=False,
        has_pypi=False,
    )
    assert result["score"] <= 3
    assert "low_visibility" in result["notes"].lower() or "low stars" in result["notes"].lower()


def test_check_signals_strong_signals():
    result = check_signals(
        project_name="react",
        description="A JavaScript library for building user interfaces",
        github_stars=220000,
        has_npm=True,
        has_pypi=False,
    )
    assert result["score"] >= 8


def test_awesome_lists_constant_is_nonempty():
    assert len(AWESOME_LISTS) > 0
    assert any("awesome" in url.lower() for url in AWESOME_LISTS)
