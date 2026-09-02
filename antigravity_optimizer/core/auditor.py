"""
Project Token Bloat and Context Quality Auditor.
Analyzes repositories, detects token waste patterns, and generates an optimization audit report.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class WasteFinding:
    category: str
    severity: str  # "HIGH", "MEDIUM", "LOW"
    title: str
    description: str
    potential_savings_tokens: int
    recommendation: str


@dataclass
class AuditReport:
    project_path: str
    total_files: int
    total_lines: int
    large_files_count: int
    grade: str  # S, A, B, C, D, F
    score_pct: int
    findings: List[WasteFinding] = field(default_factory=list)
    estimated_session_waste_tokens: int = 0
    projected_savings_pct: int = 0


EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
    ".pytest_cache",
}


class ProjectAuditor:
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()

    def audit(self) -> AuditReport:
        total_files = 0
        total_lines = 0
        large_files: List[Tuple[str, int]] = []
        findings: List[WasteFinding] = []

        # 1. Scan files
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".git")]
            for f in files:
                p = Path(root) / f
                ext = p.suffix.lower()
                if ext in (".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".cpp", ".md", ".json"):
                    try:
                        size = p.stat().st_size
                        if size > 1_000_000:
                            continue
                        lines = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
                        total_files += 1
                        total_lines += lines
                        if lines > 250:
                            rel = p.relative_to(self.project_path).as_posix()
                            large_files.append((rel, lines))
                    except Exception:
                        continue

        # 2. Analyze large files
        if len(large_files) >= 5:
            waste_est = len(large_files) * 2500
            findings.append(
                WasteFinding(
                    category="filesystem",
                    severity="HIGH" if len(large_files) > 10 else "MEDIUM",
                    title=f"{len(large_files)} adet büyük dosya (>250 satır) tespit edildi",
                    description=(
                        "Bu dosyalar tek seferde okunduğunda bağlam penceresini gereksiz yere doldurur. "
                        "Örnekler: " + ", ".join(f"{f} ({l} satır)" for f, l in large_files[:3])
                    ),
                    potential_savings_tokens=waste_est,
                    recommendation="Cerrahi satır aralıklı okuma (view_file) ve AST iskeleti (code_skeleton) kullanın.",
                )
            )

        # 3. Check for Antigravity rules and GEMINI.md
        rules_dir = self.project_path / ".agents" / "rules"
        gemini_md = self.project_path / "GEMINI.md"
        has_optimizer_rule = False

        if rules_dir.exists():
            for rf in rules_dir.glob("*.md"):
                if "token" in rf.name.lower() or "optimiz" in rf.name.lower():
                    has_optimizer_rule = True

        if not has_optimizer_rule:
            findings.append(
                WasteFinding(
                    category="prompt",
                    severity="HIGH",
                    title="Token Optimizasyon Kuralı (.agents/rules) Tanımlı Değil",
                    description="Ajan varsayılan olarak uzun özetler ve dolgu cümleleri üretebilir.",
                    potential_savings_tokens=8000,
                    recommendation="'antigravity-optimizer install' ile yalın iletişim ve cerrahi düzenleme kurallarını ekleyin.",
                )
            )

        # 4. Check for external memory (BOARD.md / MEMORY.md)
        has_memory = (self.project_path / "BOARD.md").exists() or (self.project_path / "MEMORY.md").exists()
        if not has_memory:
            findings.append(
                WasteFinding(
                    category="memory",
                    severity="MEDIUM",
                    title="Kalıcı Harici Bellek Dosyası Bulunamadı",
                    description="Görevler ve durum modelin bağlam penceresinde taşınıyor, sıkıştırma anında unutulabilir.",
                    potential_savings_tokens=12000,
                    recommendation="BOARD.md veya MEMORY.md kurarak durumu diskte tutun.",
                )
            )

        # 5. Calculate Score and Grade
        total_waste = sum(f.potential_savings_tokens for f in findings)
        penalty = min(80, len(findings) * 20 + len(large_files) * 2)
        score_pct = max(20, 100 - penalty)

        if score_pct >= 90:
            grade = "S"
        elif score_pct >= 80:
            grade = "A"
        elif score_pct >= 70:
            grade = "B"
        elif score_pct >= 60:
            grade = "C"
        elif score_pct >= 45:
            grade = "D"
        else:
            grade = "F"

        savings_pct = min(75, 25 + len(findings) * 12)

        return AuditReport(
            project_path=str(self.project_path),
            total_files=total_files,
            total_lines=total_lines,
            large_files_count=len(large_files),
            grade=grade,
            score_pct=score_pct,
            findings=findings,
            estimated_session_waste_tokens=total_waste,
            projected_savings_pct=savings_pct,
        )
