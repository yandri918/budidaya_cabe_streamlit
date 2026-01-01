import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.disease_detection_service import DiseaseDetectionService
from PIL import Image

st.set_page_config(page_title="Deteksi Penyakit AI", page_icon="📸", layout="wide")

st.title("📸 Deteksi Penyakit dengan AI")
st.markdown("**Upload foto tanaman untuk analisis otomatis**")

st.info("""
**💡 Tips Foto yang Baik:**
- Fokus pada daun yang menunjukkan gejala
- Pencahayaan cukup (tidak terlalu gelap/terang)
- Jarak dekat untuk detail
- Background sederhana
- Format: JPG atau PNG
""")

# File upload
uploaded_file = st.file_uploader(
    "Upload Foto Tanaman",
    type=['jpg', 'jpeg', 'png'],
    help="Pilih foto daun cabai untuk dianalisis"
)

if uploaded_file is not None:
    # Display original image
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.subheader("📷 Foto Original")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
    
    # Analyze button
    if st.button("🔍 Analisis Foto", type="primary"):
        with st.spinner("Menganalisis foto..."):
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                
                # Analyze
                results = DiseaseDetectionService.analyze_image(uploaded_file)
                
                # Display visualization
                with col_img2:
                    st.subheader("🎨 Analisis Visual")
                    st.image(results['visualization'], use_column_width=True)
                    st.caption("Hijau=Sehat, Kuning=Defisiensi, Merah=Bercak")
                
                # Results
                st.markdown("---")
                st.header("📊 Hasil Analisis")
                
                # Health score
                col_score1, col_score2, col_score3 = st.columns(3)
                
                with col_score1:
                    health_score = results['health_score']
                    if health_score >= 80:
                        color = "#2ECC71"
                        status = "Sehat"
                    elif health_score >= 60:
                        color = "#F39C12"
                        status = "Cukup Sehat"
                    else:
                        color = "#E74C3C"
                        status = "Perlu Perhatian"
                    
                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background-color: {color}20; border: 3px solid {color}; border-radius: 10px;'>
                        <h1 style='color: {color}; margin: 0; font-size: 3em;'>{health_score}</h1>
                        <h3 style='color: {color}; margin: 10px 0 0 0;'>{status}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_score2:
                    st.metric(
                        "Warna Daun (Auto-Score)",
                        f"{results['auto_scores']['leaf_color']}/5",
                        help="1=Kuning Kering, 5=Hijau Tua"
                    )
                    
                    st.metric(
                        "Tingkat Serangan",
                        f"{results['auto_scores']['pest_severity']:.1f}%",
                        help="Estimasi dari bercak dan kerusakan"
                    )
                
                with col_score3:
                    st.metric(
                        "Hijau",
                        f"{results['color_analysis']['green_percentage']:.1f}%"
                    )
                    st.metric(
                        "Kuning",
                        f"{results['color_analysis']['yellow_percentage']:.1f}%"
                    )
                    st.metric(
                        "Bercak",
                        f"{results['spot_analysis']['spot_density_percentage']:.1f}%"
                    )
                
                # Disease detection
                st.markdown("---")
                st.subheader("🔬 Penyakit Terdeteksi")
                
                diseases = results['detected_diseases']
                
                if diseases:
                    # Top 3 matches
                    for i, disease in enumerate(diseases[:3], 1):
                        with st.expander(f"#{i} {disease['disease']} - Confidence: {disease['confidence']:.1f}%"):
                            col_d1, col_d2 = st.columns(2)
                            
                            with col_d1:
                                st.write(f"**Kategori:** {disease['category']}")
                                st.write(f"**Tingkat Keparahan:** {disease['severity']}")
                                st.write(f"**Confidence:** {disease['confidence']:.1f}%")
                                
                                if disease.get('symptoms'):
                                    st.write("**Gejala:**")
                                    for symptom in disease['symptoms']:
                                        st.write(f"- {symptom}")
                            
                            with col_d2:
                                st.write(f"**Treatment:** {disease['treatment']}")
                                
                                if disease.get('prevention'):
                                    st.write("**Pencegahan:**")
                                    for prev in disease['prevention']:
                                        st.write(f"- {prev}")
                    
                    # Treatment recommendations
                    st.markdown("---")
                    st.subheader("💊 Rekomendasi Treatment")
                    
                    recommendations = DiseaseDetectionService.get_treatment_recommendations(diseases)
                    
                    st.success(f"**Primary Treatment:** {recommendations['primary_treatment']}")
                    
                    if recommendations['pesticides']:
                        st.write("**Pestisida yang Direkomendasikan:**")
                        for pesticide in recommendations['pesticides']:
                            st.write(f"- {pesticide}")
                        
                        st.info("💡 Lihat detail dosis di tab **Strategi Penyemprotan**")
                    
                    if recommendations['prevention']:
                        st.write("**Pencegahan:**")
                        for prev in recommendations['prevention']:
                            st.write(f"- {prev}")
                
                else:
                    st.success("✅ Tidak ada penyakit terdeteksi. Tanaman terlihat sehat!")
                
                # Integration links
                st.markdown("---")
                st.subheader("🔗 Integrasi dengan Modul Lain")
                
                col_int1, col_int2, col_int3 = st.columns(3)
                
                with col_int1:
                    st.info("""
                    **📈 Pantau Pertumbuhan**
                    - Auto-fill health assessment
                    - Leaf color: {}/5
                    - Pest severity: {:.1f}%
                    """.format(
                        results['auto_scores']['leaf_color'],
                        results['auto_scores']['pest_severity']
                    ))
                
                with col_int2:
                    st.info("""
                    **💦 Strategi Penyemprotan**
                    - Lihat dosis pestisida
                    - Jadwal aplikasi
                    - Rotasi treatment
                    """)
                
                with col_int3:
                    st.info("""
                    **📔 Jurnal Budidaya**
                    - Log hasil deteksi
                    - Track treatment
                    - Monitor progress
                    """)
            
            except Exception as e:
                st.error(f"❌ Error saat analisis: {str(e)}")
                st.info("Pastikan foto jelas dan format benar (JPG/PNG)")

else:
    st.info("👆 Upload foto tanaman untuk memulai analisis")

# Footer
st.markdown("---")
st.info("""
**📸 Cara Menggunakan:**
1. Upload foto daun cabai yang menunjukkan gejala
2. Klik "Analisis Foto"
3. Lihat hasil deteksi dan rekomendasi
4. Gunakan auto-score untuk update health assessment
5. Apply treatment sesuai rekomendasi

**⚠️ Catatan:**
- Deteksi menggunakan rule-based algorithm (color & pattern analysis)
- Akurasi tergantung kualitas foto
- Untuk diagnosis pasti, konsultasi dengan ahli
- Gunakan sebagai panduan awal treatment
""")
