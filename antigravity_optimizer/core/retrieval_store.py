"""
Lossless Context Expansion & Artifact Cache Engine.
Stores raw uncompressed tool outputs and provides deterministic reference restoration.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Optional

# A reference is always produced by store() as "ref_" + 12 hex characters. Anything else
# is not a reference this store issued, so it is rejected before touching the filesystem.
REF_ID_PATTERN = re.compile(r"^ref_[0-9a-f]{12}$")


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
        """Restores uncompressed content from a reference token.

        `ref_id` reaches this method from user/agent input, so it is validated against the
        exact shape store() issues before being used as a path component. Without that,
        a value such as "../../../etc/config" resolves outside the cache directory and
        turns this method into an arbitrary-file reader.
        """
        if not isinstance(ref_id, str) or not REF_ID_PATTERN.match(ref_id):
            return None

        store_file = (self.cache_dir / f"{ref_id}.json").resolve()

        # Defence in depth: even with a validated id, confirm the resolved path really is
        # inside the cache directory before reading it.
        try:
            store_file.relative_to(self.cache_dir)
        except ValueError:
            return None

        if not store_file.is_file():
            return None
        try:
            data = json.loads(store_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        content = data.get("content") if isinstance(data, dict) else None
        return content if isinstance(content, str) else None
