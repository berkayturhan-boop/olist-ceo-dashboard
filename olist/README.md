# 📊 Olist | CEO Yönetim İçgörü Paneli (Decision Support Dashboard)

> **Proje Hakkında**
> Bu proje, **Workintech Veri Bilimi Bootcamp**'i kapsamında verilen bitirme projesi temel alınarak geliştirilmiştir. Orijinal yapı ve veri mühendisliği süreçleri **4 kişilik bir ekip çalışmasıyla** (Agile) kurgulanmış; finansal dashboard tasarımı, müşteri memnuniyeti analizi (Logit) ve interaktif simülasyon modülleri tarafımca eklenerek final haline getirilmiştir.

![Financial Dashboard Preview](https://github.com/tmy-datamesa/CEO_talebi_takim1/assets/buraya-resim-linki-gelecek)
*(Yukarıya Finansal Özet ekran görüntüsünü ekleyin)*

## 🚀 Projenin Amacı
Bu panel, operasyonel memnuniyet metriklerini **finansal etkiye** çeviren ve buradan **portföy optimizasyonu** aksiyonuna giden, yönetim (C-Level) seviyesinde bir karar destek mekanizması sunar.

Panel 3 adımdan oluşan bir **stratejik yol haritası** izler:
1.  **Müşteri Deneyimi** (Sorun nerede?)
2.  **Finansal Etki** (Bize maliyeti ne?)
3.  **Stratejik Aksiyon** (Ne yapmalıyız?)

## 💡 Çözülen Problemler (CEO'nun Soruları)
Yönetimin cevap aradığı 3 kritik soruya odaklanılır:

* **Memnuniyet Sürücüleri:** “Müşteri puanlarını (Review Score) düşüren asıl operasyonel faktörler neler?”
* **Finansal Özet:** “Kötü hizmet ve verimsiz satıcılar kârlılığımızı ne kadar eritiyor?”
* **Portföy Optimizasyonu:** “En düşük performanslı satıcıları sistemden çıkardığımızda net kârımız maksimize olur mu?”

---

## 🧭 Uygulama Sayfaları & Analizler

### 1. Finansal Özet — Mevcut Durum (Waterfall Analizi)
Gelir ve maliyet kalemlerinin net kâra etkisini şelale grafiği ile gösterir.
* **Öne Çıkanlar:** Abonelik gelirleri, Review (İtibar) maliyetleri ve Operasyonel giderler.
* **Dosya:** `pages/home.py`

### 2. Memnuniyet Sürücüleri (Logit Modeli)
Lojistik Regresyon (Logit) algoritması kullanılarak "1 Yıldız" ve "5 Yıldız" alma olasılıkları modellenmiştir.
* **İçgörü:** Bekleme süresi (`wait_time`) arttıkça 1 yıldız riski katlanarak artmaktadır.
* **Dosya:** `pages/logit_insights.py`

### 3. Portföy Optimizasyonu (Simülasyon)
"Zarar eden satıcıları çıkarırsak ne olur?" sorusunun cevabıdır.
* **Özellik:** Slider ile interaktif senaryo analizi.
* **Çıktı:** Kârı maksimize eden optimum satıcı sayısı ve tahmini finansal kazanç.
* **Dosya:** `pages/seller_impact.py`

---

## 🛠 Kullanılan Teknolojiler

* **Python 3.x**
* **Dash & Plotly:** İnteraktif Dashboard arayüzü
* **Pandas:** Veri manipülasyonu
* **Scikit-learn:** Lojistik Regresyon modellemesi
* **Statsmodels:** İstatistiksel çıkarımlar

## 👥 Proje Ekibi (Contributors)

Bu çalışma aşağıdaki ekip üyeleri tarafından ortaklaşa geliştirilmiştir:

* **[Senin Adın]** - *Dashboard Tasarımı, Finansal Modelleme & Logit Analizi*
* **[Arkadaş 1]** - *Veri Temizliği & Hazırlık*
* **[Arkadaş 2]** - *İstatistiksel Testler*
* **[Arkadaş 3]** - *Kod Optimizasyonu*

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için:

1.  Repoyu klonlayın:
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/REPO_ADIN.git](https://github.com/KULLANICI_ADIN/REPO_ADIN.git)
    cd REPO_ADIN
    ```

2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3.  Uygulamayı başlatın:
    ```bash
    python app.py
    ```
    Tarayıcınızda `http://127.0.0.1:8050/` adresine gidin.

---
