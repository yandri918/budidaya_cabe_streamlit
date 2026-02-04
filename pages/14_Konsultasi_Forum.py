import streamlit as st
import pandas as pd
from data.qa_database import QA_DATABASE, search_qa, get_all_categories
from data.expert_tips import EXPERT_TIPS, get_all_tips, get_all_stories

st.set_page_config(page_title="Konsultasi & Forum", page_icon="💬", layout="wide")

st.title("💬 Konsultasi & Forum Budidaya Cabai")
st.markdown("**Berbagi pengetahuan dan pengalaman budidaya cabai**")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "❓ Q&A",
    "💡 Tips Ahli",
    "🏆 Success Stories",
    "📝 Konsultasi"
])

# TAB 1: Q&A
with tab1:
    st.header("❓ Tanya Jawab Budidaya Cabai")
    
    # Search and filter
    col_search1, col_search2 = st.columns([2, 1])
    
    with col_search1:
        search_query = st.text_input(
            "🔍 Cari pertanyaan",
            placeholder="Contoh: kutu daun, pupuk, panen...",
            help="Cari berdasarkan kata kunci"
        )
    
    with col_search2:
        categories = ["Semua"] + get_all_categories()
        selected_category = st.selectbox(
            "Kategori",
            categories
        )
    
    # Display Q&A
    if search_query:
        # Search mode
        results = search_qa(search_query, selected_category if selected_category != "Semua" else None)
        
        if results:
            st.success(f"Ditemukan {len(results)} hasil")
            for qa in results:
                with st.expander(f"📌 {qa['question']}", expanded=False):
                    st.write(f"**Kategori:** {qa['category']}")
                    st.write(f"**Jawaban:** {qa['answer']}")
                    if qa.get('related_modules'):
                        st.info(f"**Lihat juga:** {', '.join(qa['related_modules'])}")
                    st.caption(f"Tags: {', '.join(qa['tags'])}")
        else:
            st.warning("Tidak ada hasil. Coba kata kunci lain.")
    else:
        # Category mode
        if selected_category == "Semua":
            for category in get_all_categories():
                st.subheader(f"📂 {category}")
                for qa in QA_DATABASE[category][:3]:  # Show first 3
                    with st.expander(f"📌 {qa['question']}"):
                        st.write(f"**Jawaban:** {qa['answer']}")
                        if qa.get('related_modules'):
                            st.info(f"**Lihat juga:** {', '.join(qa['related_modules'])}")
                st.markdown("---")
        else:
            qa_list = QA_DATABASE.get(selected_category, [])
            if qa_list:
                for qa in qa_list:
                    with st.expander(f"📌 {qa['question']}"):
                        st.write(f"**Jawaban:** {qa['answer']}")
                        if qa.get('related_modules'):
                            st.info(f"**Lihat juga:** {', '.join(qa['related_modules'])}")
                        st.caption(f"Tags: {', '.join(qa['tags'])}")

# TAB 2: Expert Tips
with tab2:
    st.header("💡 Tips dari Ahli")
    
    tip_category = st.selectbox(
        "Pilih Kategori Tips",
        list(EXPERT_TIPS.keys())
    )
    
    tips = EXPERT_TIPS[tip_category]
    
    for tip in tips:
        with st.expander(f"💡 {tip['title']}", expanded=False):
            st.write(tip['content'])
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                difficulty_colors = {
                    'Mudah': '🟢',
                    'Sedang': '🟡',
                    'Sulit': '🔴'
                }
                st.caption(f"{difficulty_colors.get(tip['difficulty'], '⚪')} Tingkat Kesulitan: {tip['difficulty']}")
            
            with col_t2:
                impact_colors = {
                    'Sangat Tinggi': '🔥',
                    'Tinggi': '⭐',
                    'Sedang': '✨'
                }
                st.caption(f"{impact_colors.get(tip['impact'], '💫')} Dampak: {tip['impact']}")

# TAB 3: Success Stories
with tab3:
    st.header("🏆 Kisah Sukses Petani Cabai")
    
    stories = get_all_stories()
    
    for story in stories:
        with st.expander(f"🏆 {story['farmer_name']} - {story['location']}", expanded=True):
            col_s1, col_s2 = st.columns([2, 1])
            
            with col_s1:
                st.markdown(f"**Pencapaian:** {story['achievement']}")
                st.write(story['story'])
                
                st.markdown("**Faktor Kunci Sukses:**")
                for factor in story['key_factors']:
                    st.write(f"✓ {factor}")
                
                st.info(f"**Pelajaran:** {story['lessons']}")
            
            with col_s2:
                st.metric("Luas Lahan", story['land_size'])
                st.metric("Varietas", story['variety'])
                
                st.markdown("**Performa:**")
                st.metric(
                    "Hasil Panen",
                    f"{story['yield_after']} ton/ha",
                    delta=f"+{story['yield_after'] - story['yield_before']} ton/ha"
                )
                st.metric(
                    "Peningkatan Pendapatan",
                    story['revenue_increase']
                )

# TAB 4: Consultation
with tab4:
    st.header("📝 Konsultasi Budidaya")
    
    st.info("""
    **Cara Konsultasi:**
    1. Pilih kategori masalah
    2. Deskripsikan masalah Anda
    3. Sistem akan memberikan rekomendasi berdasarkan database
    4. Lihat modul terkait untuk solusi detail
    """)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        consult_category = st.selectbox(
            "Kategori Masalah",
            get_all_categories()
        )
        
        problem_desc = st.text_area(
            "Deskripsikan Masalah Anda",
            placeholder="Contoh: Daun cabai saya menguning dan rontok...",
            height=150
        )
    
    with col_c2:
        st.markdown("**Upload Foto (Opsional)**")
        uploaded_photo = st.file_uploader(
            "Upload foto tanaman",
            type=['jpg', 'jpeg', 'png'],
            help="Foto membantu identifikasi masalah"
        )
        
        if uploaded_photo:
            st.image(uploaded_photo, caption="Foto yang diupload", use_column_width=True)
    
    if st.button("🔍 Dapatkan Rekomendasi", type="primary"):
        if problem_desc:
            # Search related Q&A
            results = search_qa(problem_desc, consult_category)
            
            st.markdown("---")
            st.subheader("💡 Rekomendasi Berdasarkan Database")
            
            if results:
                st.success(f"Ditemukan {len(results)} solusi terkait:")
                
                for i, qa in enumerate(results[:3], 1):  # Top 3
                    with st.expander(f"Solusi #{i}: {qa['question']}", expanded=i==1):
                        st.write(f"**Jawaban:** {qa['answer']}")
                        
                        if qa.get('related_modules'):
                            st.info(f"**Modul Terkait:** {', '.join(qa['related_modules'])}")
            else:
                st.warning("Tidak ada solusi spesifik ditemukan. Berikut rekomendasi umum:")
                
                # Show general tips for category
                st.markdown(f"**Tips untuk {consult_category}:**")
                qa_list = QA_DATABASE.get(consult_category, [])
                if qa_list:
                    for qa in qa_list[:2]:
                        st.write(f"- {qa['question']}")
                        st.caption(f"  → {qa['answer'][:100]}...")
            
            # Suggest photo analysis if uploaded
            if uploaded_photo:
                st.info("""
                📸 **Analisis Foto:**
                Gunakan **Module 12: Deteksi Penyakit AI** untuk analisis foto otomatis.
                Sistem akan mendeteksi penyakit dan memberikan rekomendasi treatment.
                """)
            
            # Integration suggestions
            st.markdown("---")
            st.subheader("🔗 Modul yang Mungkin Membantu")
            
            col_int1, col_int2, col_int3 = st.columns(3)
            
            with col_int1:
                if consult_category in ["Hama & Penyakit"]:
                    st.info("""
                    **Module 03: Hama & Penyakit**
                    - Database lengkap
                    - Gejala & solusi
                    - Kontrol terpadu
                    """)
            
            with col_int2:
                if consult_category in ["Pemupukan"]:
                    st.info("""
                    **Module 05: Kalkulator Pupuk**
                    - Hitung dosis NPK
                    - Rekomendasi pupuk
                    - Jadwal pemupukan
                    """)
            
            with col_int3:
                st.info("""
                **Module 12: Deteksi Penyakit AI**
                - Upload foto tanaman
                - Analisis otomatis
                - Rekomendasi treatment
                """)
        else:
            st.warning("Silakan deskripsikan masalah Anda terlebih dahulu.")

# Footer
st.markdown("---")
st.info("""
**💬 Tentang Forum:**
- Database Q&A: 22+ pertanyaan umum
- Expert Tips: 11+ tips praktis
- Success Stories: 3+ kisah sukses
- Konsultasi: Rekomendasi otomatis berdasarkan database

**🔗 Integrasi:**
Semua rekomendasi terhubung dengan modul terkait untuk solusi lengkap.
""")
