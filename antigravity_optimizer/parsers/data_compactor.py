"""
Structured Data & Tabular Payload Compactor.
Deduplicates repetitive dictionary keys in object collections, strips null/empty fields,
and serializes into a compact column-oriented representation.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple


class DataCompactor:
    @staticmethod
    def strip_empty_fields(data: Any) -> Any:
        """Recursively purges nulls and empty elements from structures."""
        if isinstance(data, dict):
            return {
                k: DataCompactor.strip_empty_fields(v)
                for k, v in data.items()
                if v is not None and v != "" and v != [] and v != {}
            }
        elif isinstance(data, list):
            return [
                DataCompactor.strip_empty_fields(item)
                for item in data
                if item is not None and item != "" and item != [] and item != {}
            ]
        return data

    @staticmethod
    def tabularize_collection(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Converts array of dictionaries [{k1: v1, k2: v2}, ...] into column-oriented schema:
        {"__compact_table__": True, "columns": [k1, k2], "rows": [[v1, v2], ...]}
        """
        if not records or not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
            return {"data": records}

        # Collect unique keys maintaining insertion order
        columns: List[str] = []
        for r in records:
            for k in r.keys():
                if k not in columns:
                    columns.append(k)

        rows: List[List[Any]] = []
        for r in records:
            row = [r.get(col) for col in columns]
            rows.append(row)

        return {
            "__compact_table__": True,
            "columns": columns,
            "rows": rows,
            "total_records": len(rows),
        }

    @classmethod
    def compact(cls, payload_text: str, max_chars: int = 4000) -> Tuple[str, int, int]:
        """
        Compacts raw structured text.
        Returns: (compacted_str, original_length, compressed_length)
        """
        orig_len = len(payload_text)
        try:
            parsed = json.loads(payload_text)
        except Exception:
            return payload_text, orig_len, orig_len

        cleaned = cls.strip_empty_fields(parsed)

        if isinstance(cleaned, list) and len(cleaned) >= 2 and all(isinstance(x, dict) for x in cleaned):
            compacted = cls.tabularize_collection(cleaned)
        elif isinstance(cleaned, dict):
            compacted = {}
            for k, v in cleaned.items():
                if isinstance(v, list) and len(v) >= 2 and all(isinstance(x, dict) for x in v):
                    compacted[k] = cls.tabularize_collection(v)
                else:
                    compacted[k] = v
        else:
            compacted = cleaned

        compressed_str = json.dumps(compacted, ensure_ascii=False, separators=(",", ":"))
        comp_len = len(compressed_str)

        return compressed_str, orig_len, comp_len
