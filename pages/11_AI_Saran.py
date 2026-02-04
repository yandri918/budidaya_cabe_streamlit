"""
🤖 AI Saran Terbaik
Rekomendasi cerdas untuk budidaya cabai
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Saran Budidaya Cabai",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 AI Saran Terbaik")
st.markdown("**Rekomendasi cerdas berdasarkan kondisi & tujuan Anda**")

st.markdown("---")

# Input form
st.header("📝 Profil & Kondisi Anda")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌾 Kondisi Lahan")
    
    luas_lahan = st.number_input(
        "Luas Lahan (Ha)",
        min_value=0.1,
        max_value=100.0,
        value=1.0,
        step=0.1
    )
    
    lokasi = st.selectbox(
        "Lokasi",
        ["Jawa", "Sumatera", "Sulawesi", "Kalimantan", "Bali & Nusa Tenggara"]
    )
    
    ketinggian = st.number_input(
        "Ketinggian (mdpl)",
        min_value=0,
        max_value=2000,
        value=500,
        step=50
    )
    
    akses_air = st.selectbox(
        "Akses Air",
        ["Sangat Baik (Irigasi)", "Baik (Sumur)", "Sedang (Tadah Hujan)", "Terbatas"]
    )

with col2:
    st.subheader("💰 Budget & Pengalaman")
    
    budget = st.number_input(
        "Budget Tersedia (Juta Rp)",
        min_value=5,
        max_value=1000,
        value=50,
        step=5
    )
    
    pengalaman = st.selectbox(
        "Pengalaman Budidaya",
        ["Pemula (0-1 tahun)", "Menengah (1-3 tahun)", "Ahli (>3 tahun)"]
    )
    
    tujuan = st.selectbox(
        "Tujuan Utama",
        ["Profit Maksimal", "Belajar/Hobi", "Organik Premium", "Skala Besar"]
    )
    
    waktu_tersedia = st.selectbox(
        "Waktu yang Bisa Dicurahkan",
        ["Full Time", "Part Time (>4 jam/hari)", "Weekend Only"]
    )

if st.button("🤖 Dapatkan Rekomendasi AI", type="primary"):
    st.markdown("---")
    st.header("🎯 Rekomendasi AI untuk Anda")
    
    # AI Logic (Rule-based)
    budget_per_ha = budget / luas_lahan
    
    # Determine best scenario
    if "Organik" in tujuan:
        if budget_per_ha >= 200:
            recommended_scenario = "Organik_Greenhouse"
            confidence = 90
        else:
            recommended_scenario = "Organik_Terbuka"
            confidence = 85
    elif "Profit" in tujuan:
        if budget_per_ha >= 200:
            recommended_scenario = "Kimia_Greenhouse"
            confidence = 95
        elif budget_per_ha >= 30:
            recommended_scenario = "Campuran_Greenhouse"
            confidence = 88
        else:
            recommended_scenario = "Kimia_Terbuka"
            confidence = 82
    else:
        if budget_per_ha >= 100:
            recommended_scenario = "Campuran_Greenhouse"
            confidence = 85
        else:
            recommended_scenario = "Campuran_Terbuka"
            confidence = 80
    
    # Adjust for experience
    if "Pemula" in pengalaman:
        if "Greenhouse" in recommended_scenario:
            st.warning("⚠️ Greenhouse memerlukan keahlian tinggi. Pertimbangkan mulai dari lahan terbuka.")
            confidence -= 10
    
    # Display recommendation
    st.success(f"""
    ## 🎯 Skenario Terbaik: **{recommended_scenario.replace('_', ' + ')}**
    
    **Confidence Score:** {confidence}% ✨
    """)
    
    # Detailed analysis
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.subheader("✅ Kelebihan untuk Anda")
        
        if "Organik" in recommended_scenario:
            st.markdown("""
            - Harga jual tinggi (+50-100%)
            - Sesuai tujuan organik premium
            - Pasar niche dengan margin bagus
            - Ramah lingkungan
            """)
        elif "Kimia" in recommended_scenario:
            st.markdown("""
            - Yield tinggi (maksimal profit)
            - Lebih mudah untuk pemula
            - Biaya lebih rendah
            - ROI cepat
            """)
        else:
            st.markdown("""
            - Balance antara profit & sustainability
            - Fleksibel (organik + kimia darurat)
            - Risiko lebih rendah
            - Cocok untuk belajar
            """)
        
        if "Greenhouse" in recommended_scenario:
            st.markdown("""
            - Kontrol penuh iklim
            - Yield 2-3x lipat
            - Bisa tanam sepanjang tahun
            - Hama/penyakit lebih terkontrol
            """)
    
    with col_a2:
        st.subheader("⚠️ Tantangan & Solusi")
        
        if "Organik" in recommended_scenario:
            st.markdown("""
            **Tantangan:**
            - Modal lebih besar
            - Yield lebih rendah 20-30%
            - Perlu sertifikasi
            
            **Solusi:**
            - Cari pembeli premium dulu
            - Mulai skala kecil
            - Join komunitas organik
            """)
        elif "Kimia" in recommended_scenario:
            st.markdown("""
            **Tantangan:**
            - Harga jual standar
            - Resistensi hama
            - Dampak lingkungan
            
            **Solusi:**
            - Fokus volume
            - Rotasi pestisida
            - Gunakan IPM
            """)
        else:
            st.markdown("""
            **Tantangan:**
            - Perlu 2 sistem (organik + kimia)
            - Manajemen lebih kompleks
            
            **Solusi:**
            - Dokumentasi ketat
            - Pisahkan area jika perlu
            - Prioritas organik, kimia darurat
            """)
        
        if "Greenhouse" in recommended_scenario:
            st.markdown("""
            **Tantangan:**
            - Investasi besar (Rp 200-400 juta/ha)
            - Perlu keahlian teknis
            - Maintenance rutin
            
            **Solusi:**
            - Cari investor/KUR
            - Training intensif
            - Hire teknisi
            """)
    
    st.markdown("---")
    
    # Action plan
    st.subheader("📋 Rencana Aksi Step-by-Step")
    
    st.markdown(f"""
    ### Fase 1: Persiapan (Minggu 1-2)
    
    - [ ] **Budget Check**
      - Total dibutuhkan: Rp {budget_per_ha * luas_lahan:,.0f} juta
      - Budget Anda: Rp {budget:,.0f} juta
      - {"✅ Cukup!" if budget >= budget_per_ha * luas_lahan else "⚠️ Kurang, cari tambahan modal"}
    
    - [ ] **Persiapan Lahan**
      - Ukur lahan: {luas_lahan} Ha
      - Buat bedengan (lihat Kalkulator Teknis)
      - Pasang mulsa
    
    - [ ] **Beli Benih**
      - Varietas: {"Hibrida (Hot Beauty)" if "Profit" in tujuan else "Organik bersertifikat" if "Organik" in tujuan else "Cabai Merah Besar"}
      - Jumlah: ~{int(luas_lahan * 16000)} batang (lihat Kalkulator)
    
    ### Fase 2: Pembibitan (Minggu 3-6)
    
    - [ ] Semai benih
    - [ ] Perawatan bibit
    - [ ] Monitoring harian
    - [ ] Pengerasan bibit
    
    ### Fase 3: Penanaman (Minggu 7)
    
    - [ ] Tanam bibit (umur 30 hari)
    - [ ] Pasang ajir
    - [ ] Penyiraman
    - [ ] Penyulaman
    
    ### Fase 4: Pemeliharaan (Minggu 8-16)
    
    - [ ] Pemupukan rutin (lihat Kalkulator Pupuk)
    - [ ] Monitoring hama/penyakit
    - [ ] Penyiangan
    - [ ] Pemangkasan
    
    ### Fase 5: Panen (Minggu 17-20)
    
    - [ ] Panen bertahap
    - [ ] Sortasi & grading
    - [ ] Jual ke pembeli terbaik
    - [ ] Evaluasi hasil
    """)
    
    st.markdown("---")
    
    # Financial projection
    st.subheader("💰 Proyeksi Finansial")
    
    # Estimate based on scenario
    if "Greenhouse" in recommended_scenario:
        investasi = budget_per_ha * luas_lahan * 1000000
        yield_ton = 40 if "Kimia" in recommended_scenario else 35
        harga_jual = 35000 if "Kimia" in recommended_scenario else 55000
    else:
        investasi = budget_per_ha * luas_lahan * 1000000
        yield_ton = 15 if "Kimia" in recommended_scenario else 12
        harga_jual = 30000 if "Kimia" in recommended_scenario else 50000
    
    pendapatan = yield_ton * luas_lahan * harga_jual * 1000
    profit = pendapatan - investasi
    roi = (profit / investasi) * 100
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        st.metric("Investasi", f"Rp {investasi:,.0f}")
    
    with col_f2:
        st.metric("Pendapatan", f"Rp {pendapatan:,.0f}")
    
    with col_f3:
        st.metric("Profit", f"Rp {profit:,.0f}")
    
    with col_f4:
        st.metric("ROI", f"{roi:.1f}%")
    
    if roi > 50:
        st.success(f"✅ ROI {roi:.1f}% - Sangat Menguntungkan!")
    elif roi > 20:
        st.info(f"✓ ROI {roi:.1f}% - Menguntungkan")
    else:
        st.warning(f"⚠️ ROI {roi:.1f}% - Margin Tipis, pertimbangkan optimasi")
    
    st.markdown("---")
    
    # Risk assessment
    st.subheader("⚠️ Analisis Risiko")
    
    risks = []
    
    if "Pemula" in pengalaman:
        risks.append({
            "Risiko": "Kurang Pengalaman",
            "Level": "Tinggi",
            "Mitigasi": "Training intensif, konsultasi ahli, mulai skala kecil"
        })
    
    if "Terbatas" in akses_air:
        risks.append({
            "Risiko": "Akses Air Terbatas",
            "Level": "Tinggi",
            "Mitigasi": "Buat sumur bor, water harvesting, drip irrigation"
        })
    
    if budget < budget_per_ha * luas_lahan:
        risks.append({
            "Risiko": "Budget Kurang",
            "Level": "Tinggi",
            "Mitigasi": "Cari KUR, investor, atau kurangi skala"
        })
    
    if "Greenhouse" in recommended_scenario and "Pemula" in pengalaman:
        risks.append({
            "Risiko": "Kompleksitas Greenhouse",
            "Level": "Sedang",
            "Mitigasi": "Hire teknisi, training, mulai dari terbuka"
        })
    
    if lokasi == "Sumatera":
        risks.append({
            "Risiko": "Curah Hujan Tinggi",
            "Level": "Sedang",
            "Mitigasi": "Greenhouse wajib, drainase excellent"
        })
    
    if len(risks) > 0:
        df_risks = pd.DataFrame(risks)
        st.dataframe(df_risks, use_container_width=True, hide_index=True)
    else:
        st.success("✅ Risiko minimal - Kondisi Anda sangat mendukung!")
    
    st.markdown("---")
    
    # Success probability
    st.subheader("📊 Probabilitas Sukses")
    
    success_score = 100
    
    # Deduct based on risks
    if "Pemula" in pengalaman:
        success_score -= 15
    if "Terbatas" in akses_air:
        success_score -= 20
    if budget < budget_per_ha * luas_lahan:
        success_score -= 15
    if "Weekend" in waktu_tersedia:
        success_score -= 10
    
    # Add based on advantages
    if "Ahli" in pengalaman:
        success_score += 10
    if "Sangat Baik" in akses_air:
        success_score += 10
    if budget >= budget_per_ha * luas_lahan * 1.5:
        success_score += 10
    
    success_score = max(min(success_score, 100), 30)  # Clamp between 30-100
    
    if success_score >= 80:
        st.success(f"""
        ## 🎉 Probabilitas Sukses: {success_score}%
        
        **SANGAT TINGGI!** Kondisi Anda sangat mendukung. Segera eksekusi!
        """)
    elif success_score >= 60:
        st.info(f"""
        ## ✓ Probabilitas Sukses: {success_score}%
        
        **BAGUS!** Dengan persiapan matang, Anda bisa sukses.
        """)
    else:
        st.warning(f"""
        ## ⚠️ Probabilitas Sukses: {success_score}%
        
        **PERLU PERHATIAN!** Atasi risiko-risiko di atas terlebih dahulu.
        """)
    
    # Next steps
    st.markdown("---")
    st.subheader("🚀 Langkah Selanjutnya")
    
    st.info("""
    1. **Review Rekomendasi** - Baca detail di atas
    2. **Cek RAB Calculator** - Hitung biaya detail
    3. **Lihat SOP** - Pelajari prosedur lengkap
    4. **Konsultasi** - Diskusi dengan ahli/petani sukses
    5. **Mulai Bertahap** - Jangan langsung skala besar
    6. **Monitor & Evaluasi** - Catat semua, perbaiki terus
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>🤖 AI Saran Terbaik</strong></p>
    <p><small>Rekomendasi berbasis aturan cerdas - Konsultasi ahli tetap penting</small></p>
</div>
""", unsafe_allow_html=True)
