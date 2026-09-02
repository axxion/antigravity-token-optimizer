"""
Generates Antigravity Lifecycle Hooks (.agents/hooks.json).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from antigravity_optimizer.core.config import OptimizerConfig


class HooksGenerator:
    @staticmethod
    def generate_hooks_dict(config: OptimizerConfig) -> dict:
        hooks_data = {
            "token-optimizer-guard": {
                "enabled": True,
                "PreInvocation": [
                    {
                        "type": "command",
                        "command": "python -c \"import json; print(json.dumps({'injectSteps': [{'ephemeralMessage': '⚡ Token Optimizer Aktif ("
                        + config.profile.value.upper()
                        + "): Cerrahi düzenleme yapın ve yanıtları yalın tutun.'}]}))\"",
                    }
                ],
            }
        }
        return hooks_data

    @classmethod
    def install(cls, target_dir: Path, config: OptimizerConfig) -> Path:
        """Merges this tool's hook into the project's .agents/hooks.json.

        Any pre-existing file that cannot be merged (invalid JSON, JSONC with comments,
        or a top-level array instead of an object) is preserved as a timestamped .bak
        beside it rather than being discarded, and the caller is told. Silently dropping
        a user's own hooks would be unrecoverable data loss.
        """
        target_dir = Path(target_dir).resolve()
        agents_dir = target_dir / ".agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        hooks_file = agents_dir / "hooks.json"
        existing = {}
        backup_path = None

        if hooks_file.exists():
            raw = hooks_file.read_text(encoding="utf-8")
            unmergeable_reason = None
            try:
                parsed = json.loads(raw)
            except ValueError as exc:
                unmergeable_reason = f"geçersiz JSON ({exc})"
            else:
                if isinstance(parsed, dict):
                    existing = parsed
                else:
                    unmergeable_reason = (
                        f"beklenen JSON nesnesi yerine {type(parsed).__name__} bulundu"
                    )

            if unmergeable_reason is not None:
                backup_path = cls._backup(hooks_file, raw)
                # ASCII-only: this runs as a library too, where stdout may still be on a
                # legacy code page that cannot encode symbols.
                print(
                    f"  [!] Mevcut hooks.json birlestirilemedi: {unmergeable_reason}.\n"
                    f"      Orijinal dosya korundu: {backup_path.name}"
                )

        new_hooks = cls.generate_hooks_dict(config)
        existing.update(new_hooks)

        hooks_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
        return hooks_file

    @staticmethod
    def _backup(hooks_file: Path, raw: str) -> Path:
        """Writes the unmergeable original next to the target, without overwriting an
        earlier backup."""
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        candidate = hooks_file.with_name(f"hooks.json.{stamp}.bak")
        counter = 1
        while candidate.exists():
            candidate = hooks_file.with_name(f"hooks.json.{stamp}-{counter}.bak")
            counter += 1
        candidate.write_text(raw, encoding="utf-8")
        return candidate
