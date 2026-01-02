"""
Q&A Database for Consultation & Forum
Comprehensive FAQ covering common chili cultivation questions
"""

QA_DATABASE = {
    "Hama & Penyakit": [
        {
            "id": 1,
            "question": "Bagaimana cara mengatasi kutu daun pada tanaman cabai?",
            "answer": "Kutu daun dapat diatasi dengan: 1) Semprot insektisida berbahan aktif Imidacloprid atau Abamectin, 2) Gunakan pestisida organik seperti Neem Oil, 3) Aplikasi setiap 7 hari, 4) Semprot pada pagi/sore hari, 5) Perhatikan PHI sebelum panen.",
            "tags": ["kutu daun", "hama", "insektisida"],
            "related_modules": ["Module 03", "Module 09"]
        },
        {
            "id": 2,
            "question": "Tanaman cabai saya layu mendadak, apa penyebabnya?",
            "answer": "Layu mendadak biasanya disebabkan oleh layu bakteri (Ralstonia). Tindakan: 1) Cabut dan musnahkan tanaman sakit, 2) Aplikasi bakterisida Streptomycin pada tanaman sehat, 3) Perbaiki drainase, 4) Hindari luka pada akar, 5) Rotasi tanaman dengan non-solanaceae.",
            "tags": ["layu", "bakteri", "penyakit"],
            "related_modules": ["Module 03", "Module 12"]
        },
        {
            "id": 3,
            "question": "Daun cabai berbercak coklat, bagaimana mengatasinya?",
            "answer": "Bercak coklat menandakan bercak daun (Cercospora). Solusi: 1) Aplikasi fungisida Mankozeb atau Klorotalonil, 2) Semprot setiap 7-10 hari, 3) Buang daun terserang, 4) Perbaiki sirkulasi udara, 5) Hindari penyiraman dari atas.",
            "tags": ["bercak daun", "fungisida", "penyakit"],
            "related_modules": ["Module 03", "Module 09"]
        },
        {
            "id": 4,
            "question": "Cara mencegah serangan ulat grayak?",
            "answer": "Pencegahan ulat grayak: 1) Monitoring rutin (cek daun malam hari), 2) Pasang perangkap feromon, 3) Aplikasi Bacillus thuringiensis (organik), 4) Semprot insektisida Profenofos jika populasi tinggi, 5) Sanitasi kebun dari gulma.",
            "tags": ["ulat", "hama", "pencegahan"],
            "related_modules": ["Module 03", "Module 09"]
        },
        {
            "id": 5,
            "question": "Bunga cabai rontok, apa penyebabnya?",
            "answer": "Bunga rontok disebabkan: 1) Suhu terlalu tinggi (>35°C), 2) Kekurangan air, 3) Defisiensi Kalsium & Boron, 4) Serangan thrips, 5) Stress tanaman. Solusi: Aplikasi Ca+B, penyiraman teratur, kontrol thrips, naungan jika perlu.",
            "tags": ["bunga rontok", "stress", "nutrisi"],
            "related_modules": ["Module 05", "Module 13"]
        }
    ],
    
    "Pemupukan": [
        {
            "id": 6,
            "question": "Berapa dosis pupuk NPK yang tepat untuk cabai?",
            "answer": "Dosis NPK untuk cabai: 1) Fase vegetatif: NPK 16-16-16 (300kg/ha), 2) Fase berbunga: NPK 15-15-15 (250kg/ha), 3) Fase berbuah: NPK 12-12-17+2MgO (300kg/ha). Aplikasi setiap 2 minggu dengan cara kocor atau tabur.",
            "tags": ["npk", "dosis", "pupuk"],
            "related_modules": ["Module 05"]
        },
        {
            "id": 7,
            "question": "Kapan waktu terbaik untuk pemupukan?",
            "answer": "Waktu pemupukan terbaik: 1) Pagi hari (06:00-08:00) atau sore (16:00-18:00), 2) Saat tanah lembab (setelah penyiraman), 3) Hindari saat hujan deras, 4) Pupuk daun: pagi/sore saat stomata terbuka, 5) Interval 10-14 hari.",
            "tags": ["waktu", "pemupukan", "jadwal"],
            "related_modules": ["Module 05", "Module 06"]
        },
        {
            "id": 8,
            "question": "Daun cabai menguning, kekurangan nutrisi apa?",
            "answer": "Daun kuning menandakan defisiensi Nitrogen. Tindakan: 1) Aplikasi pupuk Urea (100kg/ha) atau NPK tinggi N, 2) Semprot pupuk daun NPK, 3) Tambahkan pupuk organik (kompos), 4) Cek pH tanah (optimal 6-7), 5) Perbaiki drainase.",
            "tags": ["kuning", "nitrogen", "defisiensi"],
            "related_modules": ["Module 05", "Module 12"]
        },
        {
            "id": 9,
            "question": "Apakah pupuk organik lebih baik dari kimia?",
            "answer": "Keduanya penting dan saling melengkapi: 1) Pupuk organik: memperbaiki struktur tanah, retensi air, mikroba, 2) Pupuk kimia: nutrisi cepat tersedia, dosis terukur. Kombinasi terbaik: pupuk dasar organik + pupuk susulan kimia.",
            "tags": ["organik", "kimia", "perbandingan"],
            "related_modules": ["Module 05"]
        },
        {
            "id": 10,
            "question": "Berapa dosis pupuk kandang untuk cabai?",
            "answer": "Dosis pupuk kandang: 1) 10-20 ton/ha (tergantung kualitas), 2) Aplikasi 2-3 minggu sebelum tanam, 3) Campur dengan tanah, 4) Pastikan sudah matang/terfermentasi, 5) Kombinasi dengan dolomit untuk pH optimal.",
            "tags": ["kandang", "organik", "dosis"],
            "related_modules": ["Module 05"]
        }
    ],
    
    "Penyiraman": [
        {
            "id": 11,
            "question": "Berapa kali sehari cabai harus disiram?",
            "answer": "Frekuensi penyiraman: 1) Fase bibit: 2x sehari (pagi & sore), 2) Fase vegetatif: 1-2x sehari, 3) Fase berbuah: 1x sehari (pagi), 4) Musim hujan: sesuaikan, 5) Cek kelembaban tanah (jangan terlalu basah/kering).",
            "tags": ["penyiraman", "frekuensi", "jadwal"],
            "related_modules": ["Module 06", "Module 13"]
        },
        {
            "id": 12,
            "question": "Bagaimana cara mengetahui tanaman kekurangan air?",
            "answer": "Tanda kekurangan air: 1) Daun layu (terutama siang hari), 2) Daun mengeriting, 3) Pertumbuhan terhambat, 4) Bunga/buah rontok, 5) Tanah kering hingga kedalaman 5cm. Segera siram jika ada tanda-tanda ini.",
            "tags": ["kekurangan air", "gejala", "monitoring"],
            "related_modules": ["Module 10", "Module 13"]
        },
        {
            "id": 13,
            "question": "Sistem irigasi apa yang terbaik untuk cabai?",
            "answer": "Sistem irigasi terbaik: 1) Drip irrigation (paling efisien), 2) Sprinkler (untuk lahan luas), 3) Kocor manual (lahan kecil), 4) Mulsa untuk retensi air, 5) Drainase baik untuk buang kelebihan air.",
            "tags": ["irigasi", "sistem", "efisiensi"],
            "related_modules": ["Module 01"]
        }
    ],
    
    "Panen & Pasca Panen": [
        {
            "id": 14,
            "question": "Kapan waktu panen cabai yang tepat?",
            "answer": "Waktu panen: 1) Cabai merah: 110-120 HST (warna merah penuh), 2) Cabai hijau: 90-100 HST, 3) Panen pagi hari (06:00-09:00), 4) Interval panen 3-5 hari, 5) Perhatikan PHI pestisida (minimal 7 hari setelah spray).",
            "tags": ["panen", "waktu", "jadwal"],
            "related_modules": ["Module 06", "Module 09"]
        },
        {
            "id": 15,
            "question": "Bagaimana cara menyimpan cabai agar tahan lama?",
            "answer": "Penyimpanan cabai: 1) Sortasi (buang yang rusak), 2) Simpan di tempat sejuk (10-15°C), 3) Kelembaban 85-90%, 4) Hindari sinar matahari langsung, 5) Gunakan kemasan berlubang untuk sirkulasi udara. Tahan 7-14 hari.",
            "tags": ["penyimpanan", "pasca panen", "kualitas"],
            "related_modules": ["Module 07"]
        },
        {
            "id": 16,
            "question": "Cara meningkatkan kualitas cabai untuk ekspor?",
            "answer": "Kualitas ekspor: 1) Pilih varietas unggul, 2) Aplikasi pupuk seimbang, 3) Kontrol hama/penyakit ketat, 4) Panen pada tingkat kematangan optimal, 5) Sortasi ketat (ukuran, warna, bentuk), 6) Pengemasan proper, 7) Sertifikasi GAP.",
            "tags": ["kualitas", "ekspor", "standar"],
            "related_modules": ["Module 07", "Module 08"]
        }
    ],
    
    "Varietas & Penanaman": [
        {
            "id": 17,
            "question": "Varietas cabai apa yang paling menguntungkan?",
            "answer": "Varietas menguntungkan: 1) Cabai rawit: permintaan tinggi, harga stabil, 2) Cabai keriting: pasar luas, 3) Cabai merah besar: harga premium, 4) Pilih sesuai: iklim, pasar, modal. Lihat analisis di Module 08.",
            "tags": ["varietas", "keuntungan", "pemilihan"],
            "related_modules": ["Module 07", "Module 08"]
        },
        {
            "id": 18,
            "question": "Berapa jarak tanam cabai yang ideal?",
            "answer": "Jarak tanam ideal: 1) Sistem tunggal: 60x50cm (33.000 tanaman/ha), 2) Sistem ganda: 60x60x40cm, 3) Tergantung varietas (besar/kecil), 4) Pertimbangkan: sirkulasi udara, cahaya, kemudahan perawatan.",
            "tags": ["jarak tanam", "populasi", "penanaman"],
            "related_modules": ["Module 01", "Module 04"]
        },
        {
            "id": 19,
            "question": "Apakah cabai bisa ditanam secara tumpang sari?",
            "answer": "Ya, tumpang sari cabai bisa dengan: 1) Kobis (jarak 50cm), 2) Bawang daun, 3) Jagung manis (sebagai naungan), 4) Tomat. Manfaat: optimasi lahan, diversifikasi pendapatan, kontrol hama alami. Lihat kalkulator di Module 01.",
            "tags": ["tumpang sari", "intercropping", "optimasi"],
            "related_modules": ["Module 01"]
        }
    ],
    
    "Umum": [
        {
            "id": 20,
            "question": "Berapa modal yang dibutuhkan untuk budidaya cabai 1 hektar?",
            "answer": "Modal 1 ha: Rp 30-50 juta (tergantung sistem). Rincian: bibit (Rp 8-12 juta), pupuk (Rp 10-15 juta), pestisida (Rp 5-8 juta), mulsa (Rp 3-5 juta), tenaga kerja (Rp 5-10 juta). Gunakan RAB Calculator di Module 01 untuk detail.",
            "tags": ["modal", "biaya", "investasi"],
            "related_modules": ["Module 01", "Module 07"]
        },
        {
            "id": 21,
            "question": "Berapa lama masa panen cabai?",
            "answer": "Masa panen cabai: 1) Panen pertama: 90-120 HST, 2) Masa produktif: 2-4 bulan, 3) Total siklus: 5-6 bulan, 4) Panen setiap 3-5 hari, 5) Total panen: 15-25 kali dalam 1 siklus.",
            "tags": ["masa panen", "siklus", "durasi"],
            "related_modules": ["Module 06", "Module 07"]
        },
        {
            "id": 22,
            "question": "Apakah cabai bisa ditanam di pot/polybag?",
            "answer": "Ya, cabai bisa ditanam di pot/polybag: 1) Ukuran minimal: 30cm (diameter & tinggi), 2) Media: tanah + kompos + sekam (1:1:1), 3) Drainase baik (lubang di dasar), 4) Penyiraman lebih sering, 5) Pemupukan rutin. Cocok untuk lahan terbatas.",
            "tags": ["pot", "polybag", "urban farming"],
            "related_modules": ["Module 04"]
        }
    ]
}

def search_qa(query, category=None):
    """Search Q&A by query and optional category"""
    results = []
    query_lower = query.lower()
    
    categories_to_search = [category] if category and category != "Semua" else QA_DATABASE.keys()
    
    for cat in categories_to_search:
        if cat in QA_DATABASE:
            for qa in QA_DATABASE[cat]:
                # Search in question, answer, and tags
                if (query_lower in qa['question'].lower() or
                    query_lower in qa['answer'].lower() or
                    any(query_lower in tag for tag in qa['tags'])):
                    results.append({**qa, 'category': cat})
    
    return results

def get_all_categories():
    """Get all Q&A categories"""
    return list(QA_DATABASE.keys())

def get_qa_by_category(category):
    """Get all Q&A for a specific category"""
    return QA_DATABASE.get(category, [])
