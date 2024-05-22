# sozlukApp
## Proje Hakkında
Bu proje, kelime öğrenme ve tekrar etme amacıyla ***Python*** ile tasarlanmış bir masaüstü uygulamasıdır. Uygulama, kullanıcıların kelimeleri Türkçe ve İngilizce olarak girmelerini, sesli telaffuzlarını dinlemelerini, örnek cümleler görmelerini ve kelimeleri konulara göre sınıflandırmalarını sağlar. Ayrıca, kullanıcılar kelimeleri quiz formatında test edebilir ve öğrenme ilerlemelerini takip edebilirler.

## Özellikler
- Kelime ekleme ve düzenleme
- Kelimelerin sesli telaffuzlarını dinleme
- Kelimelerin örnek cümlelerini görme
- Kelimeleri konulara göre sınıflandırma
- Kelimeleri quiz formatında test etme
- Öğrenme ilerlemesini takip etme
- Veri tabanı bağlantısı


## Kullanılan Teknolojiler
- Python: Programlama dili
- PyQt6: Grafiksel kullanıcı arayüzü (GUI) kütüphanesi
- MySQL: Veritabanı yönetim sistemi
- Requests: HTTP istekleri göndermek için kullanılan kütüphane
- Pillow: Görüntü işleme kütüphanesi
- JSON: Veri serileştirme ve deserializasyon formatı
- ConfigParser: Yapılandırma dosyalarını okumak ve yazmak için kullanılan kütüphane

## Kullanılan Kütüphaneler
- pandas: Veri analizi ve manipülasyonu için kullanılan kütüphane
- numpy: Sayısal hesaplamalar için kullanılan kütüphane
- matplotlib: Grafik çizimi için kullanılan kütüphane
- pygame: Ses oynatma için kullanılan kütüphane
- configparser: Yapılandırma dosyalarını okumak ve yazmak için kullanılan kütüphane
- Ve digerleri(*mysql*, *json*, *datetime*, *pygame*, *requests*, *PIL*, *io*)

## Kurulum
- Projeyi GitHub'dan klonlayın.
- Gerekli kütüphaneleri yükleyin: 
```python
# Ornegin
pip install pandas
```
- Veri tabanini **data/veritabani** kilasordeki *sql* dosyalari ile olusturun
- Veri tabanı bağlantı bilgilerini **data/sifre.ini** dosyasında yapılandırın.
- Uygulamayı çalıştırın: python app.py
## Kullanım
Uygulama açıldığında, kullanıcı giriş ekranını görecektir. Giriş yaptıktan sonra, kullanıcı kelime ekleme, düzenleme, sesli telaffuz dinleme, örnek cümle görme, konulara göre sınıflandırma, quiz formatında test etme ve öğrenme ilerlemesini takip etme gibi özelliklere erişebilir.

> **Not:** Uygulama icersinde kullanilacak resim, ses ve ornek cumleler vb. api yardimi ile otomatik olarak cekilecek ve klasorler veya veritabani icine koyulacaktir.
> 
## Ekran Görüntüleri
Ana ekran: Ana ekran
Kelime ekleme ekranı: Kelime ekleme ekranı
Quiz ekranı: Quiz ekranı
Katkıda Bulunma
Bu projeye katkıda bulunmak istiyorsanız, lütfen bir pull request gönderin.
### Api servisleri ile kullanilan siteler:
- Kelimeler icin https://evdeingilizcem.com/ingilizce-kelimeler
- Resimler icin https://unsplash.com
- kelime bilgileri ve sesler icin https://dictionaryapi.dev/
#### Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

#### İletişim
Bu proje hakkında herhangi bir sorunuz varsa, lütfen muhakaplan@hotmail.com adresinden bana ulaşın.
