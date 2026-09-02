"""
Generates Antigravity Skill (.agents/skills/token-optimizer/SKILL.md).
"""

from __future__ import annotations

from pathlib import Path
from antigravity_optimizer.core.config import OptimizerConfig

SKILL_TEMPLATE = """---
name: token-optimizer
description: >-
  Antigravity Token & Context Optimization Suite. Use this skill when the user asks to
  reduce token usage, audit context bloat, inspect code skeletons, or compress command outputs.
---

# Antigravity Token Optimizer Skill

Bu yetenek (skill), Antigravity oturumlarınızda bağlam israfını en aza indirmek ve günlük kotanızı korumak için tasarlanmıştır.

## 🛠️ Temel İşlemler

### 1. Token & Bağlam Denetimi (Audit)
Projedeki token şişkinliğini, büyük dosyaları ve bellek eksikliklerini taramak için:
```bash
antigravity-optimizer audit .
```

### 2. Büyük Dosyaların Kod İskeletini Çıkarma (Skeleton)
Bir dosyanın içini tamamen okumadan sadece sınıf ve metot imzalarını görmek için:
```bash
antigravity-optimizer skeleton <dosya_yolu>
```

### 3. Komut Çıktılarını Sıkıştırma (Compress)
Uzun test veya git loglarını özetlemek için:
```bash
antigravity-optimizer compress "pytest tests/"
```

### 4. Optimizasyon Profilini Değiştirme
```bash
antigravity-optimizer install --profile aggressive   # Maksimum tasarruf
antigravity-optimizer install --profile balanced     # Önerilen dengeli profil
antigravity-optimizer install --profile developer    # Detaylı loglama
```
"""


class SkillsGenerator:
    @classmethod
    def install(cls, target_dir: Path, config: OptimizerConfig) -> Path:
        target_dir = Path(target_dir).resolve()
        skill_dir = target_dir / ".agents" / "skills" / "token-optimizer"
        skill_dir.mkdir(parents=True, exist_ok=True)

        file_path = skill_dir / "SKILL.md"
        file_path.write_text(SKILL_TEMPLATE, encoding="utf-8")
        return file_path
