"""
📅 Kalender Tanam Cabai
Rekomendasi waktu tanam optimal berdasarkan lokasi & musim
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.chili_data import PLANTING_CALENDAR

st.set_page_config(
    page_title="Kalender Tanam Cabai",
    page_icon="📅",
    layout="wide"
)

# Header
st.title("📅 Kalender Tanam Cabai")
st.markdown("**Rekomendasi waktu tanam optimal berdasarkan lokasi & musim**")

st.markdown("---")

# Input
col1, col2 = st.columns(2)

with col1:
    region = st.selectbox(
        "Pilih Wilayah",
        ["Jawa", "Sumatera", "Sulawesi", "Kalimantan", "Bali & Nusa Tenggara"]
    )
    
    altitude = st.number_input(
        "Ketinggian Tempat (mdpl)",
        min_value=0,
        max_value=2000,
        value=500,
        step=50,
        help="Dataran rendah: 0-700 mdpl, Dataran tinggi: >700 mdpl"
    )

with col2:
    method = st.selectbox(
        "Metode Budidaya",
        ["Terbuka (Open Field)", "Greenhouse (Terkontrol)"]
    )
    
    current_month = datetime.now().month
    start_month = st.selectbox(
        "Rencana Mulai Tanam",
        ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
        index=current_month - 1
    )

# Analysis
st.markdown("---")
st.header("📊 Analisis & Rekomendasi")

# Get calendar data
if region in PLANTING_CALENDAR:
    calendar_data = PLANTING_CALENDAR[region]
else:
    calendar_data = PLANTING_CALENDAR["Jawa"]  # Default

# Recommendations
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌤️ Kondisi Iklim")
    
    if altitude < 700:
        st.info("""
        **Dataran Rendah (0-700 mdpl)**
        - Suhu: 25-32°C
        - Cocok untuk: Cabai rawit, Cabai keriting
        - Tantangan: Hama lebih aktif
        - Solusi: Monitoring intensif
        """)
    else:
        st.info("""
        **Dataran Tinggi (>700 mdpl)**
        - Suhu: 20-25°C
        - Cocok untuk: Cabai merah besar, Cabai hibrida
        - Keuntungan: Hama lebih sedikit
        - Perhatian: Penyakit jamur (kelembaban tinggi)
        """)

with col2:
    st.subheader("📅 Waktu Tanam Optimal")
    
    if "Greenhouse" in method:
        st.success("""
        **Greenhouse (Sepanjang Tahun)**
        - Bisa tanam kapan saja
        - Kontrol iklim lebih baik
        - Risiko cuaca minimal
        - ROI lebih cepat
        """)
    else:
        # Determine best season
        if start_month in ["April", "Mei", "Juni"]:
            st.success("""
            **Musim Kemarau (April-Mei)**
            ✅ **WAKTU TERBAIK!**
            - Curah hujan rendah
            - Hama/penyakit lebih terkontrol
            - Harga jual tinggi (panen Juli-Sept)
            - Kualitas buah bagus
            """)
        elif start_month in ["Oktober", "November"]:
            st.warning("""
            **Awal Musim Hujan (Okt-Nov)**
            ⚠️ **RISIKO SEDANG**
            - Perlu drainase baik
            - Risiko penyakit jamur tinggi
            - Harga jual sedang
            - Perlu greenhouse/naungan
            """)
        else:
            st.error("""
            **Musim Hujan (Des-Mar)**
            ❌ **TIDAK DIREKOMENDASIKAN**
            - Curah hujan tinggi
            - Penyakit sulit dikontrol
            - Kualitas buah menurun
            - Harga jual rendah
            """)

st.markdown("---")

# Timeline
st.subheader("📆 Timeline Budidaya (120 Hari)")

month_map = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
    "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
    "September": 9, "Oktober": 10, "November": 11, "Desember": 12
}

start_date = datetime(2024, month_map[start_month], 1)

timeline_data = []
phases = [
    ("Persiapan Lahan", 0, 14),
    ("Pembibitan", 0, 30),
    ("Penanaman", 30, 35),
    ("Vegetatif", 35, 60),
    ("Berbunga", 60, 75),
    ("Berbuah & Panen", 75, 120)
]

for phase, start_day, end_day in phases:
    phase_start = start_date + timedelta(days=start_day)
    phase_end = start_date + timedelta(days=end_day)
    
    timeline_data.append({
        "Fase": phase,
        "Mulai": phase_start.strftime("%d %b"),
        "Selesai": phase_end.strftime("%d %b"),
        "Durasi": f"{end_day - start_day} hari"
    })

df_timeline = pd.DataFrame(timeline_data)
st.dataframe(df_timeline, use_container_width=True, hide_index=True)

# Harvest prediction
harvest_start = start_date + timedelta(days=90)
harvest_end = start_date + timedelta(days=120)

st.success(f"""
🎯 **Prediksi Panen:**
- Panen Perdana: **{harvest_start.strftime("%d %B %Y")}**
- Panen Terakhir: **{harvest_end.strftime("%d %B %Y")}**
- Periode Panen: **30 hari** (panen bertahap 7-10 hari sekali)
""")

st.markdown("---")

# Regional recommendations
st.subheader(f"🗺️ Rekomendasi Khusus: {region}")

if region == "Jawa":
    st.markdown("""
    **Jawa (Sentra Produksi Cabai):**
    
    **Waktu Tanam Terbaik:**
    - **Musim Kemarau:** April-Mei (panen Juli-September)
    - **Musim Hujan:** Oktober-November (panen Januari-Maret)
    
    **Wilayah Unggulan:**
    - Dataran Tinggi: Garut, Magelang, Malang
    - Dataran Rendah: Brebes, Ngawi, Kediri
    
    **Tips:**
    - Hindari tanam Desember-Februari (puncak hujan)
    - Gunakan mulsa plastik (wajib)
    - Drainase harus sempurna
    """)
elif region == "Sumatera":
    st.markdown("""
    **Sumatera (Curah Hujan Tinggi):**
    
    **Rekomendasi:**
    - **Greenhouse sangat dianjurkan**
    - Tanam sepanjang tahun (dengan greenhouse)
    - Tanpa greenhouse: Mei-Agustus (relatif kering)
    
    **Wilayah Potensial:**
    - Sumatera Utara: Dataran tinggi Karo
    - Sumatera Barat: Dataran tinggi Agam
    - Lampung: Dataran rendah
    
    **Tantangan:**
    - Curah hujan tinggi sepanjang tahun
    - Kelembaban tinggi (penyakit jamur)
    - Perlu sistem drainase excellent
    """)
elif region == "Sulawesi":
    st.markdown("""
    **Sulawesi (Iklim Tropis):**
    
    **Waktu Tanam:**
    - Musim Kemarau: Mei-Juni
    - Panen: Agustus-Oktober
    
    **Wilayah Cocok:**
    - Sulawesi Selatan: Enrekang, Gowa
    - Sulawesi Utara: Minahasa (dataran tinggi)
    
    **Keuntungan:**
    - Suhu sejuk di dataran tinggi
    - Hama relatif sedikit
    - Kualitas buah bagus
    """)

st.markdown("---")

# Monthly planting guide
st.subheader("📊 Panduan Tanam per Bulan")

monthly_guide = {
    "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
    "Jawa": ["❌", "❌", "⚠️", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "✅", "⚠️", "❌"],
    "Sumatera (GH)": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Sulawesi": ["❌", "❌", "❌", "⚠️", "✅", "✅", "⚠️", "❌", "❌", "⚠️", "⚠️", "❌"]
}

df_monthly = pd.DataFrame(monthly_guide)
st.dataframe(df_monthly, use_container_width=True, hide_index=True)

st.caption("""
**Keterangan:**
- ✅ = Sangat Direkomendasikan
- ⚠️ = Bisa, tapi perlu perhatian extra
- ❌ = Tidak Direkomendasikan
- GH = Greenhouse
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>📅 Kalender Tanam Cabai</strong></p>
    <p><small>Rekomendasi berdasarkan data iklim & pengalaman petani</small></p>
</div>
""", unsafe_allow_html=True)
