"""
Tests for ProjectAuditor.
"""

import tempfile
from pathlib import Path
from antigravity_optimizer.core.auditor import ProjectAuditor


def test_project_auditor():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir).resolve()

        # Create dummy project files
        (root / "src").mkdir(parents=True)
        # Create a large file
        (root / "src" / "big_file.py").write_text("\n".join(f"# line {i}" for i in range(300)), encoding="utf-8")
        (root / "src" / "small.py").write_text("print('hello')", encoding="utf-8")

        auditor = ProjectAuditor(root)
        report = auditor.audit()

        assert report.total_files == 2
        assert report.large_files_count == 1
        assert report.grade in ("S", "A", "B", "C", "D", "F")
        assert len(report.findings) > 0
        assert report.projected_savings_pct > 0
