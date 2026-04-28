# 🚀 Fast Translate v6.8

Fast Translate; bilgisayarda çalışırken, kod yazarken, makale okurken veya oyun oynarken klavye kısayolları ve sesli komutlarla anında çeviri yapmanızı sağlayan, şeffaf arayüzlü ve sesli okuma özellikli modern bir Windows aracıdır.

## ✨ Öne Çıkan Özellikler

* 🎙️ **YENİ: Sesle Çeviri (Mikrofon Modu):** Oyunun en hararetli anında klavyeyi bırakın! Sadece kısayol tuşunuza bir kez tıklayın ve konuşun. Siz susunca program sesinizi otomatik algılar, çevirir ve chat'e saniyesinde yazar.
* ⚡ **Anında Kısayol Çevirisi:** Metni yazıp kısayola bastığınızda, program metni çevirip panonuza kopyalar ve otomatik olarak ekrana yapıştırır.
* ⚙️ **Mikrofon Testi:** Ayarlar menüsünden mikrofonunuzu seçebilir ve konuşurken yeşil barın dolduğunu izleyerek sesinizi test edebilirsiniz.
* 🔊 **Sesli Okuma (TTS):** Gelen yabancı dildeki bir metni çevirdiğinizde, program Windows'un yerleşik seslendirmenleri ile çeviriyi size anında okur. Hem öğrenin hem pratik yapın!
* 👻 **Şeffaf Bildirim Ekranı:** Çevrilen metni, yaptığınız işi bölmeden ekranın alt köşesinde şeffaf bir bildirim olarak görebilirsiniz.
* 🎨 **Modern UI & Gizlilik:** CustomTkinter ile tasarlanmış Karanlık/Aydınlık mod destekli arayüz. Tek tıkla sistem tepsisine (sağ alta) gizlenebilir ve arka planda sessizce çalışır.
* 🔄 **Otomatik Güncelleme Sistemi:** Program yeni bir özellik eklendiğinde bunu otomatik algılar ve sizi güncel sürüme yönlendirir.

## 🛠️ Kurulum ve Kullanım (Son Kullanıcılar İçin)

1. [Releases](https://github.com/Metehan6634/FastTranslate/releases) sekmesine gidin ve en güncel `Fast Translate.exe` dosyasını indirin.
2. **Çok Önemli:** Programın klavye kısayollarınızı her uygulamada sorunsuz algılayabilmesi için `.exe` dosyasına sağ tıklayıp **"Yönetici Olarak Çalıştır"** demeniz gerekmektedir.
3. Arayüzden kaynak/hedef dili seçin. Atama butonlarına tıklayarak kendi kısayol tuşlarınızı klavyeden belirleyin ve "Kaydet" butonuna basın. Uygulamayı sağ alta gizleyip işinize dönebilirsiniz!

## ☕ Destek Ol (Donate)

Eğer bu program işinize yaradıysa, bana destek olmak ve yeni projeler için motive etmek isterseniz destek olabilirsiniz!
* 🎮 **[ByNoGame Destek Linkim](https://donate.bynogame.com/metehann)**

## 🚨 ÖNEMLİ: ANTİ-HİLE SİSTEMLERİ VE BAN RİSKİ (VALORANT, CS2 vb.)

Fast Translate, oyun içinde anında çeviri yapabilmek için arka planda çok hızlı bir şekilde klavye tuşlarını (Ctrl+A, Ctrl+C, Ctrl+V) simüle eden bir altyapıyla çalışır. Program **kesinlikle bir hile (cheat) değildir**, oyun dosyalarına veya belleğine (memory) müdahale etmez.

Ancak **Riot Vanguard** gibi son derece agresif çalışan anti-hile (Anti-Cheat) sistemleri, arka planda gerçekleşen bu sanal tuş vuruşlarını (makro eylemlerini) yanlışlıkla 3. parti zararlı yazılım olarak algılayabilir.

Riot Games Destek ekibi ile bizzat yapılan resmi görüşmede: *"Sadece çeviri amaçlı olsa bile Vanguard'ın dış müdahaleleri algılayıp hesabı kalıcı olarak uzaklaştırma (perma-ban) riski olduğu"* açıkça belirtilmiştir.

**⚠️ BU NEDENLE:** Programı rekabetçi oyunlarda (Özellikle Valorant'ta) kullanmak **TAMAMEN KULLANICININ KENDİ SORUMLULUĞUNUZDADIR.** Geliştirici olarak, doğabilecek hesap kısıtlamalarından veya ban durumlarından hiçbir sorumluluk kabul etmiyorum. Ana hesabınızı riske atmamak adına bu durumu göz önünde bulundurun veya programı masaüstü/ofis işlemlerinizde kullanın.

## 💻 Geliştirici Kaynak Kodları ve Kurulum

Projeyi kendi bilgisayarınızda derlemek veya geliştirmek isterseniz:

1. Projeyi klonlayın:
```bash
git clone [https://github.com/Metehan6634/FastTranslate.git](https://github.com/Metehan6634/FastTranslate.git)
```
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

(Not: Geliştirici olarak kurarken ses algılama (PyAudio) modülü için bilgisayarınızda C++ Build Tools kurulu olması gerekir.)

## ⚠️ Bilinen Durumlar ve Çözümler
Kısayollar Çalışmıyor: Uygulamayı mutlaka Yönetici (Administrator) haklarıyla çalıştırın. Windows güvenlik duvarı klavye dinlemeyi kısıtlayabilir.

"æ" Karakteri Çıkma Sorunu: Güvenli tuş tahliye sistemi ile çözülmüştür. Yine de sorun yaşarsanız, kısayola "basılı tutmak" yerine sadece "bas-bırak" yapın.

Mikrofon İsimleri Bozuk Çıkıyor (Mojibake): v6.8 ile karakter kodlama (Encoding) hatası çözülmüştür.

## 📜 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Tamamen açık kaynaktır.

Created by Metehan
