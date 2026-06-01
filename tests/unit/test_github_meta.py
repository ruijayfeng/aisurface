from scripts.github_meta import (
    TOPIC_SUGGESTIONS,
    evaluate_description,
    suggest_topics,
)


def test_suggest_topics_from_readme():
    readme = "# my-tool\n\nA Python library for parsing Markdown files.\n"
    topics = suggest_topics(readme, existing=[])
    assert "python" in topics
    assert "markdown" in topics or "parser" in topics


def test_suggest_topics_respects_existing():
    readme = "# my-tool\n\nA Python library.\n"
    topics = suggest_topics(readme, existing=["python"])
    # Should not duplicate
    assert topics.count("python") <= 1


def test_suggest_topics_caps_at_12():
    readme = "python javascript rust go java ruby php swift kotlin typescript react vue\n" * 20
    topics = suggest_topics(readme, existing=[])
    assert len(topics) <= 12


def test_evaluate_description_good():
    desc = "A fast, open-source CLI tool that converts Markdown to HTML with 50+ themes."
    score, notes = evaluate_description(desc)
    assert score == 10
    assert "length" in notes.lower()
    assert "vague" not in notes.lower()
    assert "short" not in notes.lower()
    assert "long" not in notes.lower()


def test_evaluate_description_too_short():
    desc = "A tool."
    score, notes = evaluate_description(desc)
    assert score < 7


def test_evaluate_description_too_vague():
    desc = "Best tool ever made for doing things with stuff and more"
    score, notes = evaluate_description(desc)
    assert score < 7


def test_topic_suggestions_constant_is_nonempty():
    assert len(TOPIC_SUGGESTIONS) >= 10
