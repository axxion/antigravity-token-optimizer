"""
Antigravity Token Optimizer Configuration Models & Profiles.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class ProfileType(str, Enum):
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"
    DEVELOPER = "developer"
    CUSTOM = "custom"


@dataclass
class OptimizationFeature:
    id: str
    name: str
    description: str
    why_needed: str
    estimated_savings_pct: int
    enabled: bool = True
    category: str = "general"


DEFAULT_FEATURES: List[OptimizationFeature] = [
    OptimizationFeature(
        id="lean_prompt",
        name="Yalın İletişim ve Sıfır Dolgu (Lean Prompt)",
        description="Nezaket cümlelerini, giriş-gelişme tekrarlarını ve gereksiz özetleri engeller.",
        why_needed="Her yanıtta 100-300 token'lık gereksiz tamamlama (completion) israfını keser.",
        estimated_savings_pct=25,
        enabled=True,
        category="prompt",
    ),
    OptimizationFeature(
        id="surgical_edits",
        name="Cerrahi Dosya Düzenleme (Surgical Edits)",
        description="Dosyayı baştan sona yeniden yazmayı yasaklar; replace_file_content ve satır aralıklı okumayı zorunlu kılar.",
        why_needed="500 satırlık dosyada 2 satır değiştirmek için tüm dosyayı baştan üretme israfını önler.",
        estimated_savings_pct=55,
        enabled=True,
        category="filesystem",
    ),
    OptimizationFeature(
        id="code_skeleton",
        name="AST Kod İskeleti Çıkarıcı (Code Skeletons)",
        description="Büyük dosyalarda fonksiyon/sınıf gövdelerini atlayıp yalnızca imzaları ve tipleri bağlama alır.",
        why_needed="Kod tabanı keşfinde binlerce satırlık implementasyon detayını bağlama yüklemeyi engeller.",
        estimated_savings_pct=70,
        enabled=True,
        category="filesystem",
    ),
    OptimizationFeature(
        id="command_compression",
        name="Komut & Test Çıktısı Filtreleme (Command Compressor)",
        description="pytest, npm test, git log çıktılarındaki geçen test gürültüsünü eler, sadece hata ve özetleri tutar.",
        why_needed="Başarılı 200 testin satır satır loglarını bağlama ekleyip pencereyi şişirmeyi engeller.",
        estimated_savings_pct=60,
        enabled=True,
        category="execution",
    ),
    OptimizationFeature(
        id="search_dedup",
        name="Arama & Grep Sıkıştırma (Search Deduplication)",
        description="Grep sonuçlarında uzun satırları keser (>120 char) ve dosya başı eşleşme tavanı uygular.",
        why_needed="Gereksiz geniş regex aramalarının tüm bağlamı tüketmesini engeller.",
        estimated_savings_pct=45,
        enabled=True,
        category="search",
    ),
    OptimizationFeature(
        id="context_memory",
        name="Harici Bellek & Kontrol Noktaları (Context Checkpoints)",
        description="Görev durumlarını ve mimari kararları diskte (BOARD.md/MEMORY.md) saklar.",
        why_needed="Modelin hafızasını bağlam içinde tutarak token yakmasını ve sıkıştırma sonrası unutmasını engeller.",
        estimated_savings_pct=65,
        enabled=True,
        category="memory",
    ),
]


@dataclass
class OptimizerConfig:
    profile: ProfileType = ProfileType.BALANCED
    features: Dict[str, bool] = field(default_factory=dict)
    max_view_lines: int = 150
    max_command_output_chars: int = 4000
    max_grep_matches: int = 30
    skeleton_threshold_lines: int = 120
    install_scope: str = "workspace"  # "workspace" (.agents/) or "global" (~/.gemini/config/)

    def __post_init__(self):
        prof = self.profile
        if not self.features:
            if prof == ProfileType.AGGRESSIVE:
                self.features = {f.id: True for f in DEFAULT_FEATURES}
            elif prof == ProfileType.BALANCED:
                self.features = {
                    "lean_prompt": True,
                    "surgical_edits": True,
                    "code_skeleton": True,
                    "command_compression": True,
                    "search_dedup": True,
                    "context_memory": True,
                }
            elif prof == ProfileType.DEVELOPER:
                self.features = {
                    "lean_prompt": True,
                    "surgical_edits": True,
                    "code_skeleton": False,
                    "command_compression": False,
                    "search_dedup": True,
                    "context_memory": True,
                }
            elif prof == ProfileType.CUSTOM:
                self.features = {f.id: f.enabled for f in DEFAULT_FEATURES}

        # Apply profile-specific defaults if not customized
        if prof == ProfileType.AGGRESSIVE:
            if self.max_command_output_chars == 4000:
                self.max_command_output_chars = 2500
            if self.max_view_lines == 150:
                self.max_view_lines = 100
            if self.max_grep_matches == 30:
                self.max_grep_matches = 20
        elif prof == ProfileType.DEVELOPER:
            if self.max_command_output_chars == 4000:
                self.max_command_output_chars = 8000
            if self.max_view_lines == 150:
                self.max_view_lines = 250
            if self.max_grep_matches == 30:
                self.max_grep_matches = 50

    def is_feature_enabled(self, feature_id: str) -> bool:
        return self.features.get(feature_id, False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile.value if isinstance(self.profile, ProfileType) else self.profile,
            "features": self.features,
            "max_view_lines": self.max_view_lines,
            "max_command_output_chars": self.max_command_output_chars,
            "max_grep_matches": self.max_grep_matches,
            "skeleton_threshold_lines": self.skeleton_threshold_lines,
            "install_scope": self.install_scope,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> OptimizerConfig:
        raw_prof = data.get("profile", "balanced")
        try:
            profile = ProfileType(raw_prof)
        except ValueError:
            profile = ProfileType.BALANCED

        return cls(
            profile=profile,
            features=data.get("features", {}),
            max_view_lines=data.get("max_view_lines", 150),
            max_command_output_chars=data.get("max_command_output_chars", 4000),
            max_grep_matches=data.get("max_grep_matches", 30),
            skeleton_threshold_lines=data.get("skeleton_threshold_lines", 120),
            install_scope=data.get("install_scope", "workspace"),
        )
