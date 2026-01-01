"""
💡 Tips, Trik & Data Statistik
Best practices dan market insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Tips & Data Cabai",
    page_icon="💡",
    layout="wide"
)

# Header
st.title("💡 Tips, Trik & Data Statistik")
st.markdown("**Best practices, troubleshooting & market insights**")

st.markdown("---")

# Tabs
tabs = st.tabs(["💡 Tips & Trik", "❓ FAQ", "📈 Data Pasar", "🔧 Troubleshooting"])

with tabs[0]:
    st.header("💡 Tips & Trik Sukses")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ 10 Tips Sukses Budidaya Cabai:**
        
        1. **Pilih Varietas Tepat**
           - Sesuaikan dengan tujuan & kondisi
           - Jangan asal ikut tetangga
        
        2. **Bibit Berkualitas**
           - 50% kesuksesan ada di bibit
           - Beli dari sumber terpercaya
        
        3. **Mulsa Wajib**
           - Jaga kelembaban tanah
           - Cegah gulma & penyakit
        
        4. **Pemupukan Berimbang**
           - Jangan hanya N tinggi
           - Sesuaikan dengan fase
        
        5. **Monitoring Rutin**
           - Cek tanaman setiap hari
           - Deteksi dini hama/penyakit
        
        6. **Drainase Sempurna**
           - Cabai tidak suka tergenang
           - Buat saluran air bagus
        
        7. **Panen Tepat Waktu**
           - Jangan terlalu muda/tua
           - Perhatikan harga pasar
        
        8. **Sortasi & Grading**
           - Pisahkan grade A, B, C
           - Harga beda signifikan
        
        9. **Diversifikasi Pasar**
           - Jangan hanya ke tengkulak
           - Cari pembeli langsung
        
        10. **Catat Semua**
            - Biaya, hasil, harga
            - Evaluasi & perbaikan
        """)
    
    with col2:
        st.error("""
        **❌ 10 Kesalahan yang Harus Dihindari:**
        
        1. **Tanam Terlalu Rapat**
           - Sirkulasi udara buruk
           - Penyakit mudah menyebar
        
        2. **Over-watering**
           - Akar busuk
           - Bunga/buah rontok
        
        3. **Pestisida Berlebihan**
           - Resistensi hama
           - Bunuh musuh alami
        
        4. **Abaikan Sanitasi**
           - Sumber penyakit
           - Hama berkembang biak
        
        5. **Pupuk Tidak Seimbang**
           - Hanya fokus N
           - Abaikan P & K
        
        6. **Tanam Musim Hujan**
           - Penyakit sulit dikontrol
           - Kualitas buah jelek
        
        7. **Tidak Ada Mulsa**
           - Gulma banyak
           - Tanah cepat kering
        
        8. **Panen Sembarangan**
           - Merusak tanaman
           - Buah memar
        
        9. **Jual Cepat**
           - Tidak perhatikan harga
           - Rugi besar
        
        10. **Tidak Belajar**
            - Ulangi kesalahan
            - Tidak ada perbaikan
        """)

with tabs[1]:
    st.header("❓ FAQ - Pertanyaan Sering Ditanyakan")
    
    faqs = [
        {
            "q": "Berapa modal untuk budidaya cabai 1 ha?",
            "a": "Tergantung sistem:\n- Organik Terbuka: Rp 30-50 juta\n- Kimia Terbuka: Rp 20-35 juta\n- Greenhouse: Rp 200-400 juta\n\nLihat RAB Calculator untuk detail."
        },
        {
            "q": "Berapa lama cabai bisa panen?",
            "a": "- Cabai Rawit: 75-90 hari\n- Cabai Merah Besar: 90-120 hari\n- Cabai Hibrida: 80-100 hari\n\nPanen bertahap selama 30-60 hari."
        },
        {
            "q": "Berapa hasil panen cabai per ha?",
            "a": "Tergantung sistem & varietas:\n- Terbuka: 10-18 ton/ha\n- Greenhouse: 30-50 ton/ha\n- Organik: Lebih rendah 20-30%"
        },
        {
            "q": "Kapan waktu tanam terbaik?",
            "a": "- Jawa: April-Mei (musim kemarau)\n- Greenhouse: Sepanjang tahun\n- Hindari: Desember-Februari (puncak hujan)"
        },
        {
            "q": "Hama paling berbahaya untuk cabai?",
            "a": "Top 3:\n1. Trips (vektor virus)\n2. Tungau kuning\n3. Lalat buah\n\nLihat modul Hama & Penyakit untuk detail."
        },
        {
            "q": "Berapa ROI budidaya cabai?",
            "a": "- Kimia Terbuka: 50-100% (10-15 bulan)\n- Organik: 30-70% (18-24 bulan)\n- Greenhouse: 40-80% (15-20 bulan)"
        },
        {
            "q": "Pupuk apa yang paling penting?",
            "a": "Tergantung fase:\n- Vegetatif: N tinggi\n- Berbunga: P tinggi\n- Berbuah: K tinggi\n\nGunakan Kalkulator Pupuk untuk rekomendasi."
        },
        {
            "q": "Organik vs Kimia, mana lebih untung?",
            "a": "Organik:\n+ Harga jual tinggi (+50-100%)\n- Yield lebih rendah (-20-30%)\n- Modal lebih besar\n\nKimia:\n+ Yield tinggi\n+ Modal lebih kecil\n- Harga jual standar"
        }
    ]
    
    for faq in faqs:
        with st.expander(f"**Q: {faq['q']}**"):
            st.markdown(f"**A:** {faq['a']}")

with tabs[2]:
    st.header("📈 Data Pasar Cabai")
    
    st.info("💡 Data ini adalah estimasi. Untuk data real-time, cek BAPANAS atau pasar lokal.")
    
    # Simulated price data
    price_data = {
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
        "Harga (Rp/kg)": [45000, 50000, 55000, 40000, 35000, 30000, 25000, 28000, 32000, 38000, 42000, 48000]
    }
    
    df_price = pd.DataFrame(price_data)
    
    fig_price = px.line(
        df_price,
        x="Bulan",
        y="Harga (Rp/kg)",
        title="Tren Harga Cabai Merah (Estimasi)",
        markers=True
    )
    
    st.plotly_chart(fig_price, use_container_width=True)
    
    st.markdown("""
    **📊 Insights:**
    - Harga tertinggi: Januari-Maret (musim hujan, produksi rendah)
    - Harga terendah: Juni-Juli (panen raya)
    - Strategi: Tanam April-Mei, panen Juli-September (harga mulai naik)
    """)
    
    st.markdown("---")
    
    # Production data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Produksi Nasional", "2.8 juta ton/tahun", help="Data BPS 2023")
    
    with col2:
        st.metric("Konsumsi per Kapita", "2.5 kg/tahun", help="Rata-rata Indonesia")
    
    with col3:
        st.metric("Luas Panen", "140 ribu ha", help="Total nasional")

with tabs[3]:
    st.header("🔧 Troubleshooting")
    
    st.markdown("### Masalah Umum & Solusi")
    
    problems = [
        {
            "masalah": "Daun keriting & menggulung",
            "penyebab": ["Trips", "Tungau", "Virus"],
            "solusi": [
                "Semprot insektisida/akarisida",
                "Pasang sticky trap",
                "Cabut tanaman terinfeksi virus"
            ]
        },
        {
            "masalah": "Bunga rontok",
            "penyebab": ["Suhu terlalu tinggi", "Kekurangan air", "Hama trips"],
            "solusi": [
                "Penyiraman teratur",
                "Naungi jika terlalu panas",
                "Kendalikan trips"
            ]
        },
        {
            "masalah": "Buah busuk",
            "penyebab": ["Antraknosa", "Kelembaban tinggi", "Lalat buah"],
            "solusi": [
                "Aplikasi fungisida",
                "Perbaiki drainase",
                "Pasang perangkap lalat buah"
            ]
        },
        {
            "masalah": "Tanaman layu",
            "penyebab": ["Layu fusarium", "Layu bakteri", "Nematoda"],
            "solusi": [
                "Cabut & musnahkan tanaman sakit",
                "Rotasi tanaman",
                "Solarisasi tanah"
            ]
        },
        {
            "masalah": "Pertumbuhan kerdil",
            "penyebab": ["Virus", "Kekurangan nutrisi", "Nematoda"],
            "solusi": [
                "Kendalikan vektor virus (kutu daun, trips)",
                "Pemupukan berimbang",
                "Aplikasi nematisida"
            ]
        }
    ]
    
    for problem in problems:
        with st.expander(f"**Masalah: {problem['masalah']}**"):
            st.markdown("**Kemungkinan Penyebab:**")
            for cause in problem['penyebab']:
                st.markdown(f"- {cause}")
            
            st.markdown("\n**Solusi:**")
            for solution in problem['solusi']:
                st.success(f"✓ {solution}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>💡 Tips & Data Budidaya Cabai</strong></p>
    <p><small>Knowledge base untuk petani cabai</small></p>
</div>
""", unsafe_allow_html=True)
