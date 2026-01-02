"""
Expert Tips Database
Practical farming tips and best practices
"""

EXPERT_TIPS = {
    "Tips Harian": [
        {
            "id": 1,
            "title": "Waktu Terbaik untuk Penyiraman",
            "content": "Siram tanaman cabai pada pagi hari (06:00-08:00) atau sore hari (16:00-18:00). Hindari penyiraman siang hari karena air cepat menguap dan dapat membakar daun. Penyiraman pagi lebih baik karena tanaman punya waktu untuk menyerap air sebelum siang.",
            "difficulty": "Mudah",
            "impact": "Tinggi"
        },
        {
            "id": 2,
            "title": "Monitoring Hama Setiap Hari",
            "content": "Luangkan 15-30 menit setiap hari untuk cek tanaman. Fokus pada: bagian bawah daun (kutu, thrips), batang (ulat), dan bunga/buah. Deteksi dini = pengendalian lebih mudah dan murah. Gunakan senter untuk cek malam hari (ulat grayak aktif malam).",
            "difficulty": "Mudah",
            "impact": "Sangat Tinggi"
        },
        {
            "id": 3,
            "title": "Catat Semua Aktivitas",
            "content": "Buat jurnal budidaya harian. Catat: tanggal tanam, pemupukan, penyemprotan, penyiraman, panen, biaya, dan hasil. Data ini sangat berharga untuk evaluasi dan perencanaan musim berikutnya. Gunakan Module 11 untuk pencatatan digital.",
            "difficulty": "Mudah",
            "impact": "Tinggi"
        }
    ],
    
    "Tips Musiman": [
        {
            "id": 4,
            "title": "Strategi Musim Hujan",
            "content": "Saat musim hujan: 1) Pastikan drainase sempurna, 2) Kurangi frekuensi penyiraman, 3) Tingkatkan aplikasi fungisida (interval 5-7 hari), 4) Buat parit keliling bedengan, 5) Naungan plastik jika hujan ekstrem. Cek prakiraan cuaca di Module 13.",
            "difficulty": "Sedang",
            "impact": "Sangat Tinggi"
        },
        {
            "id": 5,
            "title": "Optimasi Musim Kemarau",
            "content": "Musim kemarau: 1) Mulsa tebal (jerami/plastik) untuk retensi air, 2) Penyiraman lebih sering (2x sehari jika perlu), 3) Naungan 30% saat panas ekstrem, 4) Aplikasi pupuk daun lebih sering, 5) Monitoring stress tanaman (daun layu).",
            "difficulty": "Sedang",
            "impact": "Tinggi"
        }
    ],
    
    "Problem Solving": [
        {
            "id": 6,
            "title": "Mengatasi Bunga Rontok",
            "content": "Bunga rontok? Cek: 1) Suhu (ideal 20-30°C), 2) Kelembaban tanah (jangan kering), 3) Aplikasi Ca+B (20ml/tangki), 4) Kontrol thrips, 5) Hindari pemupukan N berlebih saat berbunga. Aplikasi ZPT (Auxin) dapat membantu.",
            "difficulty": "Sedang",
            "impact": "Tinggi"
        },
        {
            "id": 7,
            "title": "Tanaman Kerdil dan Lambat Tumbuh",
            "content": "Pertumbuhan lambat? Penyebab: 1) Defisiensi N (daun kuning), 2) pH tanah tidak optimal (cek, sesuaikan dengan dolomit), 3) Nematoda akar (cek akar), 4) Tanah padat (aerasi buruk), 5) Kekurangan air. Identifikasi penyebab spesifik sebelum treatment.",
            "difficulty": "Sulit",
            "impact": "Tinggi"
        },
        {
            "id": 8,
            "title": "Hasil Panen Rendah",
            "content": "Panen rendah? Evaluasi: 1) Varietas (pilih yang sesuai iklim), 2) Pemupukan (cek dosis dan timing), 3) Kontrol hama/penyakit (losses bisa 30-50%), 4) Penyiraman (stress air = buah kecil), 5) Jarak tanam (terlalu rapat = kompetisi). Gunakan Module 07 untuk analisis.",
            "difficulty": "Sulit",
            "impact": "Sangat Tinggi"
        }
    ],
    
    "Optimasi Hasil": [
        {
            "id": 9,
            "title": "Meningkatkan Kualitas Buah",
            "content": "Kualitas premium: 1) Aplikasi Ca+B rutin (setiap 10 hari), 2) Pemupukan K tinggi saat berbuah, 3) Penyiraman teratur (jangan stress), 4) Panen pada tingkat kematangan optimal, 5) Sortasi ketat. Buah berkualitas = harga 20-30% lebih tinggi.",
            "difficulty": "Sedang",
            "impact": "Sangat Tinggi"
        },
        {
            "id": 10,
            "title": "Memperpanjang Masa Panen",
            "content": "Perpanjang produktivitas: 1) Pemangkasan tunas air rutin, 2) Pemupukan maintenance (NPK seimbang), 3) Kontrol hama/penyakit ketat, 4) Panen teratur (jangan biarkan buah tua di pohon), 5) Rejuvenasi dengan pemangkasan ringan. Bisa panen hingga 6 bulan.",
            "difficulty": "Sedang",
            "impact": "Tinggi"
        },
        {
            "id": 11,
            "title": "Efisiensi Biaya Produksi",
            "content": "Hemat biaya: 1) Buat kompos sendiri (kurangi pupuk kimia 30%), 2) Rotasi pestisida (hindari resistensi), 3) Monitoring ketat (aplikasi hanya saat perlu), 4) Mulsa plastik (hemat air & tenaga penyiangan), 5) Tumpang sari (diversifikasi pendapatan). Target: biaya <50% dari penjualan.",
            "difficulty": "Sedang",
            "impact": "Sangat Tinggi"
        }
    ]
}

SUCCESS_STORIES = [
    {
        "id": 1,
        "farmer_name": "Pak Budi Santoso",
        "location": "Garut, Jawa Barat",
        "land_size": "1 hektar",
        "variety": "Cabai Keriting Hibrida",
        "achievement": "Panen 15 ton/ha (dari sebelumnya 8 ton/ha)",
        "story": "Pak Budi menerapkan sistem budidaya intensif dengan monitoring ketat. Kunci sukses: pemupukan berimbang sesuai fase, kontrol hama preventif dengan rotasi pestisida, dan penyiraman drip irrigation. Investasi awal lebih tinggi, tapi ROI mencapai 180% dalam 1 musim.",
        "key_factors": [
            "Pemupukan sesuai fase pertumbuhan",
            "Monitoring hama setiap hari",
            "Drip irrigation untuk efisiensi air",
            "Rotasi pestisida mencegah resistensi",
            "Pencatatan detail untuk evaluasi"
        ],
        "yield_before": 8,
        "yield_after": 15,
        "revenue_increase": "87%",
        "lessons": "Investasi pada sistem irigasi dan monitoring ketat memberikan hasil signifikan. Pencatatan detail membantu identifikasi masalah lebih cepat."
    },
    {
        "id": 2,
        "farmer_name": "Ibu Siti Aminah",
        "location": "Bandung, Jawa Barat",
        "land_size": "0.5 hektar",
        "variety": "Cabai Rawit",
        "achievement": "Produksi organik dengan harga premium 40% lebih tinggi",
        "story": "Ibu Siti beralih ke budidaya organik setelah mengikuti pelatihan. Menggunakan kompos, pupuk kandang, dan pestisida nabati. Meskipun yield sedikit lebih rendah (10 ton/ha vs 12 ton/ha konvensional), harga jual 40% lebih tinggi membuat keuntungan lebih besar.",
        "key_factors": [
            "Kompos berkualitas dari limbah sendiri",
            "Pestisida nabati (neem oil, bawang putih)",
            "Sertifikasi organik",
            "Pemasaran langsung ke konsumen",
            "Edukasi konsumen tentang produk organik"
        ],
        "yield_before": 12,
        "yield_after": 10,
        "revenue_increase": "16%",
        "lessons": "Organik bukan hanya soal yield, tapi value. Sertifikasi dan pemasaran yang tepat kunci sukses organik."
    },
    {
        "id": 3,
        "farmer_name": "Kelompok Tani Maju Jaya",
        "location": "Malang, Jawa Timur",
        "land_size": "5 hektar (kolektif)",
        "variety": "Cabai Merah Besar",
        "achievement": "Ekspor ke Singapura dengan harga 2x pasar lokal",
        "story": "Kelompok tani ini fokus pada kualitas ekspor. Menerapkan GAP (Good Agricultural Practices), sortasi ketat, dan cold chain. Bermitra dengan eksportir untuk akses pasar internasional. Investasi besar di infrastruktur, tapi harga jual 2x lipat.",
        "key_factors": [
            "Sertifikasi GAP",
            "Sortasi dan grading ketat",
            "Cold storage dan cold chain",
            "Kemitraan dengan eksportir",
            "Konsistensi kualitas dan kuantitas"
        ],
        "yield_before": 10,
        "yield_after": 12,
        "revenue_increase": "140%",
        "lessons": "Pasar ekspor membutuhkan investasi dan komitmen tinggi, tapi memberikan return yang sangat baik. Kolaborasi kelompok tani memudahkan akses modal dan pasar."
    }
]

def get_tips_by_category(category):
    """Get tips by category"""
    return EXPERT_TIPS.get(category, [])

def get_all_tips():
    """Get all tips"""
    all_tips = []
    for category, tips in EXPERT_TIPS.items():
        for tip in tips:
            all_tips.append({**tip, 'category': category})
    return all_tips

def get_all_stories():
    """Get all success stories"""
    return SUCCESS_STORIES
