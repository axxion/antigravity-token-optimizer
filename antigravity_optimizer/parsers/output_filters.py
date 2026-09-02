"""
Output filters for command execution (pytest, jest/npm, git, linter, compiler).
"""

from __future__ import annotations

import re
from typing import Tuple


class OutputFilters:
    @staticmethod
    def filter_pytest(output: str) -> Tuple[str, bool]:
        """Compresses pytest outputs preserving failure summaries and tracebacks."""
        lines = output.splitlines()
        if len(lines) <= 15:
            return output, False

        kept_lines = []
        in_failure = False
        summary_found = False

        for line in lines:
            # Detect failure sections
            if "=== FAILURES ===" in line or "=== ERRORS ===" in line:
                in_failure = True
                kept_lines.append(line)
                continue

            if re.search(r"={3,}\s*(short test summary|.*failed.*in|.*passed.*in)\s*={3,}", line, re.I):
                in_failure = False
                summary_found = True
                kept_lines.append(line)
                continue

            if in_failure or summary_found:
                kept_lines.append(line)
            elif "FAILED " in line or "ERROR " in line:
                kept_lines.append(line)
            elif "passed in " in line or "failed in " in line:
                kept_lines.append(line)

        if len(kept_lines) >= 3:
            return "\n".join(kept_lines), True
        return output, False

    @staticmethod
    def filter_npm_jest(output: str) -> Tuple[str, bool]:
        """Compresses npm test / jest outputs, keeping failed test suites and summary."""
        lines = output.splitlines()
        if len(lines) <= 20:
            return output, False

        kept = []
        in_fail = False
        for line in lines:
            if "FAIL " in line or "● " in line:
                in_fail = True
                kept.append(line)
            elif "PASS " in line:
                in_fail = False
            elif in_fail:
                kept.append(line)
            elif "Tests:" in line or "Test Suites:" in line or "Snapshots:" in line:
                kept.append(line)

        if len(kept) >= 2:
            return "\n".join(kept), True
        return output, False

    @staticmethod
    def filter_cargo_go(output: str) -> Tuple[str, bool]:
        """Compresses cargo test and go test outputs."""
        lines = output.splitlines()
        if len(lines) <= 15:
            return output, False

        kept = []
        for line in lines:
            if "FAILED" in line or "FAIL:" in line or "error[" in line or "--- FAIL:" in line:
                kept.append(line)
            elif "test result:" in line or "FAIL\t" in line or "ok\t" in line:
                kept.append(line)

        if len(kept) >= 1:
            return "\n".join(kept), True
        return output, False

    @staticmethod
    def filter_git_status_log(output: str) -> Tuple[str, bool]:
        """Compresses verbose git log or status."""
        lines = output.splitlines()
        if len(lines) > 25:
            header = lines[:15]
            tail = lines[-5:]
            compact = header + [f"\n... [{len(lines) - 20} satır git çıktısı sıkıştırıldı] ...\n"] + tail
            return "\n".join(compact), True
        return output, False

    @staticmethod
    def filter_generic_output(output: str, max_chars: int = 4000) -> str:
        """Generic head/tail trimmer for large command outputs."""
        if len(output) <= max_chars:
            return output

        head_len = int(max_chars * 0.6)
        tail_len = int(max_chars * 0.35)

        head = output[:head_len]
        tail = output[-tail_len:]
        omitted = len(output) - head_len - tail_len

        return f"{head}\n\n... [Gereksiz {omitted:,} karakter sıkıştırıldı] ...\n\n{tail}"
