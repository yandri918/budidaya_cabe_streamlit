"""
Growth Milestones Database
Expected growth milestones by HST (Hari Setelah Tanam) for chili cultivation
"""

# Growth milestones by HST
GROWTH_MILESTONES = {
    "Persemaian": {
        "hst_range": (0, 21),
        "milestones": [
            {
                "hst": 3,
                "event": "Kecambah muncul",
                "expected_height_cm": 1,
                "expected_leaves": 2,
                "description": "Kotiledon (daun lembaga) muncul",
                "actions": ["Jaga kelembaban", "Hindari sinar matahari langsung"]
            },
            {
                "hst": 7,
                "event": "Daun sejati pertama",
                "expected_height_cm": 3,
                "expected_leaves": 4,
                "description": "Daun sejati mulai tumbuh",
                "actions": ["Mulai penyiraman pagi", "Aplikasi pupuk organik cair"]
            },
            {
                "hst": 14,
                "event": "Siap pindah polybag",
                "expected_height_cm": 8,
                "expected_leaves": 6,
                "description": "Bibit cukup kuat untuk dipindah",
                "actions": ["Pindah ke polybag", "Aklimatisasi bertahap"]
            },
            {
                "hst": 21,
                "event": "Siap tanam",
                "expected_height_cm": 15,
                "expected_leaves": 8,
                "description": "Bibit siap pindah ke lahan",
                "actions": ["Tanam di lahan", "Aplikasi pupuk dasar"]
            }
        ]
    },
    "Vegetatif": {
        "hst_range": (22, 60),
        "milestones": [
            {
                "hst": 30,
                "event": "Pertumbuhan vegetatif aktif",
                "expected_height_cm": 25,
                "expected_leaves": 15,
                "description": "Pertumbuhan daun dan batang cepat",
                "actions": ["Pemupukan NPK", "Penyiangan gulma", "Mulai penyemprotan preventif"]
            },
            {
                "hst": 40,
                "event": "Cabang mulai tumbuh",
                "expected_height_cm": 40,
                "expected_leaves": 25,
                "description": "Percabangan primer muncul",
                "actions": ["Pemangkasan tunas air", "Pemupukan lanjutan"]
            },
            {
                "hst": 50,
                "event": "Persiapan berbunga",
                "expected_height_cm": 55,
                "expected_leaves": 35,
                "description": "Tanaman siap memasuki fase generatif",
                "actions": ["Kurangi N, tingkatkan P & K", "Monitoring hama intensif"]
            },
            {
                "hst": 60,
                "event": "Akhir vegetatif",
                "expected_height_cm": 65,
                "expected_leaves": 45,
                "description": "Siap berbunga",
                "actions": ["Aplikasi pupuk berbunga", "Pastikan drainase baik"]
            }
        ]
    },
    "Berbunga": {
        "hst_range": (61, 90),
        "milestones": [
            {
                "hst": 65,
                "event": "Bunga pertama muncul",
                "expected_height_cm": 70,
                "expected_leaves": 50,
                "description": "Bunga pertama mekar",
                "actions": ["Hindari stress air", "Aplikasi kalsium boron"]
            },
            {
                "hst": 75,
                "event": "Pembungaan massal",
                "expected_height_cm": 75,
                "expected_leaves": 60,
                "description": "Banyak bunga mekar",
                "actions": ["Jaga kelembaban", "Monitoring thrips & kutu"]
            },
            {
                "hst": 85,
                "event": "Fruit set",
                "expected_height_cm": 80,
                "expected_leaves": 70,
                "description": "Bunga mulai jadi buah",
                "actions": ["Aplikasi Ca & B", "Hindari pemangkasan"]
            },
            {
                "hst": 90,
                "event": "Buah muda terbentuk",
                "expected_height_cm": 85,
                "expected_leaves": 75,
                "description": "Buah hijau mulai membesar",
                "actions": ["Pemupukan K tinggi", "Monitoring ulat buah"]
            }
        ]
    },
    "Berbuah": {
        "hst_range": (91, 150),
        "milestones": [
            {
                "hst": 100,
                "event": "Buah membesar",
                "expected_height_cm": 90,
                "expected_leaves": 80,
                "description": "Buah hijau membesar",
                "actions": ["Pemupukan K", "Penyiraman teratur"]
            },
            {
                "hst": 110,
                "event": "Panen pertama",
                "expected_height_cm": 95,
                "expected_leaves": 85,
                "description": "Buah mulai merah, siap panen",
                "actions": ["Panen selektif", "Perhatikan PHI pestisida"]
            },
            {
                "hst": 120,
                "event": "Panen rutin",
                "expected_height_cm": 100,
                "expected_leaves": 90,
                "description": "Panen setiap 3-5 hari",
                "actions": ["Panen teratur", "Pemupukan maintenance"]
            },
            {
                "hst": 150,
                "event": "Akhir produksi",
                "expected_height_cm": 105,
                "expected_leaves": 95,
                "description": "Produktivitas menurun",
                "actions": ["Evaluasi replanting", "Persiapan lahan baru"]
            }
        ]
    }
}

# Health scoring criteria
HEALTH_CRITERIA = {
    "Sangat Sehat": {
        "score_range": (90, 100),
        "indicators": [
            "Daun hijau tua mengkilap",
            "Batang kokoh tegak",
            "Tidak ada hama/penyakit",
            "Pertumbuhan sesuai milestone",
            "Bunga/buah normal"
        ],
        "color": "#2ECC71"
    },
    "Sehat": {
        "score_range": (70, 89),
        "indicators": [
            "Daun hijau normal",
            "Batang cukup kuat",
            "Hama/penyakit minimal (<5%)",
            "Pertumbuhan sedikit lambat",
            "Produksi baik"
        ],
        "color": "#27AE60"
    },
    "Cukup Sehat": {
        "score_range": (50, 69),
        "indicators": [
            "Daun hijau pucat",
            "Batang agak lemah",
            "Hama/penyakit sedang (5-15%)",
            "Pertumbuhan lambat",
            "Produksi menurun"
        ],
        "color": "#F39C12"
    },
    "Kurang Sehat": {
        "score_range": (30, 49),
        "indicators": [
            "Daun kuning/layu",
            "Batang lemah",
            "Hama/penyakit berat (15-30%)",
            "Pertumbuhan terhambat",
            "Produksi rendah"
        ],
        "color": "#E67E22"
    },
    "Tidak Sehat": {
        "score_range": (0, 29),
        "indicators": [
            "Daun kuning/kering",
            "Batang sangat lemah/rebah",
            "Hama/penyakit sangat berat (>30%)",
            "Pertumbuhan terhenti",
            "Tidak produktif"
        ],
        "color": "#E74C3C"
    }
}

def get_milestone_for_hst(hst):
    """Get expected milestone for given HST"""
    for phase, data in GROWTH_MILESTONES.items():
        hst_min, hst_max = data['hst_range']
        if hst_min <= hst <= hst_max:
            # Find closest milestone
            milestones = data['milestones']
            closest = min(milestones, key=lambda x: abs(x['hst'] - hst))
            return {
                'phase': phase,
                'milestone': closest
            }
    return None

def get_phase_for_hst(hst):
    """Get growth phase for given HST"""
    for phase, data in GROWTH_MILESTONES.items():
        hst_min, hst_max = data['hst_range']
        if hst_min <= hst <= hst_max:
            return phase
    return "Unknown"

def calculate_health_score(leaf_color, stem_strength, pest_severity, growth_rate):
    """
    Calculate health score based on observations
    
    Args:
        leaf_color: 1-5 (1=kuning kering, 5=hijau tua)
        stem_strength: 1-5 (1=sangat lemah, 5=sangat kuat)
        pest_severity: 0-100 (% tanaman terserang)
        growth_rate: 1-5 (1=terhenti, 5=sangat cepat)
    
    Returns:
        score (0-100) and category
    """
    # Weighted scoring
    leaf_score = leaf_color * 20  # Max 100
    stem_score = stem_strength * 20  # Max 100
    pest_score = max(0, 100 - pest_severity)  # Inverse
    growth_score = growth_rate * 20  # Max 100
    
    # Weighted average
    total_score = (
        leaf_score * 0.3 +
        stem_score * 0.25 +
        pest_score * 0.25 +
        growth_score * 0.2
    )
    
    # Determine category
    for category, data in HEALTH_CRITERIA.items():
        min_score, max_score = data['score_range']
        if min_score <= total_score <= max_score:
            return {
                'score': round(total_score, 1),
                'category': category,
                'color': data['color'],
                'indicators': data['indicators']
            }
    
    return {
        'score': round(total_score, 1),
        'category': 'Unknown',
        'color': '#95A5A6',
        'indicators': []
    }
