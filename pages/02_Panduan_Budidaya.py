"""
📚 Panduan Budidaya Cabai Lengkap
Step-by-step cultivation guide
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.chili_data import GROWTH_PHASES, CLIMATE_REQUIREMENTS, SOIL_REQUIREMENTS, CHILI_VARIETIES

st.set_page_config(
    page_title="Panduan Budidaya Cabai",
    page_icon="📚",
    layout="wide"
)

# Header
st.title("📚 Panduan Budidaya Cabai Lengkap")
st.markdown("**Step-by-step guide dari persiapan hingga panen**")

st.markdown("---")

# Tabs
tabs = st.tabs([
    "🌱 Persiapan",
    "📈 Tahapan Budidaya",
    "🌶️ Varietas",
    "🌡️ Syarat Tumbuh",
    "💡 Tips & Trik"
])

with tabs[0]:
    st.header("🌱 Persiapan Lahan & Penanaman")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1️⃣ Persiapan Lahan")
        st.markdown("""
        **A. Pengolahan Tanah:**
        - Bajak dalam 30-40 cm
        - Buat bedengan tinggi 30-40 cm, lebar 100-120 cm
        - Jarak antar bedengan 50-60 cm (untuk drainase)
        - Biarkan tanah "istirahat" 1-2 minggu
        
        **B. Pemupukan Dasar:**
        - Pupuk kandang matang: 20-30 ton/ha
        - Kapur dolomit (jika pH <6.0): 1-2 ton/ha
        - Aplikasi 2 minggu sebelum tanam
        - Campur rata dengan tanah
        
        **C. Pemasangan Mulsa:**
        - Gunakan mulsa plastik hitam-perak
        - Pasang rapi, kencangkan dengan tanah
        - Buat lubang tanam diameter 8-10 cm
        - Jarak tanam: 60 x 70 cm atau 50 x 60 cm
        """)
    
    with col2:
        st.subheader("2️⃣ Pembibitan")
        st.markdown("""
        **A. Persiapan Media Semai:**
        - Campuran: tanah + kompos + sekam (1:1:1)
        - Sterilisasi media (opsional)
        - Gunakan tray semai atau polybag kecil
        
        **B. Penyemaian:**
        - Rendam benih 2-4 jam (air hangat)
        - Tanam 1-2 biji per lubang
        - Kedalaman 0.5-1 cm
        - Tutup tipis dengan media
        - Siram dengan sprayer halus
        
        **C. Perawatan Bibit:**
        - Penyiraman 2x sehari (pagi & sore)
        - Naungi 50% (paranet)
        - Umur 25-30 hari siap tanam
        - Ciri: 4-6 daun sejati, tinggi 10-15 cm
        
        **D. Pengerasan Bibit:**
        - 7 hari sebelum tanam
        - Kurangi penyiraman
        - Buka naungan bertahap
        - Semprot pupuk daun (opsional)
        """)
    
    st.markdown("---")
    
    st.subheader("3️⃣ Penanaman")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Waktu Tanam Ideal:**
        - Awal musim kemarau (April-Mei)
        - Atau akhir musim hujan (September-Oktober)
        - Hindari puncak musim hujan
        """)
    
    with col2:
        st.success("""
        **Cara Tanam:**
        - Tanam sore hari (tidak panas)
        - Buat lubang di mulsa
        - Keluarkan bibit dari polybag
        - Tanam tegak, jangan terlalu dalam
        - Padatkan tanah di sekitar bibit
        """)
    
    with col3:
        st.warning("""
        **Penyulaman:**
        - Lakukan 7-10 hari setelah tanam
        - Ganti bibit yang mati/tidak tumbuh
        - Gunakan bibit cadangan
        """)

with tabs[1]:
    st.header("📈 Tahapan Budidaya (0-120 Hari)")
    
    for phase_name, phase_data in GROWTH_PHASES.items():
        with st.expander(f"**{phase_name}** ({phase_data['hari']})", expanded=True):
            st.markdown(f"**Deskripsi:** {phase_data['deskripsi']}")
            
            st.markdown("**Kegiatan Utama:**")
            for kegiatan in phase_data['kegiatan']:
                st.markdown(f"- {kegiatan}")
    
    st.markdown("---")
    
    st.subheader("📅 Timeline Detail")
    
    timeline_data = {
        "Hari": ["0-7", "7-14", "14-21", "21-30", "30-45", "45-60", "60-75", "75-90", "90-120"],
        "Kegiatan": [
            "Penyemaian benih",
            "Perawatan bibit (penyiraman, naungi)",
            "Pengerasan bibit",
            "Penanaman di lahan",
            "Pemupukan susulan 1, penyiangan",
            "Pemupukan susulan 2, pemasangan ajir",
            "Fase berbunga, pemupukan K tinggi",
            "Panen perdana",
            "Panen rutin (7-10 hari sekali)"
        ],
        "Pupuk": [
            "-",
            "Pupuk daun (opsional)",
            "-",
            "Pupuk dasar (NPK)",
            "Urea + NPK",
            "NPK + KCl",
            "KNO3 / KCl",
            "Pupuk daun + K",
            "Pupuk daun"
        ]
    }
    
    import pandas as pd
    df_timeline = pd.DataFrame(timeline_data)
    st.dataframe(df_timeline, use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("🌶️ Varietas Cabai")
    
    for variety_name, variety_data in CHILI_VARIETIES.items():
        with st.expander(f"**{variety_name}** - {variety_data['nama_latin']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Karakteristik:**")
                for key, value in variety_data['karakteristik'].items():
                    st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
            
            with col2:
                st.markdown("**Informasi Ekonomi:**")
                st.markdown(f"- **Harga Benih:** Rp {variety_data['harga_benih']:,}/sachet")
                st.markdown("**Harga Jual:**")
                for sistem, harga in variety_data['harga_jual'].items():
                    st.markdown(f"  - {sistem.title()}: Rp {harga:,}/kg")
                
                st.markdown(f"**Cocok untuk:** {', '.join(variety_data['cocok_untuk'])}")

with tabs[3]:
    st.header("🌡️ Syarat Tumbuh Cabai")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌤️ Iklim")
        for key, value in CLIMATE_REQUIREMENTS.items():
            st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
    
    with col2:
        st.subheader("🌱 Tanah")
        st.markdown(f"- **Tekstur:** {SOIL_REQUIREMENTS['tekstur']}")
        st.markdown(f"- **Drainase:** {SOIL_REQUIREMENTS['drainase']}")
        st.markdown(f"- **Bahan Organik:** {SOIL_REQUIREMENTS['bahan_organik']}")
        
        st.markdown("**Kebutuhan NPK:**")
        for nutrient, level in SOIL_REQUIREMENTS['npk'].items():
            st.markdown(f"  - {nutrient.upper()}: {level}")
    
    st.markdown("---")
    
    st.subheader("🔧 Persiapan Tanah")
    for idx, step in enumerate(SOIL_REQUIREMENTS['persiapan'], 1):
        st.markdown(f"{idx}. {step}")

with tabs[4]:
    st.header("💡 Tips & Trik Sukses")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ DO's (Lakukan):**
        
        1. **Rotasi Tanaman**
           - Jangan tanam cabai terus-menerus
           - Rotasi dengan jagung/kacang
           - Istirahatkan lahan 1-2 bulan
        
        2. **Mulsa Wajib**
           - Jaga kelembaban tanah
           - Cegah gulma
           - Kurangi percikan tanah (penyakit)
        
        3. **Pemupukan Berimbang**
           - Jangan hanya N tinggi
           - Fase berbuah butuh K tinggi
           - Gunakan pupuk mikro
        
        4. **Monitoring Rutin**
           - Cek tanaman setiap hari
           - Deteksi hama/penyakit dini
           - Catat perkembangan
        
        5. **Panen Tepat Waktu**
           - Jangan terlalu muda/tua
           - Panen pagi/sore hari
           - Sortir berdasarkan kualitas
        """)
    
    with col2:
        st.error("""
        **❌ DON'Ts (Hindari):**
        
        1. **Tanam Terlalu Rapat**
           - Sirkulasi udara buruk
           - Kelembaban tinggi
           - Penyakit mudah menyebar
        
        2. **Over-watering**
           - Akar busuk
           - Penyakit jamur
           - Bunga/buah rontok
        
        3. **Pestisida Berlebihan**
           - Resistensi hama
           - Bunuh musuh alami
           - Residu tinggi
        
        4. **Abaikan Sanitasi**
           - Buang tanaman sakit
           - Bersihkan gulma
           - Sterilisasi alat
        
        5. **Panen Sembarangan**
           - Merusak tanaman
           - Buah memar
           - Harga jual turun
        """)
    
    st.markdown("---")
    
    st.info("""
    **🎯 Kunci Sukses Budidaya Cabai:**
    
    1. **Bibit Berkualitas** - 50% kesuksesan
    2. **Pemupukan Tepat** - Sesuai fase pertumbuhan
    3. **Pengendalian Hama/Penyakit** - Preventif lebih baik
    4. **Manajemen Air** - Tidak kelebihan, tidak kekurangan
    5. **Timing Panen** - Saat harga bagus
    6. **Kualitas Produk** - Sortir & grading
    7. **Pemasaran** - Jangan jual ke tengkulak saja
    8. **Pencatatan** - Track biaya & hasil
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>📚 Panduan Budidaya Cabai</strong></p>
    <p><small>Berdasarkan best practices & pengalaman petani sukses</small></p>
</div>
""", unsafe_allow_html=True)
