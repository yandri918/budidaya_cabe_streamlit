"""
Pesticide Database for Chili Cultivation
Contains common pesticides, dosages, target pests, and safety information
"""

PESTICIDE_DATABASE = {
    # INSECTICIDES
    "Abamectin": {
        "type": "Insektisida",
        "active_ingredient": "Abamectin 18 g/L",
        "mode_of_action": "Kontak & Sistemik",
        "target_pests": ["Thrips", "Tungau", "Ulat grayak"],
        "dosage_ml_per_liter": 0.5,
        "dosage_range": "0.25-0.5 ml/L",
        "phi_days": 7,
        "price_per_liter": 350000,
        "safety_class": "II (Berbahaya)",
        "application_interval": "7-10 hari",
        "notes": "Efektif untuk tungau dan thrips. Jangan aplikasi saat terik matahari."
    },
    "Imidacloprid": {
        "type": "Insektisida",
        "active_ingredient": "Imidacloprid 200 g/L",
        "mode_of_action": "Sistemik",
        "target_pests": ["Kutu daun", "Thrips", "Lalat putih"],
        "dosage_ml_per_liter": 0.25,
        "dosage_range": "0.2-0.3 ml/L",
        "phi_days": 14,
        "price_per_liter": 280000,
        "safety_class": "II (Berbahaya)",
        "application_interval": "10-14 hari",
        "notes": "Sistemik, diserap akar dan daun. Bagus untuk pencegahan."
    },
    "Profenofos": {
        "type": "Insektisida",
        "active_ingredient": "Profenofos 500 g/L",
        "mode_of_action": "Kontak & Lambung",
        "target_pests": ["Ulat grayak", "Ulat buah", "Penggerek"],
        "dosage_ml_per_liter": 2.0,
        "dosage_range": "1.5-2.0 ml/L",
        "phi_days": 14,
        "price_per_liter": 180000,
        "safety_class": "Ib (Sangat Berbahaya)",
        "application_interval": "7 hari",
        "notes": "Efektif untuk ulat. Gunakan APD lengkap. Rotasi dengan insektisida lain."
    },
    "Deltamethrin": {
        "type": "Insektisida",
        "active_ingredient": "Deltamethrin 25 g/L",
        "mode_of_action": "Kontak",
        "target_pests": ["Kutu daun", "Thrips", "Lalat putih", "Ulat"],
        "dosage_ml_per_liter": 0.5,
        "dosage_range": "0.4-0.6 ml/L",
        "phi_days": 7,
        "price_per_liter": 220000,
        "safety_class": "II (Berbahaya)",
        "application_interval": "7-10 hari",
        "notes": "Spektrum luas. Cepat knockdown. Rotasi untuk hindari resistensi."
    },
    
    # FUNGICIDES
    "Mankozeb": {
        "type": "Fungisida",
        "active_ingredient": "Mankozeb 80%",
        "mode_of_action": "Kontak & Protektan",
        "target_diseases": ["Bercak daun", "Antraknosa", "Busuk buah"],
        "dosage_gram_per_liter": 2.0,
        "dosage_range": "1.5-2.5 g/L",
        "phi_days": 7,
        "price_per_kg": 85000,
        "safety_class": "III (Agak Berbahaya)",
        "application_interval": "7 hari",
        "notes": "Fungisida kontak, aplikasi preventif. Kombinasi dengan fungisida sistemik."
    },
    "Klorotalonil": {
        "type": "Fungisida",
        "active_ingredient": "Klorotalonil 500 g/L",
        "mode_of_action": "Kontak & Protektan",
        "target_diseases": ["Bercak daun", "Antraknosa", "Layu fusarium"],
        "dosage_ml_per_liter": 2.0,
        "dosage_range": "1.5-2.0 ml/L",
        "phi_days": 14,
        "price_per_liter": 120000,
        "safety_class": "II (Berbahaya)",
        "application_interval": "7-10 hari",
        "notes": "Protektan kuat. Aplikasi sebelum hujan. Rotasi dengan sistemik."
    },
    "Azoxystrobin": {
        "type": "Fungisida",
        "active_ingredient": "Azoxystrobin 250 g/L",
        "mode_of_action": "Sistemik & Protektan",
        "target_diseases": ["Antraknosa", "Bercak daun", "Busuk buah"],
        "dosage_ml_per_liter": 0.5,
        "dosage_range": "0.4-0.6 ml/L",
        "phi_days": 7,
        "price_per_liter": 450000,
        "safety_class": "III (Agak Berbahaya)",
        "application_interval": "10-14 hari",
        "notes": "Sistemik, efek kuratif dan preventif. Mahal tapi efektif."
    },
    "Metalaksil + Mankozeb": {
        "type": "Fungisida",
        "active_ingredient": "Metalaksil 8% + Mankozeb 64%",
        "mode_of_action": "Sistemik + Kontak",
        "target_diseases": ["Busuk akar", "Rebah semai", "Bercak daun"],
        "dosage_gram_per_liter": 2.5,
        "dosage_range": "2.0-3.0 g/L",
        "phi_days": 14,
        "price_per_kg": 180000,
        "safety_class": "II (Berbahaya)",
        "application_interval": "10-14 hari",
        "notes": "Kombinasi sistemik & kontak. Bagus untuk penyakit tanah."
    },
    
    # BACTERICIDES
    "Streptomycin": {
        "type": "Bakterisida",
        "active_ingredient": "Streptomycin sulfate 20%",
        "mode_of_action": "Sistemik",
        "target_diseases": ["Layu bakteri", "Bercak bakteri"],
        "dosage_gram_per_liter": 0.5,
        "dosage_range": "0.3-0.5 g/L",
        "phi_days": 7,
        "price_per_kg": 350000,
        "safety_class": "III (Agak Berbahaya)",
        "application_interval": "5-7 hari",
        "notes": "Antibiotik. Gunakan saat gejala awal. Rotasi untuk hindari resistensi."
    },
    
    # ORGANIC ALTERNATIVES
    "Neem Oil": {
        "type": "Insektisida Organik",
        "active_ingredient": "Azadirachtin 3000 ppm",
        "mode_of_action": "Kontak & Antifeedant",
        "target_pests": ["Kutu daun", "Thrips", "Lalat putih", "Tungau"],
        "dosage_ml_per_liter": 5.0,
        "dosage_range": "3-5 ml/L",
        "phi_days": 1,
        "price_per_liter": 85000,
        "safety_class": "IV (Aman)",
        "application_interval": "5-7 hari",
        "notes": "Organik, aman untuk beneficial insects. Aplikasi sore hari."
    },
    "Beauveria bassiana": {
        "type": "Bioinsektisida",
        "active_ingredient": "Beauveria bassiana 10^8 spora/ml",
        "mode_of_action": "Biologis (Jamur Entomopatogen)",
        "target_pests": ["Thrips", "Kutu daun", "Lalat putih", "Ulat"],
        "dosage_ml_per_liter": 2.0,
        "dosage_range": "1.5-2.5 ml/L",
        "phi_days": 0,
        "price_per_liter": 65000,
        "safety_class": "IV (Aman)",
        "application_interval": "7-10 hari",
        "notes": "Biologis, butuh kelembaban tinggi. Aplikasi sore/malam."
    },
    "Bacillus subtilis": {
        "type": "Biofungisida",
        "active_ingredient": "Bacillus subtilis 10^9 cfu/ml",
        "mode_of_action": "Biologis (Antagonis)",
        "target_diseases": ["Bercak daun", "Busuk akar", "Antraknosa"],
        "dosage_ml_per_liter": 2.0,
        "dosage_range": "1.5-2.5 ml/L",
        "phi_days": 0,
        "price_per_liter": 55000,
        "safety_class": "IV (Aman)",
        "application_interval": "7-10 hari",
        "notes": "Biologis, preventif. Kombinasi dengan kompos. Aplikasi rutin."
    }
}

# Spray schedule by growth phase
SPRAY_SCHEDULE = {
    "Persemaian (0-21 HST)": {
        "frequency": "7-10 hari",
        "focus": "Preventif penyakit tanah & rebah semai",
        "recommended": [
            {
                "week": 1,
                "pesticides": ["Metalaksil + Mankozeb", "Bacillus subtilis"],
                "target": "Busuk akar, rebah semai",
                "method": "Kocor/Siram"
            },
            {
                "week": 2,
                "pesticides": ["Mankozeb", "Bacillus subtilis"],
                "target": "Preventif jamur",
                "method": "Semprot halus"
            },
            {
                "week": 3,
                "pesticides": ["Imidacloprid", "Neem Oil"],
                "target": "Preventif hama",
                "method": "Semprot halus"
            }
        ]
    },
    "Vegetatif (22-60 HST)": {
        "frequency": "7 hari",
        "focus": "Pertumbuhan daun, preventif hama & penyakit",
        "recommended": [
            {
                "week": "4-5",
                "pesticides": ["Mankozeb", "Imidacloprid"],
                "target": "Bercak daun, kutu daun",
                "method": "Semprot"
            },
            {
                "week": "6-7",
                "pesticides": ["Klorotalonil", "Abamectin"],
                "target": "Antraknosa, thrips",
                "method": "Semprot"
            },
            {
                "week": "8",
                "pesticides": ["Azoxystrobin", "Beauveria bassiana"],
                "target": "Jamur, hama",
                "method": "Semprot"
            }
        ]
    },
    "Berbunga (61-90 HST)": {
        "frequency": "5-7 hari",
        "focus": "Proteksi bunga, preventif gugur bunga",
        "recommended": [
            {
                "week": "9-10",
                "pesticides": ["Mankozeb", "Deltamethrin"],
                "target": "Bercak daun, thrips",
                "method": "Semprot hati-hati (hindari bunga)"
            },
            {
                "week": "11-12",
                "pesticides": ["Azoxystrobin", "Abamectin"],
                "target": "Jamur, tungau",
                "method": "Semprot"
            },
            {
                "week": "13",
                "pesticides": ["Klorotalonil", "Neem Oil"],
                "target": "Preventif penyakit",
                "method": "Semprot"
            }
        ]
    },
    "Berbuah (91-150 HST)": {
        "frequency": "5-7 hari",
        "focus": "Proteksi buah, perhatikan PHI",
        "recommended": [
            {
                "week": "14-16",
                "pesticides": ["Mankozeb", "Profenofos"],
                "target": "Antraknosa, ulat buah",
                "method": "Semprot"
            },
            {
                "week": "17-19",
                "pesticides": ["Azoxystrobin", "Deltamethrin"],
                "target": "Busuk buah, hama",
                "method": "Semprot"
            },
            {
                "week": "20+ (Panen)",
                "pesticides": ["Neem Oil", "Bacillus subtilis"],
                "target": "Organik, PHI pendek",
                "method": "Semprot",
                "note": "Perhatikan PHI! Gunakan pestisida organik menjelang panen"
            }
        ]
    }
}

# Rotation groups to prevent resistance
ROTATION_GROUPS = {
    "Insektisida": {
        "Grup A": ["Abamectin", "Beauveria bassiana"],
        "Grup B": ["Imidacloprid", "Deltamethrin"],
        "Grup C": ["Profenofos"],
        "Organik": ["Neem Oil"]
    },
    "Fungisida": {
        "Grup A": ["Mankozeb", "Klorotalonil"],
        "Grup B": ["Azoxystrobin", "Metalaksil + Mankozeb"],
        "Organik": ["Bacillus subtilis"]
    }
}

def get_pesticide_info(name):
    """Get detailed info for a pesticide"""
    return PESTICIDE_DATABASE.get(name, None)

def get_schedule_for_phase(phase):
    """Get spray schedule for growth phase"""
    return SPRAY_SCHEDULE.get(phase, None)

def get_rotation_recommendations():
    """Get rotation group recommendations"""
    return ROTATION_GROUPS
