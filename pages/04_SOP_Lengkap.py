"""
📋 SOP (Standard Operating Procedure) Lengkap
6 Skenario Budidaya Cabai
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

st.set_page_config(
    page_title="SOP Budidaya Cabai",
    page_icon="📋",
    layout="wide"
)

# Header
st.title("📋 SOP Budidaya Cabai Lengkap")
st.markdown("**Standard Operating Procedure untuk 6 Skenario**")

st.markdown("---")

# Scenario selection
scenario = st.selectbox(
    "Pilih Skenario Budidaya",
    [
        "Organik + Terbuka",
        "Organik + Greenhouse",
        "Kimia + Terbuka",
        "Kimia + Greenhouse",
        "Campuran + Terbuka",
        "Campuran + Greenhouse"
    ]
)

st.markdown("---")

# SOP Content based on scenario
if "Organik" in scenario:
    fertilizer_type = "Organik (Kompos, Pupuk Kandang, MOL, PGPR)"
    pesticide_type = "Biopestisida (Neem oil, Trichoderma, Beauveria)"
elif "Kimia" in scenario:
    fertilizer_type = "Kimia (Urea, NPK, SP-36, KCl)"
    pesticide_type = "Pestisida Kimia (Insektisida, Fungisida)"
else:
    fertilizer_type = "Campuran (Organik + Kimia)"
    pesticide_type = "IPM (Biopestisida + Kimia darurat)"

if "Greenhouse" in scenario:
    location_type = "Greenhouse (Terkontrol)"
    irrigation = "Sistem Irigasi Otomatis/Fertigasi"
else:
    location_type = "Lahan Terbuka"
    irrigation = "Irigasi Manual/Drip"

# Display SOP
st.info(f"""
**Skenario:** {scenario}
- **Lokasi:** {location_type}
- **Pupuk:** {fertilizer_type}
- **Pestisida:** {pesticide_type}
- **Irigasi:** {irrigation}
""")

# Tabs for different phases
tabs = st.tabs([
    "1️⃣ Persiapan",
    "2️⃣ Pembibitan",
    "3️⃣ Penanaman",
    "4️⃣ Pemeliharaan",
    "5️⃣ Panen",
    "📝 Checklist"
])

with tabs[0]:
    st.header("1️⃣ SOP Persiapan Lahan")
    
    if "Greenhouse" in scenario:
        st.markdown("""
        ### A. Persiapan Greenhouse
        - [ ] Bersihkan greenhouse dari sisa tanaman sebelumnya
        - [ ] Sterilisasi struktur dengan disinfektan
        - [ ] Cek sistem ventilasi dan shading
        - [ ] Pastikan sistem irigasi berfungsi
        - [ ] Atur suhu optimal (25-30°C)
        
        ### B. Persiapan Media Tanam
        - [ ] Siapkan media: Cocopeat + Kompos + Sekam (1:1:1)
        - [ ] Sterilisasi media (opsional)
        - [ ] Isi polybag/pot (ukuran 30-40 cm)
        - [ ] Susun polybag dengan jarak 50x60 cm
        """)
    else:
        st.markdown("""
        ### A. Pengolahan Tanah
        - [ ] Bajak tanah sedalam 30-40 cm
        - [ ] Buat bedengan tinggi 30-40 cm, lebar 100-120 cm
        - [ ] Jarak antar bedengan 50-60 cm
        - [ ] Biarkan tanah "istirahat" 1-2 minggu
        
        ### B. Pemupukan Dasar
        """)
        
        if "Organik" in scenario:
            st.markdown("""
            - [ ] Aplikasi pupuk kandang matang: 20-30 ton/ha
            - [ ] Kompos premium: 10-15 ton/ha
            - [ ] Kapur dolomit (jika pH <6.0): 1-2 ton/ha
            - [ ] Campur rata dengan tanah
            - [ ] Tunggu 2 minggu sebelum tanam
            """)
        else:
            st.markdown("""
            - [ ] Aplikasi pupuk kandang: 10-15 ton/ha
            - [ ] NPK 16-16-16: 200-300 kg/ha
            - [ ] Kapur dolomit (jika pH <6.0): 1-2 ton/ha
            - [ ] Campur rata dengan tanah
            - [ ] Tunggu 1 minggu sebelum tanam
            """)
    
    st.markdown("""
    ### C. Pemasangan Mulsa
    - [ ] Pasang mulsa plastik hitam-perak
    - [ ] Kencangkan dengan tanah/pasak
    - [ ] Buat lubang tanam diameter 8-10 cm
    - [ ] Jarak tanam: 60x70 cm atau 50x60 cm
    """)

with tabs[1]:
    st.header("2️⃣ SOP Pembibitan (0-30 Hari)")
    
    st.markdown("""
    ### A. Persiapan Media Semai
    - [ ] Campuran: Tanah + Kompos + Sekam (1:1:1)
    - [ ] Sterilisasi media (opsional: kukus/solarisasi)
    - [ ] Isi tray semai atau polybag kecil
    - [ ] Siram hingga lembab
    
    ### B. Penyemaian (Hari 0-7)
    """)
    
    if "Organik" in scenario:
        st.markdown("""
        - [ ] Gunakan benih organik bersertifikat
        - [ ] Rendam benih 2-4 jam (air hangat + POC)
        - [ ] Tanam 1-2 biji per lubang, kedalaman 0.5-1 cm
        - [ ] Tutup tipis dengan media
        - [ ] Siram dengan sprayer halus
        - [ ] Naungi 50% (paranet)
        """)
    else:
        st.markdown("""
        - [ ] Gunakan benih hibrida berkualitas
        - [ ] Rendam benih 2-4 jam (air hangat)
        - [ ] Tanam 1-2 biji per lubang, kedalaman 0.5-1 cm
        - [ ] Tutup tipis dengan media
        - [ ] Siram dengan sprayer halus
        - [ ] Naungi 50% (paranet)
        """)
    
    st.markdown("""
    ### C. Perawatan Bibit (Hari 7-25)
    - [ ] Penyiraman 2x sehari (pagi & sore)
    - [ ] Jaga kelembaban media
    - [ ] Aplikasi pupuk daun (opsional, 1x seminggu)
    - [ ] Monitoring hama/penyakit
    - [ ] Seleksi bibit sehat
    
    ### D. Pengerasan Bibit (Hari 25-30)
    - [ ] Kurangi penyiraman bertahap
    - [ ] Buka naungan bertahap (adaptasi cahaya)
    - [ ] Semprot pupuk daun (booster)
    - [ ] Siap tanam: 4-6 daun sejati, tinggi 10-15 cm
    """)

with tabs[2]:
    st.header("3️⃣ SOP Penanaman (Hari 30)")
    
    st.markdown("""
    ### A. Waktu Tanam
    - [ ] Tanam sore hari (tidak panas)
    - [ ] Hindari hujan deras
    - [ ] Pilih cuaca mendung (ideal)
    
    ### B. Cara Tanam
    - [ ] Siram lubang tanam terlebih dahulu
    - [ ] Keluarkan bibit dari polybag hati-hati
    - [ ] Tanam tegak, jangan terlalu dalam
    - [ ] Padatkan tanah di sekitar bibit
    - [ ] Siram lagi setelah tanam
    
    ### C. Pemasangan Ajir
    - [ ] Pasang ajir bambu (tinggi 1.5-2 m)
    - [ ] Jarak 10-15 cm dari batang
    - [ ] Ikat batang dengan tali rafia (longgar)
    
    ### D. Penyulaman (Hari 37-40)
    - [ ] Cek tanaman yang mati/tidak tumbuh
    - [ ] Ganti dengan bibit cadangan
    - [ ] Pastikan semua lubang terisi
    """)

with tabs[3]:
    st.header("4️⃣ SOP Pemeliharaan (Hari 30-90)")
    
    st.markdown("### A. Penyiraman")
    if "Greenhouse" in scenario:
        st.markdown("""
        - [ ] Gunakan sistem irigasi otomatis/drip
        - [ ] Pagi: 07:00-08:00
        - [ ] Sore: 16:00-17:00 (jika perlu)
        - [ ] Jaga kelembaban 60-70%
        """)
    else:
        st.markdown("""
        - [ ] Pagi: 07:00-08:00
        - [ ] Sore: 16:00-17:00
        - [ ] Kurangi saat hujan
        - [ ] Tambah saat kemarau
        """)
    
    st.markdown("### B. Pemupukan")
    
    if "Organik" in scenario:
        st.markdown("""
        **Jadwal Pemupukan Organik:**
        
        - [ ] **Minggu 1-2:** Pupuk cair organik (POC) 5 ml/L, 1x seminggu
        - [ ] **Minggu 3-4:** POC 10 ml/L + PGPR 5 ml/L
        - [ ] **Minggu 5-6:** Kompos cair + MOL
        - [ ] **Minggu 7-8:** POC tinggi K (fase berbunga)
        - [ ] **Minggu 9-16:** POC + pupuk daun organik
        """)
    elif "Kimia" in scenario:
        st.markdown("""
        **Jadwal Pemupukan Kimia:**
        
        - [ ] **Minggu 1-2:** NPK 16-16-16 (5 g/tanaman)
        - [ ] **Minggu 3-4:** Urea (3 g) + NPK (5 g)
        - [ ] **Minggu 5-6:** NPK + KCl (5 g)
        - [ ] **Minggu 7-8:** KNO3 (5 g) - fase berbunga
        - [ ] **Minggu 9-16:** NPK + Pupuk daun
        """)
    else:
        st.markdown("""
        **Jadwal Pemupukan Campuran:**
        
        - [ ] **Minggu 1-2:** Kompos cair + NPK (3 g)
        - [ ] **Minggu 3-4:** POC + Urea (2 g)
        - [ ] **Minggu 5-6:** NPK + PGPR
        - [ ] **Minggu 7-8:** KNO3 (3 g) + POC
        - [ ] **Minggu 9-16:** Alternatif organik-kimia
        """)
    
    st.markdown("### C. Pengendalian Hama & Penyakit")
    
    if "Organik" in scenario:
        st.markdown("""
        **Preventif:**
        - [ ] Monitoring rutin (setiap hari)
        - [ ] Pasang sticky trap (kuning & biru)
        - [ ] Aplikasi PGPR/Trichoderma 2 minggu sekali
        - [ ] Semprot neem oil 1x seminggu
        
        **Kuratif (jika terserang):**
        - [ ] Beauveria bassiana untuk hama
        - [ ] Trichoderma untuk penyakit jamur
        - [ ] Pseudomonas untuk penyakit bakteri
        - [ ] Cabut tanaman sakit parah
        """)
    else:
        st.markdown("""
        **Preventif:**
        - [ ] Monitoring rutin
        - [ ] Aplikasi fungisida preventif (2 minggu sekali)
        - [ ] Rotasi pestisida (hindari resistensi)
        
        **Kuratif (jika terserang):**
        - [ ] Insektisida sesuai hama target
        - [ ] Fungisida sesuai penyakit
        - [ ] Perhatikan dosis & interval aplikasi
        - [ ] Cabut tanaman sakit parah
        """)
    
    st.markdown("""
    ### D. Pemangkasan & Pewiwilan
    - [ ] Buang tunas air/cabang tidak produktif
    - [ ] Buang daun tua/sakit
    - [ ] Jaga 2-3 cabang utama
    - [ ] Lakukan pagi hari (luka cepat kering)
    """)

with tabs[4]:
    st.header("5️⃣ SOP Panen & Pasca Panen")
    
    st.markdown("""
    ### A. Kriteria Panen
    - [ ] Umur 90-120 hari setelah tanam
    - [ ] Buah berwarna merah penuh (cabai merah)
    - [ ] Ukuran sesuai varietas
    - [ ] Tekstur keras/padat
    
    ### B. Cara Panen
    - [ ] Panen pagi hari (07:00-10:00)
    - [ ] Gunakan gunting/pisau tajam
    - [ ] Sisakan tangkai 1-2 cm
    - [ ] Hindari merusak tanaman
    - [ ] Panen bertahap (7-10 hari sekali)
    
    ### C. Sortasi & Grading
    - [ ] Grade A: Besar, mulus, warna merah penuh
    - [ ] Grade B: Sedang, sedikit cacat
    - [ ] Grade C: Kecil, cacat, untuk olahan
    - [ ] Buang buah busuk/sakit
    
    ### D. Pengemasan
    - [ ] Gunakan keranjang berlubang
    - [ ] Jangan tumpuk terlalu tinggi
    - [ ] Simpan di tempat teduh
    - [ ] Segera jual/olah (cabai mudah rusak)
    """)
    
    if "Organik" in scenario:
        st.success("""
        **💰 Harga Jual Organik:**
        - Grade A: Rp 50,000-80,000/kg
        - Grade B: Rp 40,000-60,000/kg
        - Premium: Rp 60,000-100,000/kg (dengan sertifikat)
        """)

with tabs[5]:
    st.header("📝 Checklist Lengkap")
    
    st.markdown(f"""
    ## Checklist Budidaya Cabai - {scenario}
    
    ### Minggu 0: Persiapan
    - [ ] Olah tanah
    - [ ] Aplikasi pupuk dasar
    - [ ] Pasang mulsa
    - [ ] Semai benih
    
    ### Minggu 1-4: Pembibitan
    - [ ] Perawatan bibit
    - [ ] Penyiraman rutin
    - [ ] Monitoring hama
    - [ ] Pengerasan bibit
    
    ### Minggu 4: Penanaman
    - [ ] Tanam bibit
    - [ ] Pasang ajir
    - [ ] Penyiraman
    - [ ] Penyulaman (minggu 5)
    
    ### Minggu 5-8: Vegetatif
    - [ ] Penyiraman rutin
    - [ ] Pemupukan susulan 1 (minggu 5)
    - [ ] Pemupukan susulan 2 (minggu 7)
    - [ ] Penyiangan gulma
    - [ ] Monitoring hama/penyakit
    
    ### Minggu 9-12: Berbunga
    - [ ] Pemupukan tinggi K
    - [ ] Pengendalian hama intensif (thrips)
    - [ ] Kurangi penyiraman
    - [ ] Pemangkasan tunas air
    
    ### Minggu 13-16: Berbuah & Panen
    - [ ] Pemupukan booster
    - [ ] Panen bertahap
    - [ ] Sortasi & grading
    - [ ] Pengemasan
    - [ ] Pemasaran
    
    ### Pasca Panen
    - [ ] Bersihkan lahan
    - [ ] Cabut sisa tanaman
    - [ ] Rotasi tanaman
    - [ ] Evaluasi hasil
    """)
    
    # Download button
    st.download_button(
        label="📥 Download SOP (Text)",
        data=f"SOP Budidaya Cabai - {scenario}\n\n[Isi SOP lengkap...]",
        file_name=f"SOP_Cabai_{scenario.replace(' ', '_')}.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>📋 SOP Budidaya Cabai</strong></p>
    <p><small>Standard Operating Procedure - Standar Industri</small></p>
</div>
""", unsafe_allow_html=True)
