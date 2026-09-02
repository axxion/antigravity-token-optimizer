"""
Antigravity Token Optimizer CLI & Interactive Wizard.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from antigravity_optimizer.core.auditor import ProjectAuditor
from antigravity_optimizer.core.compressor import ContextCompressor
from antigravity_optimizer.core.config import (
    DEFAULT_FEATURES,
    OptimizerConfig,
    ProfileType,
)
from antigravity_optimizer.generators.hooks_gen import HooksGenerator
from antigravity_optimizer.generators.plugin_gen import PluginGenerator
from antigravity_optimizer.generators.rules_gen import RulesGenerator
from antigravity_optimizer.generators.skills_gen import SkillsGenerator


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def print_banner():
    banner = """
======================================================================
  ⚡ ANTIGRAVITY TOKEN OPTIMIZER (v1.0.0)
  Google Antigravity IDE & CLI Icin Token & Baglam Tasarruf Motoru
======================================================================
"""
    print(banner)


def cmd_audit(args) -> int:
    target = Path(args.path or ".").resolve()
    print_banner()
    print(f"\033[93m🔍 Proje taranıyor:\033[0m {target}\n")

    auditor = ProjectAuditor(target)
    report = auditor.audit()

    grade_colors = {
        "S": "\033[92m[S - Kusursuz]\033[0m",
        "A": "\033[92m[A - Çok İyi]\033[0m",
        "B": "\033[94m[B - İyi]\033[0m",
        "C": "\033[93m[C - Orta Seviye İsraf]\033[0m",
        "D": "\033[91m[D - Yüksek İsraf]\033[0m",
        "F": "\033[91m[F - Kritik Token İsrafı]\033[0m",
    }
    grade_str = grade_colors.get(report.grade, f"[{report.grade}]")

    print("=" * 65)
    print(f"  📊 DENETİM SONUCU: {grade_str}  (Sağlık Skoru: %{report.score_pct})")
    print("=" * 65)
    print(f"  - Toplam Taranan Kod Dosyası: {report.total_files:,}")
    print(f"  - Toplam Satır Sayısı:        {report.total_lines:,}")
    print(f"  - Büyük Dosya Sayısı (>250s): {report.large_files_count}")
    print(f"  - Tahmini Oturum İsrafı:     ~{report.estimated_session_waste_tokens:,} Token")
    print(f"  - Öngörülen Tasarruf Oranı:   ~%{report.projected_savings_pct}")
    print("=" * 65)

    if report.findings:
        print("\n\033[91m⚠️  Tespit Edilen İsraf Noktaları:\033[0m")
        for idx, f in enumerate(report.findings, start=1):
            print(f"\n  {idx}. [{f.severity}] \033[1m{f.title}\033[0m")
            print(f"     Neden: {f.description}")
            print(f"     💡 Çözüm: \033[92m{f.recommendation}\033[0m")
            print(f"     💰 Potansiyel Kazanç: ~{f.potential_savings_tokens:,} Token")
    else:
        print("\n\033[92m✨ Harika! Projenizde belirgin bir token israfı tespit edilmedi.\033[0m")

    print("\n" + "-" * 65)
    print("💡 \033[1mHızlı Kurulum:\033[0m 'antigravity-optimizer install --profile balanced'")
    print("-" * 65 + "\n")
    return 0


def cmd_install(args) -> int:
    target = Path(args.path or ".").resolve()
    profile_str = (args.profile or "balanced").lower()

    try:
        profile = ProfileType(profile_str)
    except ValueError:
        print(f"\033[91mHata:\033[0m Geçersiz profil '{profile_str}'. Seçenekler: aggressive, balanced, developer, custom")
        return 1

    config = OptimizerConfig(profile=profile)
    print_banner()
    print(f"\033[92m🚀 Kurulum Başlatılıyor...\033[0m")
    print(f"  Hedef Proje: {target}")
    print(f"  Seçilen Profil: \033[96m{profile.value.upper()}\033[0m\n")

    # Install Rules
    rules_path = RulesGenerator.install(target, config)
    print(f"  ✔ Antigravity Kuralları eklendi: {rules_path.relative_to(target)}")

    # Install Skill
    skills_path = SkillsGenerator.install(target, config)
    print(f"  ✔ Antigravity Skill eklendi:     {skills_path.relative_to(target)}")

    # Install Hooks
    hooks_path = HooksGenerator.install(target, config)
    print(f"  ✔ Antigravity Hooks eklendi:     {hooks_path.relative_to(target)}")

    # Install Plugin Bundle
    plugin_path = PluginGenerator.install(target, config)
    print(f"  ✔ Antigravity Plugin oluşturuldu: {plugin_path.relative_to(target)}")

    print("\n\033[92m✅ KURULUM BAŞARIYLA TAMAMLANDI!\033[0m")
    print("  Antigravity artık bu projede seçilen profil kurallarıyla çalışacak.")
    return 0


def cmd_setup(args) -> int:
    print_banner()
    target = Path(args.path or ".").resolve()
    print(f"🎯 \033[1mAntigravity Token Optimizasyon Kurulum Sihirbazı\033[0m\n")
    print("Lütfen projeniz için uygun bir optimizasyon profili seçin:\n")

    profiles_info = [
        ("1", "🚀 Aggressive", "Maksimum Tasarruf (~%60-%75)", "Sıkı token kotaları ve otonom döngüler için en agresif tasarruf."),
        ("2", "⚖️ Balanced  ", "Önerilen Denge   (~%45-%60)", "Geliştirici deneyimini bozmadan yüksek token tasarrufu sağlar (Önerilen)."),
        ("3", "🛠️ Developer ", "Hata Odaklı     (~%30-%45)", "Detaylı test loglarını ve stack trace'leri korur, gereksiz dolguları siler."),
    ]

    for key, name, savings, desc in profiles_info:
        print(f"  [\033[92m{key}\033[0m] \033[1m{name}\033[0m - \033[93m{savings}\033[0m")
        print(f"      {desc}\n")

    choice = input("Seçiminiz [1/2/3] (Varsayılan 2): ").strip() or "2"
    profile_map = {"1": ProfileType.AGGRESSIVE, "2": ProfileType.BALANCED, "3": ProfileType.DEVELOPER}
    selected_profile = profile_map.get(choice, ProfileType.BALANCED)

    config = OptimizerConfig(profile=selected_profile)
    print(f"\nSeçilen Profil: \033[96m{selected_profile.value.upper()}\033[0m")

    # Install
    RulesGenerator.install(target, config)
    SkillsGenerator.install(target, config)
    HooksGenerator.install(target, config)
    PluginGenerator.install(target, config)

    print(f"\n\033[92m✅ Antigravity Token Optimizer başarıyla kuruldu ({target})!\033[0m\n")
    return 0


def cmd_skeleton(args) -> int:
    file_p = Path(args.file).resolve()
    if not file_p.is_file():
        print(f"\033[91mHata:\033[0m Dosya bulunamadı: {file_p}")
        return 1

    content = file_p.read_text(encoding="utf-8", errors="replace")
    compressor = ContextCompressor()
    res = compressor.extract_file_skeleton(content, file_path=str(file_p))

    print("=" * 60)
    print(f"  AST KOD İSKELETİ: {file_p.name} ({res.language})")
    print(f"  Orijinal Satır: {res.original_lines} → İskelet: {res.skeleton_lines} (\033[92m%{res.compression_ratio_pct} Tasarruf\033[0m)")
    print("=" * 60)
    print(res.skeleton)
    print("=" * 60)
    return 0


def cmd_compress(args) -> int:
    cmd_text = args.command or "pytest"
    print(f"Komut simülasyonu sıkıştırılıyor: {cmd_text}")
    compressor = ContextCompressor()
    report = compressor.compress_command_output(cmd_text, args.input or "Ran 100 tests in 2.5s\nOK\n")
    print(f"Sıkıştırma Oranı: %{report.ratio_pct} (Tahmini Tasarruf: ~{report.saved_tokens_est} Token)")
    print(report.content)
    return 0


def cmd_expand(args) -> int:
    ref_id = args.ref_id.strip()
    compressor = ContextCompressor()
    raw = compressor.store.retrieve(ref_id)
    if not raw:
        print(f"\033[91mHata:\033[0m '{ref_id}' referansına ait saklanmış çıktı bulunamadı.")
        return 1

    print("=" * 65)
    print(f"  🔍 GENİŞLETİLMİŞ ORİJİNAL ÇIKTI: {ref_id} ({len(raw):,} karakter)")
    print("=" * 65)
    print(raw)
    print("=" * 65)
    return 0


def cmd_status(args) -> int:
    target = Path(args.path or ".").resolve()
    rules_file = target / ".agents" / "rules" / "token_optimization.md"
    skill_file = target / ".agents" / "skills" / "token-optimizer" / "SKILL.md"
    hooks_file = target / ".agents" / "hooks.json"

    # NOTE: these labels are built outside the f-strings below on purpose. A backslash
    # inside an f-string *expression* is only valid on Python 3.12+, and this package
    # supports 3.9+ (see pyproject.toml requires-python).
    active = f"{GREEN}AKTİF{RESET}"
    missing = f"{RED}YOK{RESET}"

    print_banner()
    print(f"🔍 Proje: {target}\n")
    print(f"  - Kurallar (Rules): {active if rules_file.exists() else missing}")
    print(f"  - Yetenek (Skill):  {active if skill_file.exists() else missing}")
    print(f"  - Kancalar (Hooks): {active if hooks_file.exists() else missing}")
    print("")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="antigravity-optimizer",
        description="Antigravity Token Optimizer — Google Antigravity için Bağlam & Token Tasarruf Aracı",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Komutlar")

    # audit
    p_audit = subparsers.add_parser("audit", help="Projeyi token israfı ve bağlam şişkinliği için denetler")
    p_audit.add_argument("path", default=".", nargs="?", help="Hedef proje klasörü")

    # install
    p_install = subparsers.add_parser("install", help="Antigravity kural, skill ve kancalarını projeye kurar")
    p_install.add_argument("path", default=".", nargs="?", help="Hedef proje klasörü")
    p_install.add_argument("--profile", choices=["aggressive", "balanced", "developer", "custom"], default="balanced")

    # setup
    p_setup = subparsers.add_parser("setup", help="İnteraktif kurulum sihirbazını başlatır")
    p_setup.add_argument("path", default=".", nargs="?", help="Hedef proje klasörü")

    # skeleton
    p_skel = subparsers.add_parser("skeleton", help="Belirtilen dosyanın AST kod iskeletini çıkarır")
    p_skel.add_argument("file", help="Dosya yolu")

    # compress
    p_comp = subparsers.add_parser("compress", help="Komut çıktısını veya metni sıkıştırır")
    p_comp.add_argument("command", help="Komut adı")
    p_comp.add_argument("--input", default="", help="Sıkıştırılacak metin")

    # expand
    p_exp = subparsers.add_parser("expand", help="Sıkıştırılmış orijinal çıktıyı kayıpsız geri getirir")
    p_exp.add_argument("ref_id", help="Saklanan referans kimliği (örn: ref_a1b2c3d4)")

    # status
    p_stat = subparsers.add_parser("status", help="Mevcut optimizasyon durumunu gösterir")
    p_stat.add_argument("path", default=".", nargs="?", help="Hedef proje klasörü")

    args = parser.parse_args()

    if args.subcommand == "audit":
        return cmd_audit(args)
    elif args.subcommand == "install":
        return cmd_install(args)
    elif args.subcommand == "setup":
        return cmd_setup(args)
    elif args.subcommand == "skeleton":
        return cmd_skeleton(args)
    elif args.subcommand == "compress":
        return cmd_compress(args)
    elif args.subcommand == "expand":
        return cmd_expand(args)
    elif args.subcommand == "status":
        return cmd_status(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
