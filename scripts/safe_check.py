"""safe_check decorator: wrap audit checks so a single failure doesn't abort the audit.

v0.1.1 stages this decorator as a v0.3 interface. The 12 production checks
in v0.1.1 are all deterministic and never throw, so the catch path is
exercised only in tests. v0.3 will plug real LLM calls into this decorator.
"""
from __future__ import annotations

import functools
import traceback
from collections.abc import Callable

from scripts.report import CheckResult


def safe_check(fn: Callable[..., CheckResult]) -> Callable[..., CheckResult]:
    """Decorator that catches exceptions and returns a skipped CheckResult.

    Usage:
        @safe_check
        def my_check(assets: RepoAssets) -> CheckResult:
            ...

    If `my_check` throws, the decorator returns:
        CheckResult(skipped=True, passed=False, error="<msg>", score=0, max_score=10)

    The original exception's traceback is also stored in `error` for debugging.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> CheckResult:
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            tb = traceback.format_exc()
            return CheckResult(
                id=fn.__name__,
                name=fn.__name__,
                category="unknown",
                score=0,
                max_score=10,
                passed=False,
                impact=0,
                skipped=True,
                error=f"{type(exc).__name__}: {exc}\n{tb}",
            )

    return wrapper
