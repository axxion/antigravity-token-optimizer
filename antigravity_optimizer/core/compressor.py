"""
Unified token and context compressor engine.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from antigravity_optimizer.core.config import OptimizerConfig
from antigravity_optimizer.core.retrieval_store import ContextBufferStore
from antigravity_optimizer.parsers.ast_skeleton import ASTSkeletonExtractor, SkeletonResult
from antigravity_optimizer.parsers.data_compactor import DataCompactor
from antigravity_optimizer.parsers.output_filters import OutputFilters


@dataclass
class CompressionReport:
    original_size: int
    compressed_size: int
    saved_tokens_est: int
    ratio_pct: int
    content: str
    ref_id: Optional[str] = None


class ContextCompressor:
    def __init__(self, config: Optional[OptimizerConfig] = None, cache_dir: Optional[Path] = None):
        self.config = config or OptimizerConfig()
        self.store = ContextBufferStore(cache_dir=cache_dir)

    def compress_command_output(self, command: str, raw_output: str) -> CompressionReport:
        """Compresses command output using specialized filters and caches raw output for lossless expansion."""
        if not self.config.is_feature_enabled("command_compression"):
            return CompressionReport(
                original_size=len(raw_output),
                compressed_size=len(raw_output),
                saved_tokens_est=0,
                ratio_pct=0,
                content=raw_output,
            )

        cmd_lower = command.lower()
        compressed = raw_output

        if "pytest" in cmd_lower or "python -m unittest" in cmd_lower:
            compressed, _ = OutputFilters.filter_pytest(raw_output)
        elif "npm test" in cmd_lower or "jest" in cmd_lower:
            compressed, _ = OutputFilters.filter_npm_jest(raw_output)
        elif "cargo test" in cmd_lower or "go test" in cmd_lower:
            compressed, _ = OutputFilters.filter_cargo_go(raw_output)
        elif "git status" in cmd_lower or "git log" in cmd_lower:
            compressed, _ = OutputFilters.filter_git_status_log(raw_output)

        # Apply maximum character limit
        compressed = OutputFilters.filter_generic_output(
            compressed, max_chars=self.config.max_command_output_chars
        )

        ref_id = None
        if len(raw_output) > len(compressed) + 500:
            ref_id = self.store.store(raw_output, tag=command)
            compressed += f"\n\n[Orijinal cikti saklandi: {ref_id} ('antigravity-optimizer expand {ref_id}' ile acilabilir)]"

        orig_len = len(raw_output)
        comp_len = len(compressed)
        ratio = max(0, int((1.0 - (comp_len / max(1, orig_len))) * 100))
        saved_tokens = max(0, (orig_len - comp_len) // 4)

        return CompressionReport(
            original_size=orig_len,
            compressed_size=comp_len,
            saved_tokens_est=saved_tokens,
            ratio_pct=ratio,
            content=compressed,
            ref_id=ref_id,
        )

    def compress_structured_data(self, raw_json_text: str) -> CompressionReport:
        """Compacts structured JSON datasets using DataCompactor."""
        compacted, orig_len, comp_len = DataCompactor.compact(raw_json_text)
        ratio = max(0, int((1.0 - (comp_len / max(1, orig_len))) * 100))
        saved_tokens = max(0, (orig_len - comp_len) // 4)
        return CompressionReport(
            original_size=orig_len,
            compressed_size=comp_len,
            saved_tokens_est=saved_tokens,
            ratio_pct=ratio,
            content=compacted,
        )

    # Alias for backward compatibility
    compress_json = compress_structured_data

    def extract_file_skeleton(self, file_content: str, file_path: Optional[str] = None) -> SkeletonResult:
        """Extracts class and method signatures."""
        return ASTSkeletonExtractor.extract_skeleton(file_content, file_path=file_path)

    def compress_search_results(self, search_results: str) -> CompressionReport:
        """Truncates verbose search lines and deduplicates repetitive hits."""
        if not self.config.is_feature_enabled("search_dedup"):
            return CompressionReport(
                original_size=len(search_results),
                compressed_size=len(search_results),
                saved_tokens_est=0,
                ratio_pct=0,
                content=search_results,
            )

        lines = search_results.splitlines()
        if len(lines) <= self.config.max_grep_matches:
            return CompressionReport(
                original_size=len(search_results),
                compressed_size=len(search_results),
                saved_tokens_est=0,
                ratio_pct=0,
                content=search_results,
            )

        truncated_lines = []
        for line in lines[: self.config.max_grep_matches]:
            if len(line) > 130:
                truncated_lines.append(line[:120] + " ... [satır kesildi]")
            else:
                truncated_lines.append(line)

        omitted = len(lines) - self.config.max_grep_matches
        truncated_lines.append(f"\n... [{omitted} ek eşleşme bağlam tasarrufu için gizlendi] ...")
        compact_str = "\n".join(truncated_lines)

        orig_len = len(search_results)
        comp_len = len(compact_str)
        ratio = max(0, int((1.0 - (comp_len / max(1, orig_len))) * 100))
        saved_tokens = max(0, (orig_len - comp_len) // 4)

        return CompressionReport(
            original_size=orig_len,
            compressed_size=comp_len,
            saved_tokens_est=saved_tokens,
            ratio_pct=ratio,
            content=compact_str,
        )
