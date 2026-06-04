"""Unit tests for verify subcommand helpers (cost warning, query truncation)."""
from __future__ import annotations

from scripts.verify import _print_cost_warning, _truncate_queries
from scripts.verify.perplexity import PERPLEXITY_COST_PER_QUERY_USD

# -- Cost warning ----------------------------------------------------------

def test_print_cost_warning_for_perplexity(capsys):
    """Cost warning shows for Perplexity with query count and dollar estimate"""
    _print_cost_warning(["perplexity"], 10)
    captured = capsys.readouterr()
    assert "this run = 10" in captured.out
    assert "Perplexity queries" in captured.out
    assert f"~${PERPLEXITY_COST_PER_QUERY_USD:.4f}" in captured.out


def test_print_cost_warning_includes_total(capsys):
    """Cost warning shows the total estimated cost"""
    _print_cost_warning(["perplexity"], 10)
    captured = capsys.readouterr()
    expected_total = 10 * PERPLEXITY_COST_PER_QUERY_USD
    assert f"${expected_total:.2f}" in captured.out


def test_no_cost_warning_for_non_perplexity(capsys):
    """Cost warning is silent when Perplexity is not in the platform list"""
    _print_cost_warning(["deepseek", "chatgpt"], 10)
    captured = capsys.readouterr()
    assert captured.out == ""


# -- Query truncation ------------------------------------------------------

def test_truncate_queries_none_means_no_limit():
    """When max_queries is None, all queries pass through"""
    assert _truncate_queries(["a", "b", "c"], None) == ["a", "b", "c"]


def test_truncate_queries_over_limit_truncates_and_warns(capsys):
    """Truncates when over the limit and prints a stderr message"""
    result = _truncate_queries(["a", "b", "c", "d", "e"], 2)
    captured = capsys.readouterr()
    assert result == ["a", "b"]
    assert "--max-queries=2" in captured.err
    assert "5" in captured.err  # original count


def test_truncate_queries_under_limit_passes_through(capsys):
    """No truncation when under the limit, no message printed"""
    result = _truncate_queries(["a", "b"], 5)
    captured = capsys.readouterr()
    assert result == ["a", "b"]
    assert captured.err == ""
