"""
Pest and Disease Database for Chili
Extracted from AgriSensa with enhancements
"""

# Complete pest and disease database for chili
CHILI_PEST_DISEASE_DATABASE = {
    "pests": [
        {
            "id": "thrips",
            "name_id": "Trips",
            "name_en": "Thrips",
            "scientific": "Thrips parvispinus",
            "severity": "high",
            "symptoms": [
                "Daun keriting dan menggulung",
                "Bercak perak pada daun",
                "Bunga rontok",
                "Virus kuning (PYVV)"
            ],
            "damage_stage": ["Vegetatif", "Generatif"],
            "control": {
                "cultural": [
                    "Mulsa plastik perak",
                    "Blue sticky trap",
                    "Sanitasi gulma"
                ],
                "biological": [
                    "Orius spp. (predator)",
                    "Beauveria bassiana"
                ],
                "chemical": [
                    "Abamektin 18 EC (0.5 ml/L)",
                    "Spinosad 25 SC (0.5 ml/L)"
                ]
            },
            "economic_threshold": "10 ekor per bunga",
            "peak_season": "Musim kemarau"
        },
        {
            "id": "aphid",
            "name_id": "Kutu Daun",
            "name_en": "Aphid",
            "scientific": "Aphis gossypii",
            "severity": "medium",
            "symptoms": [
                "Daun keriting",
                "Embun madu",
                "Virus mosaik",
                "Pertumbuhan terhambat"
            ],
            "damage_stage": ["Vegetatif"],
            "control": {
                "cultural": [
                    "Mulsa plastik perak",
                    "Yellow sticky trap",
                    "Tanam refugia"
                ],
                "biological": [
                    "Coccinellidae (kumbang kepik)",
                    "Chrysoperla spp."
                ],
                "chemical": [
                    "Imidakloprid 200 SL (0.5 ml/L)",
                    "Acetamiprid 20 SP (0.2 g/L)"
                ]
            },
            "economic_threshold": "20% tanaman terserang",
            "peak_season": "Awal musim tanam"
        },
        {
            "id": "mite_chili",
            "name_id": "Tungau Kuning",
            "name_en": "Yellow Mite",
            "scientific": "Polyphagotarsonemus latus",
            "severity": "high",
            "symptoms": [
                "Daun muda menggulung ke bawah",
                "Daun kaku dan rapuh",
                "Pertumbuhan terhambat",
                "Bunga rontok"
            ],
            "damage_stage": ["Vegetatif", "Generatif"],
            "control": {
                "cultural": [
                    "Hindari stress air",
                    "Jaga kelembaban",
                    "Sanitasi gulma",
                    "Monitoring rutin"
                ],
                "biological": [
                    "Amblyseius spp. (predator)",
                    "Beauveria bassiana"
                ],
                "chemical": [
                    "Abamektin 18 EC (0.5 ml/L)",
                    "Spiromesifen 24 SC (0.5 ml/L)",
                    "Propargite 73 EC (2 ml/L)"
                ]
            },
            "economic_threshold": "3 tungau per pucuk",
            "peak_season": "Musim kemarau"
        },
        {
            "id": "fruit_fly",
            "name_id": "Lalat Buah",
            "name_en": "Fruit Fly",
            "scientific": "Bactrocera spp.",
            "severity": "high",
            "symptoms": [
                "Buah berlubang kecil",
                "Buah busuk",
                "Larva di dalam buah",
                "Penurunan kualitas 40-60%"
            ],
            "damage_stage": ["Generatif"],
            "control": {
                "cultural": [
                    "Petik buah terserang",
                    "Pasang perangkap metil eugenol",
                    "Bungkus buah",
                    "Sanitasi buah jatuh"
                ],
                "biological": [
                    "Fopius arisanus (parasitoid)",
                    "Beauveria bassiana"
                ],
                "chemical": [
                    "Spinosad 25 SC (0.5 ml/L)",
                    "Malathion 57 EC (2 ml/L)",
                    "Aplikasi spot spray"
                ]
            },
            "economic_threshold": "2% buah terserang",
            "peak_season": "Fase pembuahan"
        },
        {
            "id": "leafhopper",
            "name_id": "Wereng Hijau Cabai",
            "name_en": "Leafhopper",
            "scientific": "Empoasca spp.",
            "severity": "medium",
            "symptoms": [
                "Daun keriting",
                "Tepi daun terbakar (hopperburn)",
                "Pertumbuhan terhambat",
                "Vektor penyakit"
            ],
            "damage_stage": ["Vegetatif"],
            "control": {
                "cultural": [
                    "Mulsa plastik perak",
                    "Yellow sticky trap",
                    "Tanam refugia"
                ],
                "biological": [
                    "Laba-laba",
                    "Beauveria bassiana"
                ],
                "chemical": [
                    "Imidakloprid 200 SL (0.5 ml/L)",
                    "Tiametoksam 25 WG (0.2 g/L)"
                ]
            },
            "economic_threshold": "10 ekor per tanaman",
            "peak_season": "Awal musim tanam"
        }
    ],
    "diseases": [
        {
            "id": "anthracnose",
            "name_id": "Antraknosa",
            "name_en": "Anthracnose",
            "scientific": "Colletotrichum spp.",
            "severity": "high",
            "symptoms": [
                "Bercak cekung pada buah",
                "Buah busuk",
                "Bercak coklat dengan lingkaran",
                "Buah rontok"
            ],
            "damage_stage": ["Generatif"],
            "control": {
                "cultural": [
                    "Panen tepat waktu",
                    "Drainase baik",
                    "Buang buah sakit",
                    "Rotasi tanaman"
                ],
                "biological": [
                    "Trichoderma harzianum",
                    "Bacillus subtilis"
                ],
                "chemical": [
                    "Mankozeb 80 WP (2 g/L)",
                    "Azoksistrobin 25 SC (1 ml/L)",
                    "Propineb 70 WP (2 g/L)"
                ]
            },
            "favorable_conditions": "Kelembaban tinggi, hujan",
            "peak_season": "Musim hujan"
        },
        {
            "id": "fusarium_wilt",
            "name_id": "Layu Fusarium",
            "name_en": "Fusarium Wilt",
            "scientific": "Fusarium oxysporum",
            "severity": "high",
            "symptoms": [
                "Layu satu sisi",
                "Daun kuning dari bawah",
                "Pembuluh coklat",
                "Tanaman mati"
            ],
            "damage_stage": ["Vegetatif", "Generatif"],
            "control": {
                "cultural": [
                    "Gunakan varietas tahan",
                    "Rotasi tanaman",
                    "Solarisasi tanah",
                    "Drainase baik"
                ],
                "biological": [
                    "Trichoderma harzianum",
                    "Pseudomonas fluorescens"
                ],
                "chemical": [
                    "Benomil 50 WP (1 g/L)",
                    "Karbendazim 50 WP (1 g/L)"
                ]
            },
            "favorable_conditions": "Suhu 25-30°C, tanah lembab",
            "peak_season": "Sepanjang tahun"
        },
        {
            "id": "powdery_mildew",
            "name_id": "Embun Tepung",
            "name_en": "Powdery Mildew",
            "scientific": "Leveillula taurica",
            "severity": "medium",
            "symptoms": [
                "Lapisan putih seperti tepung pada daun",
                "Daun menguning",
                "Daun rontok",
                "Penurunan hasil 20-30%"
            ],
            "damage_stage": ["Vegetatif", "Generatif"],
            "control": {
                "cultural": [
                    "Jarak tanam optimal",
                    "Hindari kelembaban berlebihan",
                    "Sanitasi daun sakit",
                    "Pemupukan berimbang"
                ],
                "biological": [
                    "Ampelomyces quisqualis",
                    "Bacillus subtilis"
                ],
                "chemical": [
                    "Sulfur 80 WP (2 g/L)",
                    "Azoksistrobin 25 SC (1 ml/L)",
                    "Difenokonazol 25 EC (1 ml/L)"
                ]
            },
            "favorable_conditions": "Kelembaban sedang, suhu 20-25°C",
            "peak_season": "Musim kemarau"
        },
        {
            "id": "bacterial_spot",
            "name_id": "Bercak Bakteri",
            "name_en": "Bacterial Spot",
            "scientific": "Xanthomonas campestris pv. vesicatoria",
            "severity": "high",
            "symptoms": [
                "Bercak coklat dengan halo kuning",
                "Bercak pada daun dan buah",
                "Daun rontok",
                "Buah cacat"
            ],
            "damage_stage": ["Vegetatif", "Generatif"],
            "control": {
                "cultural": [
                    "Gunakan benih sehat",
                    "Hindari penyiraman overhead",
                    "Sanitasi alat",
                    "Rotasi tanaman"
                ],
                "biological": [
                    "Pseudomonas fluorescens",
                    "Bacillus subtilis"
                ],
                "chemical": [
                    "Bakterisida tembaga (copper oxychloride 50 WP, 2 g/L)",
                    "Streptomisin sulfat (0.5 g/L)"
                ]
            },
            "favorable_conditions": "Hujan, angin, suhu 25-30°C",
            "peak_season": "Musim hujan"
        },
        {
            "id": "virus_cmv",
            "name_id": "Virus Mosaik Mentimun",
            "name_en": "Cucumber Mosaic Virus",
            "scientific": "CMV",
            "severity": "medium",
            "symptoms": [
                "Mosaik kuning pada daun",
                "Daun keriting",
                "Buah cacat",
                "Pertumbuhan kerdil"
            ],
            "damage_stage": ["Vegetatif"],
            "control": {
                "cultural": [
                    "Gunakan varietas tahan",
                    "Cabut tanaman sakit",
                    "Kendalikan kutu daun (vektor)",
                    "Mulsa plastik perak"
                ],
                "biological": [
                    "Tidak ada (virus)",
                    "Fokus pada pengendalian vektor"
                ],
                "chemical": [
                    "Tidak ada (virus)",
                    "Kendalikan kutu daun dengan insektisida"
                ]
            },
            "favorable_conditions": "Populasi kutu daun tinggi",
            "peak_season": "Awal musim tanam"
        },
        {
            "id": "bacterial_wilt",
            "name_id": "Layu Bakteri",
            "name_en": "Bacterial Wilt",
            "scientific": "Ralstonia solanacearum",
            "severity": "high",
            "symptoms": [
                "Layu mendadak",
                "Daun hijau tapi layu",
                "Pembuluh coklat",
                "Lendir bakteri dari batang"
            ],
            "damage_stage": ["Vegetatif", "Generatif"],
            "control": {
                "cultural": [
                    "Rotasi tanaman (bukan Solanaceae)",
                    "Drainase sempurna",
                    "Cabut tanaman sakit",
                    "Solarisasi tanah"
                ],
                "biological": [
                    "Pseudomonas fluorescens",
                    "Bacillus subtilis"
                ],
                "chemical": [
                    "Bakterisida tembaga (2 g/L)",
                    "Streptomisin sulfat (0.5 g/L)"
                ]
            },
            "favorable_conditions": "Suhu tinggi, tanah lembab",
            "peak_season": "Musim hujan"
        }
    ]
}


def get_all_pests():
    """Get all pest entries"""
    return CHILI_PEST_DISEASE_DATABASE["pests"]


def get_all_diseases():
    """Get all disease entries"""
    return CHILI_PEST_DISEASE_DATABASE["diseases"]


def search_by_symptom(query):
    """Search pest/disease by symptom"""
    results = []
    query_lower = query.lower()
    
    # Search in pests
    for pest in CHILI_PEST_DISEASE_DATABASE["pests"]:
        for symptom in pest["symptoms"]:
            if query_lower in symptom.lower():
                results.append(pest)
                break
    
    # Search in diseases
    for disease in CHILI_PEST_DISEASE_DATABASE["diseases"]:
        for symptom in disease["symptoms"]:
            if query_lower in symptom.lower():
                results.append(disease)
                break
    
    return results


def get_by_id(pest_disease_id):
    """Get specific pest/disease by ID"""
    # Search in pests
    for pest in CHILI_PEST_DISEASE_DATABASE["pests"]:
        if pest["id"] == pest_disease_id:
            return pest
    
    # Search in diseases
    for disease in CHILI_PEST_DISEASE_DATABASE["diseases"]:
        if disease["id"] == pest_disease_id:
            return disease
    
    return None
