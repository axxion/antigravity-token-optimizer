---
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

## ⚠️ Bilinen Sınırlama: `.agents/hooks.json`

`install` komutu ayrıca her model çağrısından önce kısa bir hatırlatma enjekte eden bir `.agents/hooks.json`
(`PreInvocation` hook'u) kurar. Bu hook, Antigravity **CLI**'da (`agy`) çalışır; topluluk raporlarına göre
Antigravity **IDE/masaüstü uygulaması**nda (2.x) şu an sessizce tetiklenmiyor — hata vermiyor, sadece
çalışmıyor. Bu, temel işlevi **bozmaz**: yukarıdaki davranış kuralları zaten `.agents/rules/token_optimization.md`
içinde durağan bir kural olarak yer alıyor ve Antigravity IDE bu dosyayı ayrı bir mekanizmayla otomatik
okuyor. Kaybedilen şey yalnızca her tur tekrarlanan "⚡ Token Optimizer Aktif" hatırlatma mesajıdır.
