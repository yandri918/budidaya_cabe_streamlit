"""
Disease Patterns Database
Visual indicators and patterns for rule-based disease detection
"""

# Disease patterns with visual characteristics
DISEASE_PATTERNS = {
    "Sehat": {
        "category": "Healthy",
        "severity": "None",
        "visual_indicators": {
            "leaf_color_hsv": {
                "h_range": (35, 85),  # Green hue
                "s_range": (40, 100),  # Saturation
                "v_range": (40, 100)   # Value/brightness
            },
            "spot_density": (0, 5),  # % of leaf area
            "yellowing": (0, 10),    # % yellow pixels
            "browning": (0, 5)       # % brown pixels
        },
        "health_score_range": (80, 100),
        "treatment": "Pertahankan perawatan rutin",
        "prevention": ["Monitoring rutin", "Nutrisi seimbang", "Sanitasi kebun"]
    },
    
    "Bercak Daun (Cercospora)": {
        "category": "Fungal",
        "severity": "Medium",
        "visual_indicators": {
            "leaf_color_hsv": {
                "h_range": (20, 60),
                "s_range": (30, 90),
                "v_range": (30, 80)
            },
            "spot_density": (10, 40),  # Brown/dark spots
            "yellowing": (15, 40),
            "browning": (10, 30)
        },
        "health_score_range": (40, 70),
        "symptoms": ["Bercak coklat bulat", "Halo kuning", "Daun rontok"],
        "treatment": "Fungisida (Mankozeb, Klorotalonil)",
        "prevention": ["Sanitasi", "Drainase baik", "Rotasi fungisida"]
    },
    
    "Layu Bakteri (Ralstonia)": {
        "category": "Bacterial",
        "severity": "High",
        "visual_indicators": {
            "leaf_color_hsv": {
                "h_range": (15, 50),
                "s_range": (20, 70),
                "v_range": (20, 60)
            },
            "spot_density": (5, 20),
            "yellowing": (30, 60),
            "browning": (20, 50),
            "wilting_score": (40, 80)  # Estimated from color/texture
        },
        "health_score_range": (20, 40),
        "symptoms": ["Layu mendadak", "Batang menghitam", "Akar busuk"],
        "treatment": "Bakterisida (Streptomycin), cabut tanaman sakit",
        "prevention": ["Sanitasi ketat", "Hindari luka", "Rotasi tanaman"]
    },
    
    "Kuning (Defisiensi Nitrogen)": {
        "category": "Nutrient",
        "severity": "Low",
        "visual_indicators": {
            "leaf_color_hsv": {
                "h_range": (20, 45),  # Yellow-green
                "s_range": (20, 60),
                "v_range": (40, 80)
            },
            "spot_density": (0, 10),
            "yellowing": (40, 70),
            "browning": (0, 10)
        },
        "health_score_range": (50, 70),
        "symptoms": ["Daun kuning merata", "Pertumbuhan lambat", "Daun tua menguning"],
        "treatment": "Pupuk nitrogen (Urea, NPK tinggi N)",
        "prevention": ["Pemupukan teratur", "Cek pH tanah", "Mulsa organik"]
    },
    
    "Keriting (Virus/Kutu)": {
        "category": "Viral/Pest",
        "severity": "Medium",
        "visual_indicators": {
            "leaf_color_hsv": {
                "h_range": (25, 70),
                "s_range": (30, 80),
                "v_range": (30, 70)
            },
            "spot_density": (5, 25),
            "yellowing": (20, 50),
            "browning": (5, 20),
            "texture_irregularity": (30, 70)  # Estimated
        },
        "health_score_range": (30, 60),
        "symptoms": ["Daun keriting", "Pertumbuhan terhambat", "Kutu daun"],
        "treatment": "Insektisida (Imidacloprid) + cabut tanaman terinfeksi virus",
        "prevention": ["Kontrol vektor (kutu)", "Sanitasi", "Varietas tahan"]
    },
    
    "Antraknosa": {
        "category": "Fungal",
        "severity": "High",
        "visual_indicators": {
            "leaf_color_hsv": {
                "h_range": (15, 55),
                "s_range": (25, 85),
                "v_range": (25, 75)
            },
            "spot_density": (15, 50),  # Dark spots on fruit/leaf
            "yellowing": (10, 35),
            "browning": (15, 45),
            "black_spots": (10, 40)
        },
        "health_score_range": (25, 50),
        "symptoms": ["Bercak hitam cekung", "Buah busuk", "Daun berlubang"],
        "treatment": "Fungisida sistemik (Azoxystrobin)",
        "prevention": ["Sanitasi buah jatuh", "Drainase", "Hindari luka"]
    }
}

# Health scoring thresholds
HEALTH_THRESHOLDS = {
    "leaf_color_green": {
        "excellent": (70, 100),  # % green pixels
        "good": (50, 69),
        "fair": (30, 49),
        "poor": (10, 29),
        "critical": (0, 9)
    },
    "spot_density": {
        "excellent": (0, 5),
        "good": (6, 15),
        "fair": (16, 30),
        "poor": (31, 50),
        "critical": (51, 100)
    },
    "yellowing": {
        "excellent": (0, 10),
        "good": (11, 25),
        "fair": (26, 40),
        "poor": (41, 60),
        "critical": (61, 100)
    }
}

def get_disease_by_pattern(green_pct, spot_density, yellowing_pct, browning_pct):
    """
    Match visual indicators to disease patterns
    
    Returns:
        list of matched diseases with confidence scores
    """
    matches = []
    
    for disease_name, pattern in DISEASE_PATTERNS.items():
        indicators = pattern['visual_indicators']
        
        # Calculate match score (0-100)
        score = 0
        max_score = 0
        
        # Green color match (inverse for yellowing)
        green_expected = 100 - (indicators.get('yellowing', (0, 0))[0] + indicators.get('yellowing', (0, 0))[1]) / 2
        green_diff = abs(green_pct - green_expected)
        green_score = max(0, 100 - green_diff)
        score += green_score * 0.4
        max_score += 100 * 0.4
        
        # Spot density match
        spot_range = indicators.get('spot_density', (0, 0))
        if spot_range[0] <= spot_density <= spot_range[1]:
            spot_score = 100
        else:
            spot_diff = min(abs(spot_density - spot_range[0]), abs(spot_density - spot_range[1]))
            spot_score = max(0, 100 - spot_diff * 2)
        score += spot_score * 0.3
        max_score += 100 * 0.3
        
        # Yellowing match
        yellow_range = indicators.get('yellowing', (0, 0))
        if yellow_range[0] <= yellowing_pct <= yellow_range[1]:
            yellow_score = 100
        else:
            yellow_diff = min(abs(yellowing_pct - yellow_range[0]), abs(yellowing_pct - yellow_range[1]))
            yellow_score = max(0, 100 - yellow_diff * 2)
        score += yellow_score * 0.3
        max_score += 100 * 0.3
        
        # Normalize score
        confidence = (score / max_score * 100) if max_score > 0 else 0
        
        if confidence > 30:  # Minimum threshold
            matches.append({
                'disease': disease_name,
                'confidence': round(confidence, 1),
                'category': pattern['category'],
                'severity': pattern['severity'],
                'health_score_range': pattern['health_score_range'],
                'treatment': pattern['treatment'],
                'symptoms': pattern.get('symptoms', []),
                'prevention': pattern.get('prevention', [])
            })
    
    # Sort by confidence
    matches.sort(key=lambda x: x['confidence'], reverse=True)
    
    return matches

def calculate_health_score_from_image(green_pct, spot_density, yellowing_pct):
    """Calculate overall health score from image analysis"""
    
    # Weighted scoring
    green_score = 0
    for category, (min_val, max_val) in HEALTH_THRESHOLDS['leaf_color_green'].items():
        if min_val <= green_pct <= max_val:
            if category == 'excellent':
                green_score = 95
            elif category == 'good':
                green_score = 75
            elif category == 'fair':
                green_score = 55
            elif category == 'poor':
                green_score = 35
            else:
                green_score = 15
            break
    
    spot_score = 0
    for category, (min_val, max_val) in HEALTH_THRESHOLDS['spot_density'].items():
        if min_val <= spot_density <= max_val:
            if category == 'excellent':
                spot_score = 95
            elif category == 'good':
                spot_score = 75
            elif category == 'fair':
                spot_score = 55
            elif category == 'poor':
                spot_score = 35
            else:
                spot_score = 15
            break
    
    yellow_score = 0
    for category, (min_val, max_val) in HEALTH_THRESHOLDS['yellowing'].items():
        if min_val <= yellowing_pct <= max_val:
            if category == 'excellent':
                yellow_score = 95
            elif category == 'good':
                yellow_score = 75
            elif category == 'fair':
                yellow_score = 55
            elif category == 'poor':
                yellow_score = 35
            else:
                yellow_score = 15
            break
    
    # Weighted average
    health_score = (green_score * 0.5 + spot_score * 0.3 + yellow_score * 0.2)
    
    return round(health_score, 1)
