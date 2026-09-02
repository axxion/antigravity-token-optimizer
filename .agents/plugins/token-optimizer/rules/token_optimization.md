# Antigravity Token & Context Optimization Rules

> [!NOTE]
> Bu kural dosyası **Antigravity Token Optimizer** (Profil: `BALANCED`) tarafından otomatik oluşturulmuştur.

## 1. Temel Davranış İlkeleri

### A. Yalın İletişim & Sıfır Dolgu (Lean Prompt)
- **Gereksiz nezaketi ve dolgu cümlelerini atlayın:** 'Elbette!', 'Anladım', 'Şimdi sizin için yapıyorum' gibi açılış cümleleri kurmayın; doğrudan çözüme ve koda geçin.
- **Talimatları tekrar etmeyin:** Kullanıcının verdiği emri kendi cümlelerinizle özetlemeyin.
- **Kısa ve öz yanıt verin:** Değişiklikleri 1-2 cümlelik odaklanmış maddelerle açıklayın.

### B. Cerrahi Dosya Düzenleme & Dilimleme (Surgical Edits)
- **Tüm dosyayı baştan yazmayın (`write_file` yasağı):** Mevcut bir dosyada değişiklik yaparken yalnızca değişen bloğu hedefleyen cerrahi araçları (`replace_file_content` veya `replace_content`) kullanın.
- **Gereksiz tam dosya okuması yapmayın:** Büyük dosyalarda daima satır aralığı (`start_line`, `end_line`, max 150 satır) belirtin.
- **Sadece ilgili bölümleri okuyun:** Bir fonksiyonu incelemek için 500 satırlık dosyanın tamamını bağlama çekmeyin.

### C. AST Kod İskeletleri (Code Skeletons)
- **120 satırı aşan büyük dosyalarda:** İlk incelemede implementasyon detaylarını değil; sınıf, metot ve tip imzalarını (skeleton) inceleyin.
- Yalnızca düzenlenecek metodun gövdesini bağlama dahil edin.

### D. Komut & Test Çıktısı Optimizasyonu
- Uzun test çıktılarında (`pytest`, `npm test`) geçen testlerin detaylarını atlayın; yalnızca başarısız test yığınlarını (failures) ve özet sayıları raporlayın.
- Komut çıktılarında maksimum 4000 karakter sınırını aşmayın.

### E. Arama ve Grep Disiplini
- Grep ve dosya aramalarında tek seferde maksimum 30 eşleşme inceleyin.
- Çok geniş desenler (örn: `.*`) yerine spesifik sembol adlarıyla arama yapın.

### F. Harici Bellek & Kontrol Noktaları
- Durum, görev listesi ve mimari kararları modelin geçici konuşma geçmişinde tutmak yerine `BOARD.md`, `LEDGER.md` veya `MEMORY.md` dosyalarına kaydedin.
- Sıkıştırma (compaction) durumlarında görev geçmişini bu dosyalardan geri yükleyin.
