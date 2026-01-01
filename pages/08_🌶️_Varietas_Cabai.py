"""
🌶️ Varietas Cabai - Perbandingan Lengkap
Database varietas dengan rekomendasi
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.chili_data import CHILI_VARIETIES

st.set_page_config(
    page_title="Varietas Cabai",
    page_icon="🌶️",
    layout="wide"
)

# Header
st.title("🌶️ Varietas Cabai - Perbandingan Lengkap")
st.markdown("**Pilih varietas terbaik untuk budidaya Anda**")

st.markdown("---")

# Comparison Table
st.subheader("📊 Perbandingan Varietas")

comparison_data = []
for variety_name, variety_data in CHILI_VARIETIES.items():
    comparison_data.append({
        "Varietas": variety_name,
        "Nama Latin": variety_data["nama_latin"],
        "Tinggi": variety_data["karakteristik"]["tinggi"],
        "Umur Panen": variety_data["karakteristik"]["umur_panen"],
        "Yield": variety_data["karakteristik"]["yield"],
        "Tingkat Pedas": variety_data["karakteristik"]["tingkat_pedas"],
        "Harga Benih": f"Rp {variety_data['harga_benih']:,}",
        "Harga Jual (Organik)": f"Rp {variety_data['harga_jual']['organik']:,}/kg"
    })

df_comparison = pd.DataFrame(comparison_data)
st.dataframe(df_comparison, use_container_width=True, hide_index=True)

st.markdown("---")

# Detailed view
st.subheader("📝 Detail Varietas")

for variety_name, variety_data in CHILI_VARIETIES.items():
    with st.expander(f"**{variety_name}** - {variety_data['nama_latin']}", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Karakteristik:**")
            for key, value in variety_data["karakteristik"].items():
                st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
            
            st.markdown(f"\n**Cocok untuk:** {', '.join(variety_data['cocok_untuk'])}")
        
        with col2:
            st.markdown("**Informasi Ekonomi:**")
            st.markdown(f"- **Harga Benih:** Rp {variety_data['harga_benih']:,}/sachet")
            
            st.markdown("\n**Harga Jual:**")
            for sistem, harga in variety_data['harga_jual'].items():
                st.markdown(f"- {sistem.title()}: Rp {harga:,}/kg")

st.markdown("---")

# Recommendation Tool
st.subheader("🎯 Rekomendasi Varietas")

col1, col2 = st.columns(2)

with col1:
    tujuan = st.selectbox(
        "Tujuan Budidaya",
        ["Komersial (Profit)", "Hobi/Konsumsi", "Premium/Export"]
    )
    
    sistem = st.selectbox(
        "Sistem Budidaya",
        ["Organik Terbuka", "Organik Greenhouse", "Kimia Terbuka", 
         "Kimia Greenhouse", "Campuran Terbuka", "Campuran Greenhouse"]
    )

with col2:
    budget = st.selectbox(
        "Budget Benih",
        ["Rendah (<Rp 150k)", "Sedang (Rp 150-200k)", "Tinggi (>Rp 200k)"]
    )
    
    preferensi = st.selectbox(
        "Preferensi",
        ["Cepat Panen", "Yield Tinggi", "Harga Jual Tinggi", "Mudah Perawatan"]
    )

if st.button("🔍 Cari Rekomendasi", type="primary"):
    st.success("✅ Rekomendasi Berdasarkan Kriteria Anda:")
    
    # Simple recommendation logic
    if "Premium" in tujuan or "Export" in tujuan:
        st.markdown("""
        **Rekomendasi: Cabai Hibrida (Hot Beauty)**
        
        ✅ **Alasan:**
        - Yield sangat tinggi (40-60 ton/ha di greenhouse)
        - Kualitas premium
        - Cocok untuk export
        - Tahan penyakit
        
        💰 **Proyeksi:**
        - Investasi benih: Rp 250,000/sachet
        - Harga jual: Rp 35,000-60,000/kg
        - ROI: Excellent (18-24 bulan)
        """)
    elif "Hobi" in tujuan:
        st.markdown("""
        **Rekomendasi: Cabai Rawit**
        
        ✅ **Alasan:**
        - Mudah perawatan
        - Cepat panen (75-90 hari)
        - Cocok lahan kecil
        - Harga benih terjangkau
        
        💰 **Proyeksi:**
        - Investasi benih: Rp 150,000/sachet
        - Harga jual: Rp 35,000-60,000/kg
        - Cocok untuk konsumsi sendiri
        """)
    else:
        if "Greenhouse" in sistem:
            st.markdown("""
            **Rekomendasi: Cabai Merah Besar**
            
            ✅ **Alasan:**
            - Yield tinggi di greenhouse (30-50 ton/ha)
            - Permintaan pasar stabil
            - Harga jual bagus
            - Cocok untuk bisnis
            
            💰 **Proyeksi:**
            - Investasi benih: Rp 135,000/sachet
            - Harga jual: Rp 25,000-50,000/kg
            - ROI: Good (15-20 bulan)
            """)
        else:
            st.markdown("""
            **Rekomendasi: Cabai Keriting**
            
            ✅ **Alasan:**
            - Adaptif di lahan terbuka
            - Yield bagus (12-20 ton/ha)
            - Permintaan tinggi
            - Balance antara yield & harga
            
            💰 **Proyeksi:**
            - Investasi benih: Rp 140,000/sachet
            - Harga jual: Rp 30,000-55,000/kg
            - ROI: Good (12-18 bulan)
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>🌶️ Varietas Cabai</strong></p>
    <p><small>Pilih varietas sesuai tujuan & kondisi Anda</small></p>
</div>
""", unsafe_allow_html=True)
