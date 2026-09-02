"""
Tests for Generator modules (Rules, Skills, Hooks, Plugin).
"""

import json
import tempfile
from pathlib import Path
from antigravity_optimizer.core.config import OptimizerConfig, ProfileType
from antigravity_optimizer.generators.hooks_gen import HooksGenerator
from antigravity_optimizer.generators.plugin_gen import PluginGenerator
from antigravity_optimizer.generators.rules_gen import RulesGenerator
from antigravity_optimizer.generators.skills_gen import SkillsGenerator


def test_generators_installation():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir).resolve()
        cfg = OptimizerConfig(profile=ProfileType.BALANCED)

        # 1. Rules
        rules_p = RulesGenerator.install(root, cfg)
        assert rules_p.exists()
        content = rules_p.read_text(encoding="utf-8")
        assert "Lean Prompt" in content
        assert "Surgical Edits" in content

        # 2. Skill
        skill_p = SkillsGenerator.install(root, cfg)
        assert skill_p.exists()
        skill_content = skill_p.read_text(encoding="utf-8")
        assert "name: token-optimizer" in skill_content

        # 3. Hooks
        hooks_p = HooksGenerator.install(root, cfg)
        assert hooks_p.exists()
        hooks_json = json.loads(hooks_p.read_text(encoding="utf-8"))
        assert "token-optimizer-guard" in hooks_json

        # 4. Plugin
        plugin_dir = PluginGenerator.install(root, cfg)
        assert (plugin_dir / "plugin.json").exists()
        manifest = json.loads((plugin_dir / "plugin.json").read_text(encoding="utf-8"))
        assert manifest["name"] == "token-optimizer"
