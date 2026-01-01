"""
Activity Templates for Cultivation Journal
Predefined activity types with default values
"""

# Activity categories and templates
ACTIVITY_TEMPLATES = {
    "Penyemprotan": {
        "icon": "💦",
        "color": "#3498DB",
        "default_cost": 150000,
        "fields": ["Pestisida", "Dosis", "Target", "Metode"],
        "description": "Aplikasi pestisida/fungisida",
        "source_module": "Strategi Penyemprotan"
    },
    "Pemupukan": {
        "icon": "🌱",
        "color": "#2ECC71",
        "default_cost": 200000,
        "fields": ["Jenis Pupuk", "Dosis", "Metode"],
        "description": "Aplikasi pupuk organik/kimia",
        "source_module": "Kalkulator Pupuk"
    },
    "Penyiangan": {
        "icon": "🌿",
        "color": "#27AE60",
        "default_cost": 50000,
        "fields": ["Area", "Metode"],
        "description": "Pembersihan gulma",
        "source_module": "SOP"
    },
    "Pemangkasan": {
        "icon": "✂️",
        "color": "#E67E22",
        "default_cost": 75000,
        "fields": ["Jenis", "Jumlah Tanaman"],
        "description": "Pemangkasan tunas/daun",
        "source_module": "SOP"
    },
    "Penyiraman": {
        "icon": "💧",
        "color": "#3498DB",
        "default_cost": 30000,
        "fields": ["Volume", "Durasi"],
        "description": "Irigasi/penyiraman",
        "source_module": "SOP"
    },
    "Panen": {
        "icon": "🌶️",
        "color": "#E74C3C",
        "default_cost": 100000,
        "fields": ["Jumlah (kg)", "Kualitas", "Harga Jual"],
        "description": "Panen cabai",
        "source_module": "Analisis Bisnis"
    },
    "Pengukuran": {
        "icon": "📏",
        "color": "#9B59B6",
        "default_cost": 0,
        "fields": ["Tinggi", "Jumlah Daun", "Kondisi"],
        "description": "Monitoring pertumbuhan",
        "source_module": "Pantau Pertumbuhan"
    },
    "Observasi": {
        "icon": "👁️",
        "color": "#95A5A6",
        "default_cost": 0,
        "fields": ["Hama/Penyakit", "Tingkat Serangan", "Tindakan"],
        "description": "Observasi hama/penyakit",
        "source_module": "Hama & Penyakit"
    },
    "Lain-lain": {
        "icon": "📝",
        "color": "#34495E",
        "default_cost": 0,
        "fields": ["Keterangan"],
        "description": "Aktivitas lainnya",
        "source_module": None
    }
}

# SOP tasks by growth phase (simplified from Module 04)
SOP_TASKS_BY_PHASE = {
    "Persemaian (0-21 HST)": [
        {"task": "Penyemaian benih", "hst": 0, "activity_type": "Lain-lain"},
        {"task": "Penyiraman semai", "hst": "1-21", "activity_type": "Penyiraman"},
        {"task": "Aplikasi fungisida preventif", "hst": "7, 14", "activity_type": "Penyemprotan"},
        {"task": "Pindah ke polybag", "hst": 14, "activity_type": "Lain-lain"},
        {"task": "Aklimatisasi bibit", "hst": "15-21", "activity_type": "Lain-lain"}
    ],
    "Vegetatif (22-60 HST)": [
        {"task": "Tanam di lahan", "hst": 21, "activity_type": "Lain-lain"},
        {"task": "Pemupukan dasar", "hst": 21, "activity_type": "Pemupukan"},
        {"task": "Penyiraman rutin", "hst": "22-60", "activity_type": "Penyiraman"},
        {"task": "Penyiangan gulma", "hst": "30, 40, 50", "activity_type": "Penyiangan"},
        {"task": "Pemupukan susulan 1", "hst": 30, "activity_type": "Pemupukan"},
        {"task": "Penyemprotan preventif", "hst": "30, 37, 44, 51", "activity_type": "Penyemprotan"},
        {"task": "Pemangkasan tunas air", "hst": "40, 50", "activity_type": "Pemangkasan"},
        {"task": "Pemupukan susulan 2", "hst": 45, "activity_type": "Pemupukan"},
        {"task": "Pengukuran pertumbuhan", "hst": "30, 40, 50, 60", "activity_type": "Pengukuran"}
    ],
    "Berbunga (61-90 HST)": [
        {"task": "Aplikasi pupuk berbunga", "hst": 60, "activity_type": "Pemupukan"},
        {"task": "Penyemprotan hama bunga", "hst": "65, 72, 79, 86", "activity_type": "Penyemprotan"},
        {"task": "Aplikasi Ca + B", "hst": "65, 75, 85", "activity_type": "Pemupukan"},
        {"task": "Monitoring bunga", "hst": "65-90", "activity_type": "Observasi"},
        {"task": "Penyiraman teratur", "hst": "61-90", "activity_type": "Penyiraman"}
    ],
    "Berbuah (91-150 HST)": [
        {"task": "Pemupukan K tinggi", "hst": "90, 105, 120", "activity_type": "Pemupukan"},
        {"task": "Penyemprotan (perhatikan PHI)", "hst": "95, 102, 109", "activity_type": "Penyemprotan"},
        {"task": "Monitoring ulat buah", "hst": "91-150", "activity_type": "Observasi"},
        {"task": "Panen pertama", "hst": 110, "activity_type": "Panen"},
        {"task": "Panen rutin", "hst": "110-150", "activity_type": "Panen"},
        {"task": "Penyiraman", "hst": "91-150", "activity_type": "Penyiraman"}
    ]
}

def get_activity_template(activity_type):
    """Get template for an activity type"""
    return ACTIVITY_TEMPLATES.get(activity_type, ACTIVITY_TEMPLATES["Lain-lain"])

def get_sop_tasks_for_hst(hst):
    """Get SOP tasks for a specific HST"""
    tasks = []
    
    # Determine phase
    if 0 <= hst <= 21:
        phase = "Persemaian (0-21 HST)"
    elif 22 <= hst <= 60:
        phase = "Vegetatif (22-60 HST)"
    elif 61 <= hst <= 90:
        phase = "Berbunga (61-90 HST)"
    elif 91 <= hst <= 150:
        phase = "Berbuah (91-150 HST)"
    else:
        return []
    
    phase_tasks = SOP_TASKS_BY_PHASE.get(phase, [])
    
    for task_info in phase_tasks:
        task_hst = task_info['hst']
        
        # Check if task applies to current HST
        if isinstance(task_hst, int):
            if task_hst == hst:
                tasks.append(task_info)
        elif isinstance(task_hst, str):
            # Range or multiple values
            if '-' in task_hst:
                # Range
                start, end = map(int, task_hst.split('-'))
                if start <= hst <= end:
                    tasks.append(task_info)
            elif ',' in task_hst:
                # Multiple specific days
                hst_list = [int(x.strip()) for x in task_hst.split(',')]
                if hst in hst_list:
                    tasks.append(task_info)
    
    return tasks

def get_all_sop_tasks():
    """Get all SOP tasks grouped by phase"""
    return SOP_TASKS_BY_PHASE
