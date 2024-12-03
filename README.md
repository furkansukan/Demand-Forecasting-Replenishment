# 📈 Talep Tahmini & Yeniden Sipariş Optimizasyonu 🚚

**Talep Tahmini & Yeniden Sipariş Optimizasyonu** projesine hoş geldiniz! 🎯  
Bu uygulama, işletmelerin stok yönetimini optimize etmesine yardımcı olmak için talep tahmini ve ekonomik sipariş miktarı (EOQ) hesaplamalarını akıllı sipariş planlamasıyla birleştirir. 💡

---

## 🌟 Özellikler
1. **Talep Tahmini** 📊  
   - Gelecek 30 günlük talebi tahmin etmek için **Prophet modeli** kullanır.  
   - Geçmiş veri trendlerine dayalı doğru tahminler sunar.  

2. **Ekonomik Sipariş Miktarı (EOQ) Hesaplama** 📦  
   - **Maliyetleri en aza indiren optimal sipariş miktarını** belirler.  
   - Sipariş maliyeti, stok taşıma maliyeti ve tahmin edilen talebe göre hesaplanır.

3. **Yeniden Sipariş Planlaması** 🗓️  
   - Günlük stok seviyelerini simüle ederek stok tükenmelerini ve fazla stok sorunlarını önler.  
   - Stok seviyesi yeniden sipariş eşiğinin altına düştüğünde otomatik sipariş planlar.  

4. **Etkileşimli Parametreler** ⚙️  
   - **Teslim süresi (lead time)**, **sipariş maliyeti** ve **stok taşıma maliyetini** özelleştirin.  
   - Sipariş planını grafiklerle görselleştirin.

---

## 📖 Nasıl Çalışır?

### 1️⃣ Talep Tahmini  
**Prophet modeli**, geçmiş satış verileri üzerinden gelecek 30 günü tahmin eder (`yhat`).  
Örnek:  
```python
total_demand_30_days = forecast_30_days["yhat"].sum()
```

### 2️⃣ Ekonomik Sipariş Miktarı (EOQ)  
EOQ şu formülle hesaplanır:  
\[
EOQ = \sqrt{\frac{{2 \cdot D \cdot S}}{{H}}}
\]  
- \(D\): Tahmin edilen talep (ör. 30 günlük toplam talep).  
- \(S\): Sipariş maliyeti (ör. 50 TL/sipariş).  
- \(H\): Taşıma maliyeti (ör. 2 TL/birim/yıl).  

Örnek hesaplama:  
```python
optimal_order_quantity = round(math.sqrt((2 * total_demand_30_days * ordering_cost) / holding_cost))
```

### 3️⃣ Yeniden Sipariş Planlaması  
Stok seviyesi her gün kontrol edilir ve yeniden sipariş eşiğinin altına düşerse sipariş planlanır. 📈  

Hesaplama örneği:  
```python
reorder_level = forecast_30_days["yhat"].mean() * lead_time
```

`matplotlib` ile görselleştirme:  
- Stok seviyeleri 📉  
- Yeniden sipariş seviyesi 🚨  
- Sipariş tarihleri 📅  

---

## 🎨 Görsel Çıktılar

1. **Tahmin Tablosu**  
   - Gelecek 30 gün için talep tahminlerini (`yhat`) gösterir.  

2. **Sipariş Planı Tablosu**  
   - **Sipariş tarihleri** ve **sipariş miktarlarını** içerir.

3. **Stok Seviyesi Grafiği**  
   - 📉 Zamanla değişen stok seviyeleri.  
   - 🚨 Yeniden sipariş seviyesi (kırmızı kesikli çizgi).  
   - 📅 Sipariş verilen günler (yeşil kesikli çizgi).  

---

## ⚡ Başlangıç Rehberi

### Gereksinimler
- Python 3.8+  
- Gerekli kütüphaneler: `streamlit`, `pandas`, `matplotlib`, `prophet`, `numpy`.

### Kurulum
1. Projeyi klonlayın:  
   ```bash
   git clone https://github.com/kullaniciadi/talep-tahmini-siparis.git
   cd talep-tahmini-siparis
   ```

2. Bağımlılıkları yükleyin:  
   ```bash
   pip install -r requirements.txt
   ```

### Uygulamayı Çalıştırma
**Streamlit** uygulamasını başlatın:  
```bash
streamlit run app.py
```

---


---

## 🛠️ Proje Yapısı
```
.
├── app.py                  # Ana uygulama dosyası
├── requirements.txt        # Gerekli Python kütüphaneleri
├── README.md               # Proje dökümantasyonu
└── data/                   # Geçmiş ve tahmin verileri
```

---

## 📞 İletişim
Herhangi bir sorunuz veya öneriniz varsa, bana şu kanallardan ulaşabilirsiniz:

📧 E-mail: furkansukan10@gmail.com

🪪 LinkedIn: [furkansukan](https://www.linkedin.com/in/furkansukan/)

🔗 Kaggle: [Profilim](https://www.kaggle.com/furkansukan)

🎗️ Demand Forecasting & Replenishment Sitesi: [Websitesi](https://demand-forecasting-replenishment-furkansukan.streamlit.app/)

f❤️r RNV.ai
---



