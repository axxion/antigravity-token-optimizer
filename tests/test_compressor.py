"""
Tests for ContextCompressor and OutputFilters.
"""

from antigravity_optimizer.core.compressor import ContextCompressor
from antigravity_optimizer.core.config import OptimizerConfig, ProfileType


def test_command_compression():
    compressor = ContextCompressor(OptimizerConfig(profile=ProfileType.BALANCED))

    # Pytest output with lots of noise and one failure
    raw_pytest = """
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-8.0.0
rootdir: /project
collected 50 items

test_auth.py ....................................                      [ 72%]
test_api.py .............F                                             [100%]

================================== FAILURES ===================================
_________________________________ test_login __________________________________

    def test_login():
>       assert login("bad") == 200
E       assert 401 == 200

test_api.py:15: AssertionError
=========================== short test summary info ===========================
FAILED test_api.py::test_login - assert 401 == 200
======================== 1 failed, 49 passed in 0.42s =========================
"""
    res = compressor.compress_command_output("pytest tests/", raw_pytest)
    assert res.ratio_pct > 0
    assert "FAILURES" in res.content
    assert "AssertionError" in res.content
    assert "1 failed, 49 passed" in res.content


def test_search_compression():
    compressor = ContextCompressor(OptimizerConfig(max_grep_matches=5))

    raw_search = "\n".join(f"src/file_{i}.py:{i}: " + ("x" * 200) for i in range(20))
    res = compressor.compress_search_results(raw_search)

    assert res.ratio_pct > 0
    assert "ek eşleşme bağlam tasarrufu için gizlendi" in res.content
    assert len(res.content.splitlines()) <= 8


def test_data_compactor():
    import json
    compressor = ContextCompressor()

    raw_data = [
        {"id": 1, "name": "Alice", "role": "admin", "empty_field": None, "notes": ""},
        {"id": 2, "name": "Bob", "role": "developer", "empty_field": None, "notes": ""},
        {"id": 3, "name": "Charlie", "role": "designer", "empty_field": None, "notes": ""},
    ]
    raw_json = json.dumps(raw_data, indent=4)
    res = compressor.compress_structured_data(raw_json)

    assert res.ratio_pct > 30
    assert "__compact_table__" in res.content
    assert "columns" in res.content
    assert "rows" in res.content
    assert "empty_field" not in res.content  # Stripped null


def test_context_buffer_store():
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        from pathlib import Path
        compressor = ContextCompressor(cache_dir=Path(tmpdir))

        huge_log = "FATAL ERROR AT LINE " + ("0123456789\n" * 1000)
        res = compressor.compress_command_output("npm test", huge_log)

        assert res.ref_id is not None
        assert "Orijinal cikti saklandi" in res.content

        # Retrieve back
        recovered = compressor.store.retrieve(res.ref_id)
        assert recovered == huge_log


def test_cargo_go_compression_keeps_failure_detail():
    """Regression: the filter used to keep only marker lines, discarding the panic
    message, the assertion left/right values and the `file.go:42: expected X got Y`
    lines — i.e. everything that makes a failure actionable."""
    from antigravity_optimizer.parsers.output_filters import OutputFilters

    cargo = "\n".join([
        "   Compiling payments v0.1.0",
        "    Finished test [unoptimized + debuginfo] target(s) in 2.31s",
        "",
        "running 24 tests",
        *[f"test util::case_{i} ... ok" for i in range(18)],
        "test payments::test_total ... FAILED",
        "",
        "---- payments::test_total stdout ----",
        "thread 'payments::test_total' panicked at src/payments.rs:88:5:",
        "assertion `left == right` failed",
        "  left: 41",
        " right: 42",
        "",
        "test result: FAILED. 23 passed; 1 failed; 0 ignored",
    ])
    out, changed = OutputFilters.filter_cargo_go(cargo)
    assert changed is True
    for needed in ("panicked at", "left: 41", "right: 42", "test result: FAILED"):
        assert needed in out, f"cargo failure detail lost: {needed!r}"
    assert len(out) < len(cargo), "no compression achieved"

    go = "\n".join([
        *[f"=== RUN   TestOther{i}" for i in range(14)],
        *[f"--- PASS: TestOther{i} (0.00s)" for i in range(14)],
        "--- FAIL: TestCheckout (0.01s)",
        "    payment_test.go:42: expected 1999 got 0",
        "    payment_test.go:43: currency mismatch: TRY vs USD",
        "FAIL",
        "FAIL\texample.com/pkg/payment\t0.031s",
    ])
    out, changed = OutputFilters.filter_cargo_go(go)
    assert changed is True
    for needed in ("--- FAIL: TestCheckout", "expected 1999 got 0", "currency mismatch"):
        assert needed in out, f"go failure detail lost: {needed!r}"
    assert len(out) < len(go), "no compression achieved"


def test_compressor_massive_outputs():
    compressor = ContextCompressor(OptimizerConfig(profile=ProfileType.AGGRESSIVE))

    # 50,000 character output
    huge_output = "TEST LINE " + ("0123456789\n" * 4000)
    res = compressor.compress_command_output("npm test", huge_output)
    assert len(res.content) <= 3000
    assert res.ratio_pct > 80
    assert "sıkıştırıldı" in res.content
