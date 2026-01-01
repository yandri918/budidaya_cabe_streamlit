"""
🌶️ Budidaya Cabai - Platform Lengkap
Main Dashboard & Navigation
"""

import streamlit as st
import sys
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Budidaya Cabai - Platform Lengkap",
    page_icon="🌶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #C92A2A 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stat-card {
        background: linear-gradient(135deg, #FFE5E5 0%, #FFD0D0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .comparison-table {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌶️ Platform Budidaya Cabai Lengkap</h1>
    <p style="font-size: 1.2rem;">Standar Industri | 6 Skenario Budidaya | AI-Powered</p>
    <p><strong>Organik • Kimia • Campuran | Terbuka • Greenhouse</strong></p>
</div>
""", unsafe_allow_html=True)

# Quick Stats
st.markdown("### 📊 Ringkasan Platform")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h2>12</h2>
        <p>Modul Lengkap</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h2>6</h2>
        <p>Skenario Budidaya</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h2>10+</h2>
        <p>Hama & Penyakit</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h2>100%</h2>
        <p>Berbasis Data</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Features
st.markdown("### 🎯 Fitur Utama")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📅 Kalender Tanam</h4>
        <p>Rekomendasi waktu tanam optimal berdasarkan lokasi & iklim</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>💰 Prediksi Harga</h4>
        <p>ML forecasting 3-6 bulan ke depan</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 AI Saran Terbaik</h4>
        <p>Personalized recommendations untuk sistem budidaya</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>💵 RAB Calculator</h4>
        <p>6 skenario lengkap dengan ROI analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>📋 SOP Lengkap</h4>
        <p>Standard Operating Procedure untuk setiap sistem</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🧪 Kalkulator Pupuk</h4>
        <p>Perhitungan NPK makro & mikro nutrient</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🐛 Hama & Penyakit</h4>
        <p>Database lengkap dengan solusi organik & kimia</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Analisis Bisnis</h4>
        <p>ROI, break-even, cashflow projection</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🌶️ Varietas Cabai</h4>
        <p>10+ varietas dengan rekomendasi</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>💡 Tips & Trik</h4>
        <p>Best practices & troubleshooting</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>📈 Data & Statistik</h4>
        <p>Real-time price & market insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>📚 Panduan Lengkap</h4>
        <p>Step-by-step cultivation guide</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 6 Cultivation Scenarios
st.markdown("### 🆚 6 Skenario Budidaya")

import pandas as pd

scenarios_data = {
    'Skenario': [
        '1. Organik + Terbuka',
        '2. Organik + Greenhouse',
        '3. Kimia + Terbuka',
        '4. Kimia + Greenhouse',
        '5. Campuran + Terbuka',
        '6. Campuran + Greenhouse'
    ],
    'Investasi/ha': [
        'Rp 30-50 juta',
        'Rp 250-400 juta',
        'Rp 20-35 juta',
        'Rp 200-350 juta',
        'Rp 25-40 juta',
        'Rp 220-380 juta'
    ],
    'Yield (ton/ha)': [
        '8-12',
        '25-35',
        '12-18',
        '35-50',
        '10-15',
        '30-45'
    ],
    'Harga Jual (Rp/kg)': [
        '40-60k',
        '50-80k',
        '20-35k',
        '25-40k',
        '30-45k',
        '35-55k'
    ],
    'ROI (bulan)': [
        '18-24',
        '20-30',
        '10-15',
        '15-20',
        '12-18',
        '16-24'
    ]
}

df_scenarios = pd.DataFrame(scenarios_data)
st.dataframe(df_scenarios, use_container_width=True, hide_index=True)

st.markdown("---")

# Getting Started
st.markdown("### 🚀 Mulai Sekarang")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **📚 Pemula?**
    
    Mulai dari:
    1. Panduan Budidaya
    2. AI Saran Terbaik
    3. RAB Calculator
    """)

with col2:
    st.success("""
    **💼 Bisnis?**
    
    Fokus ke:
    1. Analisis Bisnis
    2. Prediksi Harga
    3. Kalender Tanam
    """)

with col3:
    st.warning("""
    **🌱 Organik?**
    
    Lihat:
    1. SOP Organik
    2. Hama & Penyakit (Organik)
    3. Kalkulator Pupuk Organik
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>🌶️ Platform Budidaya Cabai</strong></p>
    <p>Berbasis data dari AgriSensa | Standar Industri | Comprehensive</p>
    <p><small>Gunakan sidebar untuk navigasi ke modul-modul</small></p>
</div>
""", unsafe_allow_html=True)
