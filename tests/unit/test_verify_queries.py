"""Query generator unit tests."""
from scripts.verify.queries import generate_queries


def test_generates_10_queries_by_default():
    queries = generate_queries(project_name="aisurface", description="AI search audit for OSS", project_type="python-library")
    assert len(queries) == 10


def test_queries_mention_project_topic():
    queries = generate_queries(project_name="ziwei", description="Zi Wei Dou Shu web app", project_type="web-app")
    assert any("Zi Wei" in q or "ziwei" in q.lower() or "dou shu" in q.lower() for q in queries)


def test_count_parameter():
    assert len(generate_queries("x", "y", "generic", count=5)) == 5


def test_custom_queries_from_file(tmp_path):
    qfile = tmp_path / "q.txt"
    qfile.write_text("Q1\nQ2\nQ3\n", encoding="utf-8")
    from scripts.verify.queries import load_queries_from_file
    assert load_queries_from_file(qfile) == ["Q1", "Q2", "Q3"]
