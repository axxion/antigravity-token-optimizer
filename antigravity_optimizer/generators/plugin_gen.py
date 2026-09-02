"""
Generates Antigravity Plugin bundle (.agents/plugins/token-optimizer/).
"""

from __future__ import annotations

import json
from pathlib import Path
from antigravity_optimizer.core.config import OptimizerConfig
from antigravity_optimizer.generators.rules_gen import RulesGenerator
from antigravity_optimizer.generators.skills_gen import SkillsGenerator
from antigravity_optimizer.generators.hooks_gen import HooksGenerator


class PluginGenerator:
    @classmethod
    def install(cls, target_dir: Path, config: OptimizerConfig) -> Path:
        target_dir = Path(target_dir).resolve()
        plugin_dir = target_dir / ".agents" / "plugins" / "token-optimizer"
        plugin_dir.mkdir(parents=True, exist_ok=True)

        # 1. plugin.json
        manifest = {
            "name": "token-optimizer",
            "version": "1.0.0",
            "description": "Token & Context Optimization Plugin for Google Antigravity",
            "profile": config.profile.value,
        }
        (plugin_dir / "plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # 2. rules
        rules_dir = plugin_dir / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        (rules_dir / "token_optimization.md").write_text(
            RulesGenerator.generate_rules_content(config), encoding="utf-8"
        )

        # 3. skills
        skills_dir = plugin_dir / "skills" / "token-optimizer"
        skills_dir.mkdir(parents=True, exist_ok=True)
        from antigravity_optimizer.generators.skills_gen import SKILL_TEMPLATE
        (skills_dir / "SKILL.md").write_text(SKILL_TEMPLATE, encoding="utf-8")

        # 4. hooks
        hooks_data = HooksGenerator.generate_hooks_dict(config)
        (plugin_dir / "hooks.json").write_text(
            json.dumps(hooks_data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        return plugin_dir
