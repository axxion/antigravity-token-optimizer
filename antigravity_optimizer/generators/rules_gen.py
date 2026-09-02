"""
Generates Antigravity Rule markdown files (.agents/rules/token_optimization.md or GEMINI.md).
"""

from __future__ import annotations

from pathlib import Path
from antigravity_optimizer.core.config import OptimizerConfig


class RulesGenerator:
    @staticmethod
    def generate_rules_content(config: OptimizerConfig) -> str:
        sections = [
            "# Antigravity Token & Context Optimization Rules",
            "",
            "> [!NOTE]",
            f"> Bu kural dosyası **Antigravity Token Optimizer** (Profil: `{config.profile.value.upper()}`) tarafından otomatik oluşturulmuştur.",
            "",
            "## 1. Temel Davranış İlkeleri",
            "",
        ]

        if config.is_feature_enabled("lean_prompt"):
            sections.extend([
                "### A. Yalın İletişim & Sıfır Dolgu (Lean Prompt)",
                "- **Gereksiz nezaketi ve dolgu cümlelerini atlayın:** 'Elbette!', 'Anladım', 'Şimdi sizin için yapıyorum' gibi açılış cümleleri kurmayın; doğrudan çözüme ve koda geçin.",
                "- **Talimatları tekrar etmeyin:** Kullanıcının verdiği emri kendi cümlelerinizle özetlemeyin.",
                "- **Kısa ve öz yanıt verin:** Değişiklikleri 1-2 cümlelik odaklanmış maddelerle açıklayın.",
                "",
            ])

        if config.is_feature_enabled("surgical_edits"):
            sections.extend([
                "### B. Cerrahi Dosya Düzenleme & Dilimleme (Surgical Edits)",
                "- **Tüm dosyayı baştan yazmayın (`write_file` yasağı):** Mevcut bir dosyada değişiklik yaparken yalnızca değişen bloğu hedefleyen cerrahi araçları (`replace_file_content` veya `replace_content`) kullanın.",
                f"- **Gereksiz tam dosya okuması yapmayın:** Büyük dosyalarda daima satır aralığı (`start_line`, `end_line`, max {config.max_view_lines} satır) belirtin.",
                "- **Sadece ilgili bölümleri okuyun:** Bir fonksiyonu incelemek için 500 satırlık dosyanın tamamını bağlama çekmeyin.",
                "",
            ])

        if config.is_feature_enabled("code_skeleton"):
            sections.extend([
                "### C. AST Kod İskeletleri (Code Skeletons)",
                f"- **{config.skeleton_threshold_lines} satırı aşan büyük dosyalarda:** İlk incelemede implementasyon detaylarını değil; sınıf, metot ve tip imzalarını (skeleton) inceleyin.",
                "- Yalnızca düzenlenecek metodun gövdesini bağlama dahil edin.",
                "",
            ])

        if config.is_feature_enabled("command_compression"):
            sections.extend([
                "### D. Komut & Test Çıktısı Optimizasyonu",
                f"- Uzun test çıktılarında (`pytest`, `npm test`) geçen testlerin detaylarını atlayın; yalnızca başarısız test yığınlarını (failures) ve özet sayıları raporlayın.",
                f"- Komut çıktılarında maksimum {config.max_command_output_chars} karakter sınırını aşmayın.",
                "",
            ])

        if config.is_feature_enabled("search_dedup"):
            sections.extend([
                "### E. Arama ve Grep Disiplini",
                f"- Grep ve dosya aramalarında tek seferde maksimum {config.max_grep_matches} eşleşme inceleyin.",
                "- Çok geniş desenler (örn: `.*`) yerine spesifik sembol adlarıyla arama yapın.",
                "",
            ])

        if config.is_feature_enabled("context_memory"):
            sections.extend([
                "### F. Harici Bellek & Kontrol Noktaları",
                "- Durum, görev listesi ve mimari kararları modelin geçici konuşma geçmişinde tutmak yerine `BOARD.md`, `LEDGER.md` veya `MEMORY.md` dosyalarına kaydedin.",
                "- Sıkıştırma (compaction) durumlarında görev geçmişini bu dosyalardan geri yükleyin.",
                "",
            ])

        return "\n".join(sections).strip() + "\n"

    @classmethod
    def install(cls, target_dir: Path, config: OptimizerConfig) -> Path:
        target_dir = Path(target_dir).resolve()
        rules_dir = target_dir / ".agents" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)

        file_path = rules_dir / "token_optimization.md"
        content = cls.generate_rules_content(config)
        file_path.write_text(content, encoding="utf-8")
        return file_path
