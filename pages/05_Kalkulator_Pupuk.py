"""
🧪 Kalkulator Pupuk Cabai
NPK Makro & Mikro Nutrient Calculator
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

st.set_page_config(
    page_title="Kalkulator Pupuk Cabai",
    page_icon="🧪",
    layout="wide"
)

# Header
st.title("🧪 Kalkulator Pupuk Cabai")
st.markdown("**Perhitungan kebutuhan pupuk NPK makro & mikro**")

st.markdown("---")

# Tabs
tabs = st.tabs(["📊 Kalkulator", "📚 Panduan Pemupukan", "💰 Estimasi Biaya"])

with tabs[0]:
    st.header("📊 Kalkulator Kebutuhan Pupuk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Data")
        
        luas_ha = st.number_input(
            "Luas Lahan (Ha)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1
        )
        
        sistem = st.selectbox(
            "Sistem Budidaya",
            ["Organik", "Kimia", "Campuran"]
        )
        
        fase = st.selectbox(
            "Fase Pertumbuhan",
            ["Vegetatif (0-60 HST)", "Berbunga (60-75 HST)", "Berbuah (75-120 HST)"]
        )
        
        target_yield = st.number_input(
            "Target Produksi (ton/ha)",
            min_value=5.0,
            max_value=50.0,
            value=15.0,
            step=1.0
        )
    
    with col2:
        st.subheader("Hasil Uji Tanah (Opsional)")
        
        st.info("Jika tidak ada data uji tanah, gunakan nilai default")
        
        ph_tanah = st.number_input("pH Tanah", min_value=4.0, max_value=8.0, value=6.5, step=0.1)
        n_tanah = st.selectbox("Status N", ["Rendah", "Sedang", "Tinggi"], index=1)
        p_tanah = st.selectbox("Status P", ["Rendah", "Sedang", "Tinggi"], index=1)
        k_tanah = st.selectbox("Status K", ["Rendah", "Sedang", "Tinggi"], index=1)
    
    if st.button("🧮 Hitung Kebutuhan Pupuk", type="primary"):
        # Kebutuhan NPK per fase (kg/ha)
        npk_requirements = {
            "Vegetatif (0-60 HST)": {"N": 120, "P": 60, "K": 80},
            "Berbunga (60-75 HST)": {"N": 80, "P": 80, "K": 120},
            "Berbuah (75-120 HST)": {"N": 60, "P": 100, "K": 150}
        }
        
        base_npk = npk_requirements[fase]
        
        # Adjust based on soil status
        adjustments = {"Rendah": 1.3, "Sedang": 1.0, "Tinggi": 0.7}
        
        n_need = base_npk["N"] * adjustments[n_tanah] * luas_ha
        p_need = base_npk["P"] * adjustments[p_tanah] * luas_ha
        k_need = base_npk["K"] * adjustments[k_tanah] * luas_ha
        
        st.success("✅ Perhitungan Selesai!")
        
        # Display results
        st.subheader("📋 Kebutuhan NPK")
        
        col_n, col_p, col_k = st.columns(3)
        
        with col_n:
            st.metric("Nitrogen (N)", f"{n_need:.1f} kg", help="Untuk pertumbuhan vegetatif")
        
        with col_p:
            st.metric("Fosfor (P₂O₅)", f"{p_need:.1f} kg", help="Untuk pembungaan & perakaran")
        
        with col_k:
            st.metric("Kalium (K₂O)", f"{k_need:.1f} kg", help="Untuk kualitas buah")
        
        st.markdown("---")
        
        # Rekomendasi pupuk
        st.subheader("💊 Rekomendasi Pupuk")
        
        if sistem == "Organik":
            st.markdown("""
            **Pupuk Organik:**
            
            1. **Pupuk Kandang Matang**
               - Dosis: {} ton
               - Aplikasi: Pupuk dasar, 2 minggu sebelum tanam
               - Kandungan: N 0.5%, P 0.3%, K 0.5%
            
            2. **Kompos Premium**
               - Dosis: {} ton
               - Aplikasi: Campuran dengan pupuk kandang
               - Kandungan: N 1.5%, P 1%, K 1%
            
            3. **Pupuk Cair Organik (POC)**
               - Dosis: 5-10 ml/L air
               - Frekuensi: 1x seminggu
               - Aplikasi: Kocor/semprot daun
            
            4. **PGPR (Plant Growth Promoting Rhizobacteria)**
               - Dosis: 5 ml/L air
               - Frekuensi: 2 minggu sekali
               - Manfaat: Fiksasi N, pelarut P
            
            5. **MOL (Mikro Organisme Lokal)**
               - Dosis: 100-200 ml/tanaman
               - Frekuensi: 2 minggu sekali
               - Aplikasi: Kocor ke tanah
            """.format(
                round(n_need / 5, 1),  # Pupuk kandang
                round(p_need / 10, 1)  # Kompos
            ))
            
        elif sistem == "Kimia":
            # Hitung kebutuhan pupuk kimia
            urea_kg = n_need / 0.46  # Urea 46% N
            sp36_kg = p_need / 0.36  # SP-36 36% P2O5
            kcl_kg = k_need / 0.60   # KCl 60% K2O
            npk_kg = (n_need + p_need + k_need) / 0.48  # NPK 16-16-16
            
            st.markdown(f"""
            **Pupuk Kimia:**
            
            **Opsi 1: Pupuk Tunggal**
            1. **Urea (46% N)**
               - Kebutuhan: {urea_kg:.1f} kg
               - Aplikasi: 3-4 kali, interval 2 minggu
               - Dosis per aplikasi: {urea_kg/4:.1f} kg
            
            2. **SP-36 (36% P₂O₅)**
               - Kebutuhan: {sp36_kg:.1f} kg
               - Aplikasi: 2 kali (awal + fase berbunga)
               - Dosis per aplikasi: {sp36_kg/2:.1f} kg
            
            3. **KCl (60% K₂O)**
               - Kebutuhan: {kcl_kg:.1f} kg
               - Aplikasi: 3 kali (vegetatif, berbunga, berbuah)
               - Dosis per aplikasi: {kcl_kg/3:.1f} kg
            
            **Opsi 2: NPK Majemuk**
            1. **NPK 16-16-16**
               - Kebutuhan: {npk_kg:.1f} kg
               - Aplikasi: 4-5 kali selama musim tanam
               - Dosis per aplikasi: {npk_kg/5:.1f} kg
            
            2. **KNO₃ (Kalium Nitrat)**
               - Kebutuhan: {k_need*0.8:.1f} kg
               - Aplikasi: Fase berbunga & berbuah
               - Dosis: 5-10 g/tanaman
            """)
            
        else:  # Campuran
            st.markdown(f"""
            **Pupuk Campuran (IPM):**
            
            **Pupuk Dasar (Organik):**
            1. Pupuk Kandang: {round(n_need/10, 1)} ton
            2. Kompos: {round(p_need/15, 1)} ton
            
            **Pupuk Susulan (Kimia):**
            1. NPK 16-16-16: {round((n_need + p_need + k_need)/0.48 * 0.5, 1)} kg
            2. KNO₃: {round(k_need*0.5, 1)} kg
            
            **Pupuk Hayati:**
            1. PGPR: 5 ml/L, 2 minggu sekali
            2. Trichoderma: 10 g/L, 2 minggu sekali
            """)
        
        st.markdown("---")
        
        # Mikro nutrient
        st.subheader("🔬 Kebutuhan Mikro Nutrient")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Mikro Nutrient Penting:**
            - **Fe (Besi)**: 2-5 kg/ha
            - **Mn (Mangan)**: 1-3 kg/ha
            - **Zn (Seng)**: 1-2 kg/ha
            """)
        
        with col2:
            st.markdown("""
            **Aplikasi:**
            - **Cu (Tembaga)**: 0.5-1 kg/ha
            - **B (Boron)**: 0.3-0.5 kg/ha
            - **Mo (Molibdenum)**: 0.1-0.2 kg/ha
            """)
        
        st.info("""
        💡 **Cara Aplikasi Mikro:**
        - Semprot daun dengan pupuk mikro lengkap
        - Konsentrasi: 1-2 g/L air
        - Frekuensi: 2 minggu sekali
        - Waktu: Pagi/sore hari
        """)

with tabs[1]:
    st.header("📚 Panduan Pemupukan Cabai")
    
    st.markdown("""
    ## Jadwal Pemupukan Lengkap
    
    ### Fase 1: Vegetatif (0-60 HST)
    **Fokus: Pertumbuhan daun & batang**
    
    - **Minggu 1-2:** Pupuk dasar (organik/NPK)
    - **Minggu 3-4:** Urea/POC (tinggi N)
    - **Minggu 5-6:** NPK seimbang
    - **Minggu 7-8:** Urea + KCl
    
    **Dosis per tanaman:**
    - Organik: 200-300 ml POC
    - Kimia: 5-10 g NPK
    
    ---
    
    ### Fase 2: Berbunga (60-75 HST)
    **Fokus: Pembentukan bunga**
    
    - **Minggu 9-10:** NPK + KCl (tinggi P & K)
    - **Minggu 11:** Pupuk daun + mikro
    
    **Dosis per tanaman:**
    - Organik: 300 ml POC tinggi P
    - Kimia: 10 g NPK + 5 g KNO₃
    
    ---
    
    ### Fase 3: Berbuah (75-120 HST)
    **Fokus: Kualitas & kuantitas buah**
    
    - **Minggu 12-14:** KNO₃ / KCl (tinggi K)
    - **Minggu 15-16:** Pupuk daun + booster
    
    **Dosis per tanaman:**
    - Organik: 300 ml POC tinggi K
    - Kimia: 10 g KNO₃
    
    ---
    
    ## Tips Pemupukan
    
    ✅ **DO:**
    - Pupuk saat tanah lembab
    - Aplikasi pagi/sore hari
    - Kocor di sekitar tanaman (jarak 10-15 cm dari batang)
    - Siram setelah pemupukan
    - Rotasi jenis pupuk
    
    ❌ **DON'T:**
    - Pupuk saat terik matahari
    - Over-dosis (lebih bahaya dari kurang)
    - Pupuk menempel batang (bisa terbakar)
    - Pupuk saat tanah kering
    - Hanya fokus N (harus seimbang NPK)
    """)

with tabs[2]:
    st.header("💰 Estimasi Biaya Pupuk")
    
    luas_calc = st.number_input("Luas Lahan (Ha)", min_value=0.1, max_value=100.0, value=1.0, step=0.1, key="cost_calc")
    sistem_calc = st.selectbox("Sistem", ["Organik", "Kimia", "Campuran"], key="cost_sistem")
    
    if sistem_calc == "Organik":
        biaya_data = {
            "Item": [
                "Pupuk Kandang (20 ton)",
                "Kompos (10 ton)",
                "POC (200 liter)",
                "PGPR (50 liter)",
                "MOL (100 liter)",
                "Pupuk Daun Organik"
            ],
            "Harga Satuan": [
                "Rp 800,000/ton",
                "Rp 1,000,000/ton",
                "Rp 25,000/liter",
                "Rp 50,000/liter",
                "Rp 15,000/liter",
                "Rp 2,000,000/paket"
            ],
            "Total": [
                16000000 * luas_calc,
                10000000 * luas_calc,
                5000000 * luas_calc,
                2500000 * luas_calc,
                1500000 * luas_calc,
                2000000 * luas_calc
            ]
        }
    elif sistem_calc == "Kimia":
        biaya_data = {
            "Item": [
                "Urea (300 kg)",
                "SP-36 (200 kg)",
                "KCl (250 kg)",
                "NPK 16-16-16 (400 kg)",
                "KNO₃ (100 kg)",
                "Pupuk Daun & Mikro"
            ],
            "Harga Satuan": [
                "Rp 3,500/kg",
                "Rp 4,000/kg",
                "Rp 5,000/kg",
                "Rp 18,000/kg",
                "Rp 35,000/kg",
                "Rp 2,000,000/paket"
            ],
            "Total": [
                1050000 * luas_calc,
                800000 * luas_calc,
                1250000 * luas_calc,
                7200000 * luas_calc,
                3500000 * luas_calc,
                2000000 * luas_calc
            ]
        }
    else:
        biaya_data = {
            "Item": [
                "Pupuk Kandang (10 ton)",
                "Kompos (5 ton)",
                "NPK 16-16-16 (200 kg)",
                "KNO₃ (50 kg)",
                "PGPR (30 liter)",
                "Pupuk Daun"
            ],
            "Harga Satuan": [
                "Rp 800,000/ton",
                "Rp 1,000,000/ton",
                "Rp 18,000/kg",
                "Rp 35,000/kg",
                "Rp 50,000/liter",
                "Rp 1,500,000/paket"
            ],
            "Total": [
                8000000 * luas_calc,
                5000000 * luas_calc,
                3600000 * luas_calc,
                1750000 * luas_calc,
                1500000 * luas_calc,
                1500000 * luas_calc
            ]
        }
    
    df_biaya = pd.DataFrame(biaya_data)
    df_biaya['Total'] = df_biaya['Total'].apply(lambda x: f"Rp {x:,.0f}")
    
    st.dataframe(df_biaya, use_container_width=True, hide_index=True)
    
    # Total
    total_biaya = sum([float(x.replace('Rp ', '').replace(',', '')) for x in df_biaya['Total']])
    
    st.success(f"""
    **💰 Total Biaya Pupuk: Rp {total_biaya:,.0f}**
    
    Untuk {luas_calc} ha selama 1 musim tanam (4 bulan)
    
    **Per Bulan:** Rp {total_biaya/4:,.0f}
    **Per Hari:** Rp {total_biaya/120:,.0f}
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>🧪 Kalkulator Pupuk Cabai</strong></p>
    <p><small>Perhitungan berdasarkan standar agronomis</small></p>
</div>
""", unsafe_allow_html=True)
