"""
🐛 Hama & Penyakit Cabai
Database lengkap dengan solusi organik & kimia
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.pest_disease_data import get_all_pests, get_all_diseases, search_by_symptom, get_by_id

st.set_page_config(
    page_title="Hama & Penyakit Cabai",
    page_icon="🐛",
    layout="wide"
)

# Header
st.title("🐛 Hama & Penyakit Cabai")
st.markdown("**Database lengkap dengan solusi organik & kimia**")

st.markdown("---")

# Search
st.subheader("🔍 Cari Berdasarkan Gejala")
search_query = st.text_input(
    "Masukkan gejala yang Anda lihat",
    placeholder="Contoh: daun keriting, buah berlubang, layu"
)

if search_query:
    results = search_by_symptom(search_query)
    if results:
        st.success(f"Ditemukan {len(results)} hasil")
        for item in results:
            with st.expander(f"**{item['name_id']}** ({item['scientific']})", expanded=True):
                severity_color = "🔴" if item['severity'] == 'high' else "🟡"
                st.markdown(f"**Tingkat Keparahan:** {severity_color} {item['severity'].title()}")
                
                st.markdown("**Gejala:**")
                for symptom in item['symptoms']:
                    st.markdown(f"- {symptom}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Pengendalian Kultur Teknis:**")
                    for ctrl in item['control']['cultural']:
                        st.markdown(f"✓ {ctrl}")
                
                with col2:
                    st.markdown("**Pengendalian Hayati/Organik:**")
                    for ctrl in item['control']['biological']:
                        st.markdown(f"🌿 {ctrl}")
                
                with col3:
                    st.markdown("**Pengendalian Kimia:**")
                    for ctrl in item['control']['chemical']:
                        st.markdown(f"💊 {ctrl}")
    else:
        st.warning("Tidak ditemukan hasil. Coba kata kunci lain.")

st.markdown("---")

# Tabs
tabs = st.tabs(["🐜 Hama (5)", "🦠 Penyakit (6)", "📊 Ringkasan"])

with tabs[0]:
    st.header("🐜 Hama Cabai")
    
    pests = get_all_pests()
    
    for pest in pests:
        with st.expander(f"**{pest['name_id']}** - {pest['scientific']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                severity_badge = "🔴 TINGGI" if pest['severity'] == 'high' else "🟡 SEDANG"
                st.markdown(f"**Tingkat Keparahan:** {severity_badge}")
                
                st.markdown("**Gejala Serangan:**")
                for symptom in pest['symptoms']:
                    st.markdown(f"- {symptom}")
                
                st.markdown(f"**Fase Serangan:** {', '.join(pest['damage_stage'])}")
                st.markdown(f"**Ambang Ekonomi:** {pest['economic_threshold']}")
                st.markdown(f"**Puncak Serangan:** {pest['peak_season']}")
            
            with col2:
                st.info(f"""
                **Quick Info:**
                - **Nama Latin:** _{pest['scientific']}_
                - **Nama Inggris:** {pest['name_en']}
                - **Tipe:** Hama
                """)
            
            st.markdown("---")
            
            st.markdown("### 🛡️ Strategi Pengendalian")
            
            col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
            
            with col_ctrl1:
                st.markdown("**1️⃣ Kultur Teknis (Preventif)**")
                for ctrl in pest['control']['cultural']:
                    st.success(f"✓ {ctrl}")
            
            with col_ctrl2:
                st.markdown("**2️⃣ Hayati/Organik**")
                for ctrl in pest['control']['biological']:
                    st.success(f"🌿 {ctrl}")
            
            with col_ctrl3:
                st.markdown("**3️⃣ Kimia (Kuratif)**")
                for ctrl in pest['control']['chemical']:
                    st.warning(f"💊 {ctrl}")

with tabs[1]:
    st.header("🦠 Penyakit Cabai")
    
    diseases = get_all_diseases()
    
    for disease in diseases:
        with st.expander(f"**{disease['name_id']}** - {disease['scientific']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                severity_badge = "🔴 TINGGI" if disease['severity'] == 'high' else "🟡 SEDANG"
                st.markdown(f"**Tingkat Keparahan:** {severity_badge}")
                
                st.markdown("**Gejala Penyakit:**")
                for symptom in disease['symptoms']:
                    st.markdown(f"- {symptom}")
                
                st.markdown(f"**Fase Serangan:** {', '.join(disease['damage_stage'])}")
                st.markdown(f"**Kondisi Menguntungkan:** {disease['favorable_conditions']}")
                st.markdown(f"**Puncak Serangan:** {disease['peak_season']}")
            
            with col2:
                st.info(f"""
                **Quick Info:**
                - **Nama Latin:** _{disease['scientific']}_
                - **Nama Inggris:** {disease['name_en']}
                - **Tipe:** Penyakit
                """)
            
            st.markdown("---")
            
            st.markdown("### 🛡️ Strategi Pengendalian")
            
            col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
            
            with col_ctrl1:
                st.markdown("**1️⃣ Kultur Teknis (Preventif)**")
                for ctrl in disease['control']['cultural']:
                    st.success(f"✓ {ctrl}")
            
            with col_ctrl2:
                st.markdown("**2️⃣ Hayati/Organik**")
                for ctrl in disease['control']['biological']:
                    st.success(f"🌿 {ctrl}")
            
            with col_ctrl3:
                st.markdown("**3️⃣ Kimia (Kuratif)**")
                for ctrl in disease['control']['chemical']:
                    st.warning(f"💊 {ctrl}")

with tabs[2]:
    st.header("📊 Ringkasan Hama & Penyakit")
    
    # Summary table
    summary_data = []
    
    for pest in pests:
        summary_data.append({
            'Jenis': 'Hama',
            'Nama': pest['name_id'],
            'Nama Latin': pest['scientific'],
            'Keparahan': pest['severity'].title(),
            'Fase Serangan': ', '.join(pest['damage_stage']),
            'Puncak': pest['peak_season']
        })
    
    for disease in diseases:
        summary_data.append({
            'Jenis': 'Penyakit',
            'Nama': disease['name_id'],
            'Nama Latin': disease['scientific'],
            'Keparahan': disease['severity'].title(),
            'Fase Serangan': ', '.join(disease['damage_stage']),
            'Puncak': disease['peak_season']
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Hama", len(pests))
    
    with col2:
        st.metric("Total Penyakit", len(diseases))
    
    with col3:
        high_severity = sum(1 for item in pests + diseases if item['severity'] == 'high')
        st.metric("Keparahan Tinggi", high_severity)
    
    with col4:
        st.metric("Total Database", len(pests) + len(diseases))
    
    st.markdown("---")
    
    st.info("""
    **💡 Tips Pengendalian Hama & Penyakit:**
    
    1. **Preventif Lebih Baik** - Kultur teknis adalah kunci
    2. **IPM (Integrated Pest Management)** - Kombinasi organik & kimia
    3. **Monitoring Rutin** - Deteksi dini = pengendalian mudah
    4. **Rotasi Pestisida** - Hindari resistensi
    5. **Sanitasi** - Bersihkan gulma & tanaman sakit
    6. **Gunakan Musuh Alami** - Predator & parasitoid
    7. **Aplikasi Tepat** - Waktu, dosis, cara aplikasi
    8. **Catat Serangan** - Untuk evaluasi & perbaikan
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>🐛 Database Hama & Penyakit Cabai</strong></p>
    <p><small>Data dari AgriSensa | Verified by experts</small></p>
</div>
""", unsafe_allow_html=True)
