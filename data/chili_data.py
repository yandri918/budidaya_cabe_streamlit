"""
Chili Cultivation Data
Extracted from AgriSensa with enhancements for 6 scenarios
"""

# Chili varieties database
CHILI_VARIETIES = {
    "Cabai Rawit": {
        "nama_latin": "Capsicum frutescens",
        "karakteristik": {
            "tinggi": "50-80 cm",
            "umur_panen": "75-90 hari",
            "yield": "5-8 ton/ha",
            "tingkat_pedas": "Sangat Pedas (50,000-100,000 SHU)"
        },
        "cocok_untuk": ["Organik Terbuka", "Kimia Terbuka", "Campuran Terbuka"],
        "harga_benih": 150000,  # per sachet
        "harga_jual": {
            "organik": 60000,
            "kimia": 35000,
            "campuran": 45000
        }
    },
    "Cabai Merah Besar": {
        "nama_latin": "Capsicum annuum",
        "karakteristik": {
            "tinggi": "80-120 cm",
            "umur_panen": "90-120 hari",
            "yield": "15-25 ton/ha (terbuka), 30-50 ton/ha (greenhouse)",
            "tingkat_pedas": "Sedang (2,500-5,000 SHU)"
        },
        "cocok_untuk": ["Semua skenario"],
        "harga_benih": 135000,
        "harga_jual": {
            "organik": 50000,
            "kimia": 25000,
            "campuran": 35000
        }
    },
    "Cabai Keriting": {
        "nama_latin": "Capsicum annuum var. longum",
        "karakteristik": {
            "tinggi": "70-100 cm",
            "umur_panen": "85-110 hari",
            "yield": "12-20 ton/ha (terbuka), 25-40 ton/ha (greenhouse)",
            "tingkat_pedas": "Sedang-Pedas (5,000-15,000 SHU)"
        },
        "cocok_untuk": ["Semua skenario"],
        "harga_benih": 140000,
        "harga_jual": {
            "organik": 55000,
            "kimia": 30000,
            "campuran": 40000
        }
    },
    "Cabai Hibrida (Hot Beauty)": {
        "nama_latin": "Capsicum annuum F1",
        "karakteristik": {
            "tinggi": "100-130 cm",
            "umur_panen": "80-100 hari",
            "yield": "20-30 ton/ha (terbuka), 40-60 ton/ha (greenhouse)",
            "tingkat_pedas": "Sedang (3,000-8,000 SHU)"
        },
        "cocok_untuk": ["Kimia Greenhouse", "Campuran Greenhouse"],
        "harga_benih": 250000,
        "harga_jual": {
            "organik": 60000,
            "kimia": 35000,
            "campuran": 45000
        }
    }
}

# Growth phases for chili
GROWTH_PHASES = {
    "Pembibitan": {
        "hari": "0-30",
        "deskripsi": "Persemaian hingga bibit siap tanam",
        "kegiatan": [
            "Semai benih di tray/polybag",
            "Penyiraman rutin 2x sehari",
            "Pemupukan daun (jika perlu)",
            "Seleksi bibit sehat"
        ]
    },
    "Vegetatif": {
        "hari": "30-60",
        "deskripsi": "Pertumbuhan batang dan daun",
        "kegiatan": [
            "Penanaman di lahan/greenhouse",
            "Pemupukan dasar",
            "Pemasangan mulsa & ajir",
            "Penyiraman teratur",
            "Penyiangan gulma"
        ]
    },
    "Berbunga": {
        "hari": "60-75",
        "deskripsi": "Pembentukan bunga",
        "kegiatan": [
            "Pemupukan susulan (tinggi K)",
            "Pengendalian hama (thrips, kutu daun)",
            "Penyiraman dikurangi",
            "Pemangkasan tunas air"
        ]
    },
    "Berbuah": {
        "hari": "75-120",
        "deskripsi": "Pembentukan dan pematangan buah",
        "kegiatan": [
            "Pemupukan booster (K tinggi)",
            "Pengendalian hama intensif",
            "Panen bertahap (7-10 hari sekali)",
            "Sortasi & grading"
        ]
    }
}

# Climate requirements
CLIMATE_REQUIREMENTS = {
    "suhu_optimal": "20-30°C",
    "suhu_min": "15°C",
    "suhu_max": "35°C",
    "curah_hujan": "600-1200 mm/tahun",
    "kelembaban": "60-80%",
    "ketinggian": "0-1400 mdpl",
    "ph_tanah": "6.0-7.0",
    "cahaya": "Full sun (8-10 jam/hari)"
}

# Soil requirements
SOIL_REQUIREMENTS = {
    "tekstur": "Lempung berpasir (sandy loam)",
    "drainase": "Baik (tidak tergenang)",
    "bahan_organik": "Tinggi (>3%)",
    "npk": {
        "n": "Sedang-Tinggi",
        "p": "Sedang",
        "k": "Tinggi"
    },
    "persiapan": [
        "Bajak dalam 30-40 cm",
        "Buat bedengan tinggi 30-40 cm",
        "Aplikasi pupuk kandang 20-30 ton/ha",
        "Kapur dolomit jika pH <6.0",
        "Istirahatkan 1-2 minggu"
    ]
}

# Planting calendar by region
PLANTING_CALENDAR = {
    "Jawa": {
        "musim_kemarau": {
            "tanam": "April-Mei",
            "panen": "Juli-September",
            "catatan": "Hasil terbaik, harga tinggi"
        },
        "musim_hujan": {
            "tanam": "Oktober-November",
            "panen": "Januari-Maret",
            "catatan": "Risiko penyakit tinggi"
        }
    },
    "Sumatera": {
        "sepanjang_tahun": {
            "tanam": "Sepanjang tahun (greenhouse)",
            "panen": "Kontinyu",
            "catatan": "Perlu greenhouse untuk kontrol curah hujan"
        }
    },
    "Sulawesi": {
        "musim_kemarau": {
            "tanam": "Mei-Juni",
            "panen": "Agustus-Oktober",
            "catatan": "Cocok untuk dataran tinggi"
        }
    }
}
