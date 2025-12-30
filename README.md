# Olist | Yönetim İçgörü Paneli (Dash)

Operasyonel memnuniyet metriklerini **finansal etkiye** çeviren ve buradan **portföy optimizasyonu** aksiyonuna giden, yönetim seviyesinde bir karar destek demo paneli.

> Panel 3 adımdan oluşan bir “yol haritası” sunar:  
> **(1) Müşteri Deneyimi → (2) Finansal Etki → (3) Stratejik Aksiyon**

---

## 🚀 Neyi çözüyor?

Yönetimin hızlı cevap aradığı 3 soruya odaklanır:

1. **Memnuniyet Sürücüleri:** “Müşteri puanlarını en çok hangi operasyonel faktörler etkiliyor?”
2. **Finansal Özet:** “Bu operasyonel problemler kârlılığı bugün ne kadar eritiyor?”
3. **Portföy Optimizasyonu:** “En düşük performanslı satıcıları yönettiğimizde net kâr nerede maksimum olur?”

---

## 🧭 Uygulama Sayfaları

### 1) Memnuniyet Sürücüleri (Operasyonel Memnuniyet Analizi)
- Lojistik regresyon (Logit) çıktılarıyla:
  - **1★ riskini artıran** faktörler
  - **5★ kaybına neden olan** faktörler
- Yönetim diliyle kısa “Analizden Çıkarımlar” ve “Stratejik Öneriler” kartları

Dosya: `pages/logit_insights.py`

---

### 2) Finansal Özet — Mevcut Durum
- Gelir–maliyet–net kâr kırılımı:
  - Abonelik + komisyon gelirleri
  - Review (memnuniyetsizlik) maliyeti
  - IT/Operasyon maliyeti
  - Net kâr (hedef KPI vurgulu)
- Waterfall görseli: gelir → maliyet → net sonuç

Dosya: `pages/home.py`

---

### 3) Portföy Optimizasyonu (Satıcı Çıkarma Etkisi)
- Slider ile “en düşük performanslı kaç satıcı çıkarılsın?” senaryosu
- Sol grafikte portföy boyutu vs kârlılık eğrileri
- Sağda seçili senaryonun “tek bakış” finansal özeti
- “İdeal nokta (peak profit)” işaretlemesi

Dosya: `pages/seller_impact.py`

---

### 4) Metodoloji
- Panelin kapsamı, varsayımlar ve okuma rehberi
- Eğitim amacı / şeffaflık notu

Dosya: `pages/about.py`

---

## 🧠 Metodoloji Özeti

### Lojistik Regresyon (Logit)
- Amaç: “1★ alma olasılığı” ve “5★ olasılığı” gibi memnuniyet olaylarını açıklamak
- Operasyonel değişkenler üzerinden göreceli etki gücü üretmek (yönetim seviyesi yorum)

> Model çıktıları demo içindir; amaç karar destek yaklaşımını göstermektir.

### IT / Operasyon Maliyeti
- Basit ve ölçeklenebilir bir maliyet yaklaşımı kullanılır (eğitim senaryosu).
- Satıcı sayısı ve ürün hacmi ile maliyetin ölçek davranışı modellenir.

---

## 🗂 Proje Yapısı

```bash
.
├── app.py
├── data/                          # Olist CSV datasetleri
├── olist/                         # Veri erişim ve hesaplama sınıfları
├── pages/                         # Dash sayfaları
│   ├── about.py                   # Metodoloji
│   ├── home.py                    # Finansal Özet
│   ├── logit_insights.py          # Memnuniyet Sürücüleri
│   └── seller_impact.py           # Portföy Optimizasyonu
└── README.md
