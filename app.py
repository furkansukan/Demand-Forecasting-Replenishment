import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from prophet import Prophet

import matplotlib.pyplot as plt

# Streamlit sayfa başlığı
st.title("Demand Forecasting & Replenishment")

# Sol bar (Sidebar) oluşturma
sidebar = st.sidebar
st.sidebar.title("RNV.ai")
    image = Image.open('logo.png')
    with st.sidebar:
        st.image(image, caption='rnv.ai', use_column_width=True)
        
        st.write("Akıllı stok yönetimi ile satışlarınızı artırın")
# Sayfa seçenekleri
pages = {
    "Ana Sayfa": "home",
    "Talep Tahmini": "demand_forecasting",
    "Optimal Sipariş Miktarı (EOQ)": "eoq",
    "Yeniden Sipariş Zamanlaması (Replenishment Planı)": "replenishment",
    "İletişim": "contact"
}

# Sayfa seçim menüsü
page_selection = sidebar.radio("Sayfa Seçin", options=list(pages.keys()))

# Rastgelelik için seed belirleme
np.random.seed(42)

# Başlangıç ve bitiş tarihlerini belirleme
start_date = "2021-01-01"
end_date = "2024-12-03"

# Tarih sütunu
dates = pd.date_range(start=start_date, end=end_date)

# Gün sayısını güncelle
n_days = len(dates)

# Günlük talep (y değişkeni) rastgele dağılım
daily_sales = np.random.randint(5, 15, size=n_days)  # 5 ile 15 arasında rastgele satışlar

# Başlangıç stok seviyesi
initial_stock = np.random.randint(50, 100)  # Başlangıç stok seviyesi (random)

# Stok seviyesi (stock_level) ve yenileme
stock_levels = [initial_stock]
for sales in daily_sales:
    current_stock = stock_levels[-1] - sales
    if current_stock <= 10:  # Yeniden sipariş eşiği
        current_stock += np.random.randint(50, 150)  # Rastgele yenileme miktarı
    stock_levels.append(current_stock)

# Son stok seviyesini eşitlemek
stock_levels = stock_levels[:-1]

# Veri çerçevesi oluşturma
df = pd.DataFrame({
    "ds": dates,
    "y": daily_sales,
    "stock_level": stock_levels
})

# Sayfa içerikleri
if page_selection == "Ana Sayfa":
    st.header("Ana Sayfa")

    # Kullanıcıya veri yükleme seçeneği
    uploaded_file = st.file_uploader("Veri Yükleyin", type=["csv", "xlsx"])
    if uploaded_file is not None:
        # Veriyi yükle ve göster
        uploaded_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(
            uploaded_file)
        st.write(uploaded_df.head())
        st.write("Yüklenen Veri")
    else:
        # Örnek veri gösterimi
        st.write(df.head())
        st.write("Oluşturulan Örnek Veri")

    # Günlük veri görselleştirme
    st.subheader("Günlük Talep ve Stok Seviyesi")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["ds"], df["y"], label="Günlük Talep", color="blue", alpha=0.7)
    ax.plot(df["ds"], df["stock_level"], label="Günlük Stok Seviyesi", color="green", alpha=0.7)
    ax.set_title("Günlük Talep ve Stok Seviyesi")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Değer")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # Haftalık veri görselleştirme
    st.subheader("Haftalık Talep ve Stok Seviyesi")
    weekly_df = df.resample('W', on='ds').sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(weekly_df.index, weekly_df["y"], label="Haftalık Talep", color="blue", alpha=0.7)
    ax.plot(weekly_df.index, weekly_df["stock_level"], label="Haftalık Stok Seviyesi", color="green", alpha=0.7)
    ax.set_title("Haftalık Talep ve Stok Seviyesi")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Değer")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # Aylık veri görselleştirme
    st.subheader("Aylık Talep ve Stok Seviyesi")
    monthly_df = df.resample('M', on='ds').sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_df.index, monthly_df["y"], label="Aylık Talep", color="blue", alpha=0.7)
    ax.plot(monthly_df.index, monthly_df["stock_level"], label="Aylık Stok Seviyesi", color="green", alpha=0.7)
    ax.set_title("Aylık Talep ve Stok Seviyesi")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Değer")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

elif page_selection == "Talep Tahmini":
    st.header("Talep Tahmini (Demand Forecasting)")
    # Talep Tahmini sayfası
    if page_selection == "Talep Tahmini":


        # Prophet modeli için veri hazırlığı
        product_df = df[["ds", "y"]]

        # Prophet modelini oluştur ve eğit
        model = Prophet()
        model.fit(product_df)

        # Tahmin süresi (30 gün)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        # Tahmin sonuçlarını dataframe olarak göster
        forecast_30_days = forecast.tail(30)[["ds", "yhat"]]
        st.session_state.model = model
        st.session_state.forecast = forecast
        st.session_state.forecast_30_days = forecast_30_days
        # Tahmin edilen tüm veriyi göster
        st.subheader("Tahmin Edilen Tüm Veri")
        st.write(forecast[["ds", "yhat"]].tail(30))  # Son 30 günün tahminini göster

        # Grafiksel görselleştirme
        st.subheader("Talep Tahmini (30 Gün)")
        fig, ax = plt.subplots(figsize=(12, 6))
        model.plot(forecast, ax=ax)
        ax.set_title("Talep Tahmini (30 Gün)")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Talep")
        ax.grid()
        st.pyplot(fig)

        # Son 45 gün için görselleştirme
        st.subheader("Son 45 Günlük Talep Tahmini")
        forecast_45_days = forecast.tail(45)

        # Grafiksel görselleştirme - Son 45 gün
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(forecast_45_days["ds"], forecast_45_days["yhat"], label="Tahmin Edilen Talep", color="blue", alpha=0.7)
        ax.set_title("Son 45 Günlük Talep Tahmini")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Talep")
        ax.legend()
        ax.grid()
        st.pyplot(fig)


elif page_selection == "Optimal Sipariş Miktarı (EOQ)":
    st.header("Optimal Sipariş Miktarı (EOQ Hesabı)")
    st.write("EOQ hesaplamalarını yapabilirsiniz.")

    forecast_30_days = st.session_state.get("forecast_30_days", None)
    model = st.session_state.get("model", None)
    forecast = st.session_state.get("forecast", None)
    # EOQ hesaplama fonksiyonu
    def eoq(demand, ordering_cost, holding_cost):
        """
        Economic Order Quantity (EOQ) hesaplama.
        """
        return np.sqrt((2 * demand * ordering_cost) / holding_cost)


    # Bilgilendirme notu
    st.markdown("""
        **Optimal Sipariş Miktarı (EOQ - Economic Order Quantity)**:
        Optimal sipariş miktarını (EOQ - Economic Order Quantity) belirlemek için şu adımları izleyebiliriz:

        EOQ Formülü: √(2DS/H) Burada:
        
        - (D): Toplam talep (örneğin, 30 günlük tahmin edilen toplam talep).
        - (S): Sipariş başına sabit maliyet (örneğin, 50 birim).
        - (H): Birim başına yıllık tutma maliyeti (örneğin, 2 birim).

        **Tahmin Edilen Günlük Talep**: Prophet modeli ile tahmin edilen 30 günlük toplam talep hesaplanır.

        **Hesaplama**: EOQ formülü uygulanarak optimal sipariş miktarı hesaplanır.
    """)

    # Kullanıcıdan sipariş ve tutma maliyetlerini alma
    ordering_cost = st.number_input("Sipariş Başına Sabit Maliyet (S)", value=50, min_value=0)
    holding_cost = st.number_input("Birim Başına Yıllık Tutma Maliyeti (H)", value=2, min_value=0)

    # Tahmin edilen 30 günlük toplam talep
    total_demand_30_days = forecast_30_days["yhat"].sum()

    # EOQ Hesaplama
    optimal_order_quantity = eoq(total_demand_30_days, ordering_cost, holding_cost)
    st.session_state.optimal_order_quantity = optimal_order_quantity
    # Çıktıları gösterme
    st.subheader("Hesaplamalar")
    st.write(f"Tahmin Edilen 30 Günlük Toplam Talep: {total_demand_30_days:.2f}")
    st.write(f"Optimal Sipariş Miktarı (EOQ): {optimal_order_quantity:.2f} birim")

    # Grafiksel görselleştirme
    st.subheader("Talep Tahmini (30 Gün)")
    fig, ax = plt.subplots(figsize=(12, 6))
    model.plot(forecast, ax=ax)
    ax.set_title("Talep Tahmini (30 Gün)")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Talep")
    ax.grid()
    st.pyplot(fig)

    # Kullanıcıya bilgi verme
    st.markdown("""
        **EOQ Hesaplama**:
        - Optimal Sipariş Miktarı (EOQ), talep, sipariş başına maliyet ve tutma maliyetleri göz önüne alınarak hesaplanır.
        - Bu hesaplama, stok yenileme stratejisini optimize etmede yardımcı olabilir ve ürün siparişlerini daha verimli hale getirebilir.
    """)


elif page_selection == "Yeniden Sipariş Zamanlaması (Replenishment Planı)":
    st.header("Yeniden Sipariş Zamanlaması (Replenishment Planı)")
    st.write("Replenishment planınızı oluşturabilirsiniz.")

    # Yeniden Sipariş Zamanlaması sayfası için bilgilendirme notu
    st.markdown("""
    ### Yeniden Sipariş Zamanlaması (Replenishment Planı)

    Yeniden sipariş planı oluşturmak için şu adımları izleriz:

    1. **Mevcut Stok Bilgisi**  
    Veri çerçevesindeki `stock_level` bilgisini kullanırız. Yeniden sipariş seviyesi (reorder level), tahmini günlük talep ve tedarik süresine (lead time) göre hesaplanır:  
       

    2. **Replenishment Planı**  
    EOQ'ya göre optimal sipariş miktarını kullanırız.  
    Her gün için stok seviyesi tahmini günlük talep ile azaltılır.  
    Stok seviyesi yeniden sipariş seviyesinin altına düştüğünde sipariş verilmesi gerekir.

    ---

    ### Çıktılar:
    1. **Sipariş Planı Tablosu**:  
       - Tarih (`Date`): Siparişin verilmesi gereken tarih.  
       - Sipariş Miktarı (`Order Quantity`): Sipariş miktarı (EOQ ile hesaplanan miktar).

    2. **Grafik**:
       - Stok seviyesi çizgisi.
       - Yeniden sipariş seviyesi (kırmızı kesikli çizgi).
       - Sipariş verilen günler (yeşil kesikli çizgiler).

    ---

    Bu plan, stok seviyelerinin sürekli izlenmesini ve tahminlere dayalı otomatik sipariş zamanlamasını sağlar. EOQ ve talep tahmini kullanılarak stok optimizasyonu sağlanır.
    """)

    # Lead time kullanıcıdan alınacak
    lead_time = st.number_input("Tedarik Süresi (Lead Time, gün cinsinden)", min_value=1, value=3)

    # Forecast verisi ve optimal sipariş miktarı (EOQ) daha önce hesaplanmış olmalı
    forecast_30_days = st.session_state.get("forecast_30_days", None)
    optimal_order_quantity = st.session_state.get("optimal_order_quantity", None)

    # Mevcut stok seviyesini almak (örnek olarak)
    current_stock = df["stock_level"].iloc[-1]  # Mevcut stok

    if forecast_30_days is not None and optimal_order_quantity is not None:
        # Yeniden sipariş seviyesini hesapla
        reorder_level = forecast_30_days["yhat"].mean() * lead_time

        # Sipariş planı tablosunu başlatma
        replenishment_plan = []
        stock_levels_simulated = [current_stock]  # Mevcut stok başlangıcı
        order_dates = []  # Sipariş verilen günlerin tarihleri

        # 30 günlük tahmin üzerinden stok seviyesi simülasyonu
        for i, row in forecast_30_days.iterrows():
            daily_demand = row["yhat"]  # Günlük tahmin edilen talep
            new_stock_level = stock_levels_simulated[-1] - daily_demand  # Stok seviyesini düşür

            # Eğer stok seviyesi yeniden sipariş seviyesinin altına düşerse
            if new_stock_level <= reorder_level:
                order_dates.append(row["ds"])  # Sipariş tarihini kaydet
                new_stock_level += optimal_order_quantity  # EOQ ile stok artırımı

            stock_levels_simulated.append(new_stock_level)  # Güncellenmiş stok seviyesini ekle

        # Grafiksel görselleştirme
        fig, ax = plt.subplots(figsize=(12, 6))  # Yeni figür oluşturuluyor
        ax.plot(forecast_30_days["ds"], stock_levels_simulated[1:], label="Stok Seviyesi",
                color="blue")  # İlk elemanı atla
        ax.axhline(reorder_level, color="red", linestyle="--", label="Yeniden Sipariş Seviyesi")
        for date in order_dates:
            ax.axvline(date, color="green", linestyle="--", label="Sipariş Verilen Gün")
        ax.set_title("Stok Seviyesi ve Sipariş Zamanlaması")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Stok Seviyesi")
        ax.legend()
        ax.grid()

        # st.pyplot() fonksiyonuna figür parametresi sağlanarak hata giderildi
        st.pyplot(fig)

        # Sipariş planı tablosunu oluşturma
        replenishment_plan_df = pd.DataFrame({
            "Date": order_dates,
            "Order Quantity": [optimal_order_quantity] * len(order_dates)
        })

        st.write("### Sipariş Planı Tablosu")
        st.write(replenishment_plan_df)

    else:
        st.error(
            "Talep tahmini verisi ve optimal sipariş miktarı bulunamadı. Lütfen önce Talep Tahmini sayfasını çalıştırın.")


elif page_selection == "İletişim":
    st.header("İletişim")
    st.write("""
                **Daha Fazla Soru ve İletişim İçin**  
                Bu projeyle ilgili herhangi bir sorunuz veya geri bildiriminiz olursa benimle iletişime geçmekten çekinmeyin! Aşağıdaki platformlar üzerinden ulaşabilirsiniz:
                """)

    st.write("📧 **E-posta**: furkansukan10@gmail.com")
    st.write("🪪 **LinkedIn**: https://www.linkedin.com/in/furkansukan/")
    st.write("🔗 **Kaggle**: https://www.kaggle.com/furkansukan")
    st.write("🐙 **GitHub**: https://github.com/furkansukan")  # Buraya bağlantı ekleyebilirsiniz
    # Buraya bağlantı ekleyebilirsiniz

    st.write("""
                Görüş ve önerilerinizi duymaktan mutluluk duyarım!
                """)

