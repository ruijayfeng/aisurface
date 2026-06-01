from scripts.critic import offline_critique, parse_critique_response


def test_offline_critique_scores_readme_quality():
    result = offline_critique(
        readme_text="# my-tool\n\nA fast CLI for parsing Markdown.\n\n## Install\n\npip install my-tool\n",
        topic="CLI tool",
    )
    assert 0 <= result["problem_clarity"] <= 10
    assert 0 <= result["has_faq"] <= 10
    assert 0 <= result["has_code_examples"] <= 10
    assert "would_cite" in result
    # Test readme has "## Install" + "pip install" — code example branch should fire
    assert result["has_code_examples"] >= 4
    # Test readme's first paragraph is "A fast CLI for parsing Markdown." (35 chars, no problem keywords)
    # and doesn't contain superlatives. Base score 5, "fast" keyword gives +2.
    assert result["problem_clarity"] == 7
    # No FAQ section, no code examples >= 2 fences, no "when to use" — these are all 0
    assert result["has_faq"] == 0
    assert result["has_when_to_use"] == 0
    # topic is now in the summary
    assert "CLI tool" in result["summary"]


def test_offline_critique_detects_faq():
    readme = "# Tool\n\nA test.\n\n## FAQ\n\n### Q: How?\nA: Yes.\n"
    result = offline_critique(readme_text=readme, topic="x")
    assert result["has_faq"] >= 8


def test_offline_critique_detects_code_examples():
    readme = "# Tool\n\n## Install\n\n```bash\npip install x\n```\n"
    result = offline_critique(readme_text=readme, topic="x")
    assert result["has_code_examples"] >= 8


def test_offline_critique_detects_problem_statement():
    weak = "# Tool\n\nA thing.\n"
    strong = "# Tool\n\nTired of manually converting Markdown? my-tool automates it in 3 lines.\n"
    weak_result = offline_critique(weak, "x")
    strong_result = offline_critique(strong, "x")
    assert strong_result["problem_clarity"] > weak_result["problem_clarity"]


def test_parse_critique_response_handles_json():
    raw = '{"would_cite": "yes", "problem_clarity": 8}'
    parsed = parse_critique_response(raw)
    assert parsed["would_cite"] == "yes"
    assert parsed["problem_clarity"] == 8


def test_parse_critique_response_handles_markdown_fenced_json():
    raw = '```json\n{"would_cite": "no", "problem_clarity": 3}\n```'
    parsed = parse_critique_response(raw)
    assert parsed["problem_clarity"] == 3
