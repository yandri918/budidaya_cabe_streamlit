"""
📈 Prediksi Harga Cabai
Analisis tren & rekomendasi waktu jual
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Prediksi Harga Cabai",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 Prediksi Harga Cabai")
st.markdown("**Analisis tren harga & rekomendasi waktu jual terbaik**")

st.markdown("---")

# Generate simulated historical data
def generate_price_data():
    """Generate simulated price data for demonstration"""
    months = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
    
    # Base price with seasonal pattern
    base_price = 35000
    seasonal_factor = [1.4, 1.5, 1.6, 1.2, 1.0, 0.8, 0.7, 0.75, 0.9, 1.1, 1.2, 1.3]
    
    prices = []
    for i, month in enumerate(months):
        month_idx = month.month - 1
        seasonal = seasonal_factor[month_idx]
        noise = np.random.normal(0, 2000)
        price = base_price * seasonal + noise
        prices.append(max(price, 15000))  # Min price 15k
    
    return pd.DataFrame({
        'Tanggal': months,
        'Harga': prices
    })

df_prices = generate_price_data()

# Tabs
tabs = st.tabs(["📊 Tren Harga", "🔮 Prediksi", "💡 Rekomendasi", "📅 Kalender Harga"])

with tabs[0]:
    st.header("📊 Tren Harga Historis")
    
    # Price trend chart
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=df_prices['Tanggal'],
        y=df_prices['Harga'],
        mode='lines+markers',
        name='Harga Cabai Merah',
        line=dict(color='#FF6B6B', width=2),
        marker=dict(size=6)
    ))
    
    # Add moving average
    df_prices['MA_3'] = df_prices['Harga'].rolling(window=3).mean()
    
    fig_trend.add_trace(go.Scatter(
        x=df_prices['Tanggal'],
        y=df_prices['MA_3'],
        mode='lines',
        name='Moving Average (3 bulan)',
        line=dict(color='#4ECDC4', width=2, dash='dash')
    ))
    
    fig_trend.update_layout(
        title='Tren Harga Cabai Merah (2023-2024)',
        xaxis_title='Bulan',
        yaxis_title='Harga (Rp/kg)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Statistics
    st.markdown("---")
    st.subheader("📊 Statistik Harga")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Harga Rata-rata", f"Rp {df_prices['Harga'].mean():,.0f}/kg")
    
    with col2:
        st.metric("Harga Tertinggi", f"Rp {df_prices['Harga'].max():,.0f}/kg")
    
    with col3:
        st.metric("Harga Terendah", f"Rp {df_prices['Harga'].min():,.0f}/kg")
    
    with col4:
        volatility = df_prices['Harga'].std()
        st.metric("Volatilitas", f"Rp {volatility:,.0f}")
    
    # Monthly analysis
    st.markdown("---")
    st.subheader("📅 Analisis Bulanan")
    
    df_prices['Bulan'] = df_prices['Tanggal'].dt.month_name()
    df_monthly = df_prices.groupby('Bulan')['Harga'].mean().reset_index()
    
    # Sort by month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_monthly['Bulan'] = pd.Categorical(df_monthly['Bulan'], categories=month_order, ordered=True)
    df_monthly = df_monthly.sort_values('Bulan')
    
    fig_monthly = px.bar(
        df_monthly,
        x='Bulan',
        y='Harga',
        title='Rata-rata Harga per Bulan',
        labels={'Harga': 'Harga (Rp/kg)', 'Bulan': 'Bulan'},
        color='Harga',
        color_continuous_scale='RdYlGn_r'
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)

with tabs[1]:
    st.header("🔮 Prediksi Harga")
    
    st.info("💡 Prediksi menggunakan metode Moving Average sederhana untuk edukasi")
    
    # Simple forecast using moving average
    last_3_months = df_prices['Harga'].tail(3).mean()
    
    # Generate forecast for next 6 months
    forecast_months = pd.date_range(
        start=df_prices['Tanggal'].max() + timedelta(days=30),
        periods=6,
        freq='M'
    )
    
    # Apply seasonal pattern
    seasonal_factor = [1.4, 1.5, 1.6, 1.2, 1.0, 0.8]
    forecast_prices = []
    
    for i, month in enumerate(forecast_months):
        month_idx = month.month - 1
        seasonal = seasonal_factor[month_idx % 12]
        forecast_price = last_3_months * seasonal
        forecast_prices.append(forecast_price)
    
    df_forecast = pd.DataFrame({
        'Tanggal': forecast_months,
        'Harga_Prediksi': forecast_prices
    })
    
    # Combined chart
    fig_forecast = go.Figure()
    
    # Historical
    fig_forecast.add_trace(go.Scatter(
        x=df_prices['Tanggal'],
        y=df_prices['Harga'],
        mode='lines',
        name='Harga Historis',
        line=dict(color='#FF6B6B', width=2)
    ))
    
    # Forecast
    fig_forecast.add_trace(go.Scatter(
        x=df_forecast['Tanggal'],
        y=df_forecast['Harga_Prediksi'],
        mode='lines+markers',
        name='Prediksi',
        line=dict(color='#4ECDC4', width=2, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig_forecast.update_layout(
        title='Prediksi Harga 6 Bulan Ke Depan',
        xaxis_title='Bulan',
        yaxis_title='Harga (Rp/kg)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Forecast table
    st.subheader("📋 Detail Prediksi")
    
    df_forecast_display = df_forecast.copy()
    df_forecast_display['Bulan'] = df_forecast_display['Tanggal'].dt.strftime('%B %Y')
    df_forecast_display['Harga'] = df_forecast_display['Harga_Prediksi'].apply(lambda x: f"Rp {x:,.0f}/kg")
    
    st.dataframe(
        df_forecast_display[['Bulan', 'Harga']],
        use_container_width=True,
        hide_index=True
    )
    
    st.warning("""
    ⚠️ **Disclaimer:**
    - Prediksi ini adalah estimasi berdasarkan pola historis
    - Harga aktual dapat berbeda karena faktor eksternal
    - Gunakan sebagai referensi, bukan keputusan mutlak
    - Selalu cek harga pasar real-time sebelum menjual
    """)

with tabs[2]:
    st.header("💡 Rekomendasi Waktu Jual")
    
    # Current month
    current_month = datetime.now().month
    
    # Best months to sell (high price months)
    high_price_months = [1, 2, 3, 10, 11, 12]  # Jan-Mar, Oct-Dec
    low_price_months = [6, 7, 8]  # Jun-Aug
    
    if current_month in high_price_months:
        st.success("""
        ✅ **WAKTU BAGUS UNTUK JUAL!**
        
        Bulan ini termasuk periode harga tinggi:
        - Curah hujan tinggi → Produksi rendah
        - Permintaan tinggi (hari raya, musim hujan)
        - Harga cenderung naik
        
        **Rekomendasi:**
        - Jual segera jika sudah panen
        - Sortir grade A untuk harga maksimal
        - Cari pembeli langsung (bypass tengkulak)
        """)
    elif current_month in low_price_months:
        st.error("""
        ❌ **HARGA SEDANG RENDAH**
        
        Bulan ini termasuk periode harga rendah:
        - Panen raya → Oversupply
        - Cuaca bagus → Produksi tinggi
        - Harga tertekan
        
        **Rekomendasi:**
        - Tunda penjualan jika memungkinkan
        - Pertimbangkan olahan (dikeringkan, dibekukan)
        - Jual ke industri dengan kontrak
        - Fokus volume, bukan harga
        """)
    else:
        st.info("""
        ⚠️ **HARGA SEDANG-SEDANG SAJA**
        
        Bulan ini harga cenderung stabil:
        - Transisi musim
        - Supply-demand seimbang
        
        **Rekomendasi:**
        - Monitor harga harian
        - Jual bertahap (tidak sekaligus)
        - Diversifikasi pembeli
        """)
    
    st.markdown("---")
    
    # Strategy recommendations
    st.subheader("📊 Strategi Penjualan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Strategi Harga Tinggi:**
        
        1. **Timing:**
           - Jual saat puncak harga (Jan-Mar)
           - Hindari panen raya (Jun-Aug)
        
        2. **Kualitas:**
           - Sortir ketat (Grade A)
           - Kemasan menarik
           - Bersih & segar
        
        3. **Pasar:**
           - Supermarket/modern market
           - Export (jika organik)
           - Restoran/hotel
        
        4. **Negosiasi:**
           - Jangan terburu-buru
           - Bandingkan harga
           - Kontrak jangka panjang
        """)
    
    with col2:
        st.markdown("""
        **💰 Maksimalkan Profit:**
        
        1. **Diversifikasi:**
           - Jangan jual semua sekaligus
           - Simpan sebagian (jika ada cold storage)
           - Olah menjadi produk lain
        
        2. **Informasi:**
           - Pantau harga BAPANAS
           - Join grup petani
           - Hubungan baik dengan pembeli
        
        3. **Fleksibilitas:**
           - Siap jual cepat saat harga puncak
           - Tahan jika harga jelek
           - Alternatif pasar
        
        4. **Kualitas:**
           - Panen tepat waktu
           - Handling hati-hati
           - Sortasi konsisten
        """)

with tabs[3]:
    st.header("📅 Kalender Harga Tahunan")
    
    # Create heatmap of average prices by month
    st.subheader("🗓️ Pola Harga Bulanan")
    
    # Simulated monthly pattern
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    price_pattern = [50000, 55000, 60000, 45000, 35000, 25000, 22000, 25000, 30000, 40000, 45000, 48000]
    status = ['Tinggi', 'Tinggi', 'Tinggi', 'Sedang', 'Sedang', 'Rendah', 'Rendah', 'Rendah', 'Sedang', 'Sedang', 'Sedang', 'Tinggi']
    
    df_calendar = pd.DataFrame({
        'Bulan': months,
        'Harga Rata-rata': price_pattern,
        'Status': status
    })
    
    # Color-coded table
    def color_status(val):
        if val == 'Tinggi':
            return 'background-color: #90EE90'
        elif val == 'Rendah':
            return 'background-color: #FFB6C1'
        else:
            return 'background-color: #FFE4B5'
    
    df_calendar['Harga'] = df_calendar['Harga Rata-rata'].apply(lambda x: f"Rp {x:,}/kg")
    
    st.dataframe(
        df_calendar[['Bulan', 'Harga', 'Status']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Best planting time
    st.subheader("🌱 Rekomendasi Waktu Tanam")
    
    st.success("""
    **Strategi Optimal:**
    
    1. **Tanam April-Mei**
       - Panen: Juli-September
       - Harga mulai naik (Sep-Okt)
       - Hindari panen raya (Jun-Jul)
    
    2. **Tanam Oktober-November**
       - Panen: Januari-Maret
       - Harga puncak (Jan-Mar)
       - Risiko: Musim hujan
       - Solusi: Greenhouse/drainase bagus
    
    3. **Hindari Tanam:**
       - Desember-Februari (panen Apr-Jun = harga rendah)
       - Juni-Juli (panen Sep-Nov = harga sedang)
    """)
    
    # Price cycle visualization
    fig_cycle = go.Figure()
    
    fig_cycle.add_trace(go.Scatter(
        x=months,
        y=price_pattern,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10)
    ))
    
    fig_cycle.update_layout(
        title='Siklus Harga Tahunan',
        xaxis_title='Bulan',
        yaxis_title='Harga (Rp/kg)',
        height=400
    )
    
    st.plotly_chart(fig_cycle, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>📈 Prediksi Harga Cabai</strong></p>
    <p><small>Data simulasi untuk edukasi - Selalu cek harga real-time</small></p>
</div>
""", unsafe_allow_html=True)
