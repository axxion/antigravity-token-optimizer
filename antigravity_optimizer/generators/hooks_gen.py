"""
Generates Antigravity Lifecycle Hooks (.agents/hooks.json).
"""

from __future__ import annotations

import json
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
        target_dir = Path(target_dir).resolve()
        agents_dir = target_dir / ".agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        hooks_file = agents_dir / "hooks.json"
        existing = {}
        if hooks_file.exists():
            try:
                existing = json.loads(hooks_file.read_text(encoding="utf-8"))
            except Exception:
                existing = {}

        new_hooks = cls.generate_hooks_dict(config)
        existing.update(new_hooks)

        hooks_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
        return hooks_file
