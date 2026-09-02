"""
Lossless Context Expansion & Artifact Cache Engine.
Stores raw uncompressed tool outputs and provides deterministic reference restoration.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional


class ContextBufferStore:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = (cache_dir or Path(".agents") / ".cache" / "buffer_store").resolve()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def store(self, raw_content: str, tag: str = "output") -> str:
        """
        Stores original uncompressed content and returns unique reference identifier.
        Format: ref_4f89a1bc
        """
        digest = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()[:12]
        ref_id = f"ref_{digest}"
        store_file = self.cache_dir / f"{ref_id}.json"

        payload = {
            "ref_id": ref_id,
            "tag": tag,
            "char_count": len(raw_content),
            "content": raw_content,
        }
        store_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return ref_id

    def retrieve(self, ref_id: str) -> Optional[str]:
        """Restores uncompressed content from reference token."""
        store_file = self.cache_dir / f"{ref_id}.json"
        if not store_file.exists():
            return None
        try:
            data = json.loads(store_file.read_text(encoding="utf-8"))
            return data.get("content")
        except Exception:
            return None
