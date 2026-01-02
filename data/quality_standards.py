"""
Quality Standards Database
Standards for grading, inspection, and quality control
"""

# Quality grading standards
QUALITY_STANDARDS = {
    'Grade A': {
        'name': 'Premium',
        'size_mm': (60, 100),
        'color': 'Merah cerah, seragam',
        'max_defects_pct': 0,
        'min_uniformity_pct': 95,
        'price_premium': 1.3,
        'description': 'Kualitas terbaik untuk pasar premium dan ekspor'
    },
    'Grade B': {
        'name': 'Standar',
        'size_mm': (40, 60),
        'color': 'Merah normal',
        'max_defects_pct': 5,
        'min_uniformity_pct': 85,
        'price_premium': 1.0,
        'description': 'Kualitas standar untuk pasar lokal'
    },
    'Grade C': {
        'name': 'Ekonomis',
        'size_mm': (20, 40),
        'color': 'Merah/hijau campur',
        'max_defects_pct': 15,
        'min_uniformity_pct': 70,
        'price_premium': 0.7,
        'description': 'Kualitas ekonomis untuk industri'
    },
    'Reject': {
        'name': 'Afkir',
        'size_mm': (0, 20),
        'color': 'Busuk/rusak',
        'max_defects_pct': 100,
        'min_uniformity_pct': 0,
        'price_premium': 0.2,
        'description': 'Tidak layak konsumsi segar'
    }
}

# Inspection checklists
INSPECTION_CHECKLISTS = {
    'pre_harvest': {
        'name': 'Inspeksi Pra-Panen',
        'items': [
            {
                'id': 'maturity',
                'item': 'Kematangan buah 80-90%',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'pest_free',
                'item': 'Tidak ada serangan hama aktif',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'disease_free',
                'item': 'Tidak ada penyakit pada buah',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'weather',
                'item': 'Cuaca cerah (tidak hujan)',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'equipment',
                'item': 'Peralatan panen bersih dan siap',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'timing',
                'item': 'Waktu panen optimal (pagi hari)',
                'weight': 10,
                'critical': False
            }
        ]
    },
    'harvest': {
        'name': 'Inspeksi Saat Panen',
        'items': [
            {
                'id': 'timing',
                'item': 'Panen dilakukan pagi hari (06:00-09:00)',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'method',
                'item': 'Buah dipetik dengan tangkai',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'damage',
                'item': 'Tidak ada kerusakan mekanis',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'sorting',
                'item': 'Sortasi langsung di lapangan',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'container',
                'item': 'Wadah panen bersih dan kering',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'handling',
                'item': 'Penanganan hati-hati (tidak dilempar)',
                'weight': 15,
                'critical': True
            }
        ]
    },
    'post_harvest': {
        'name': 'Inspeksi Pasca-Panen',
        'items': [
            {
                'id': 'washing',
                'item': 'Pencucian dengan air bersih',
                'weight': 15,
                'critical': True
            },
            {
                'id': 'drying',
                'item': 'Pengeringan udara (tidak sinar matahari langsung)',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'final_sorting',
                'item': 'Sortasi akhir sesuai standar',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'grading',
                'item': 'Grading sesuai standar kualitas',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'packaging',
                'item': 'Pengemasan higienis',
                'weight': 15,
                'critical': True
            },
            {
                'id': 'storage',
                'item': 'Penyimpanan suhu dan kelembaban tepat',
                'weight': 15,
                'critical': False
            }
        ]
    },
    'packaging': {
        'name': 'Inspeksi Pengemasan',
        'items': [
            {
                'id': 'cleanliness',
                'item': 'Kemasan bersih dan kering',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'labeling',
                'item': 'Label lengkap (nama, tanggal, grade)',
                'weight': 20,
                'critical': True
            },
            {
                'id': 'weight',
                'item': 'Berat sesuai standar',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'uniformity',
                'item': 'Keseragaman produk dalam kemasan',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'sealing',
                'item': 'Kemasan tertutup rapat',
                'weight': 15,
                'critical': False
            },
            {
                'id': 'appearance',
                'item': 'Tampilan kemasan menarik',
                'weight': 15,
                'critical': False
            }
        ]
    }
}

# Certification types
CERTIFICATION_TYPES = {
    'organic': {
        'name': 'Sertifikasi Organik',
        'validity_months': 12,
        'requirements': [
            'Tidak menggunakan pestisida sintetis',
            'Tidak menggunakan pupuk kimia',
            'Periode konversi minimal 2 tahun',
            'Audit tahunan',
            'Dokumentasi lengkap'
        ],
        'benefits': [
            'Harga premium 30-50%',
            'Akses pasar organik',
            'Ekspor ke negara maju'
        ]
    },
    'gap': {
        'name': 'Good Agricultural Practices (GAP)',
        'validity_months': 24,
        'requirements': [
            'Penggunaan pestisida sesuai aturan',
            'Pencatatan aktivitas budidaya',
            'Pengelolaan limbah',
            'Kesehatan dan keselamatan pekerja',
            'Audit berkala'
        ],
        'benefits': [
            'Akses pasar modern (supermarket)',
            'Harga lebih stabil',
            'Kepercayaan pembeli'
        ]
    },
    'haccp': {
        'name': 'HACCP (Hazard Analysis Critical Control Point)',
        'validity_months': 12,
        'requirements': [
            'Identifikasi bahaya',
            'Penetapan titik kontrol kritis',
            'Monitoring berkelanjutan',
            'Dokumentasi lengkap',
            'Pelatihan karyawan'
        ],
        'benefits': [
            'Keamanan pangan terjamin',
            'Akses pasar ekspor',
            'Mengurangi risiko kontaminasi'
        ]
    },
    'halal': {
        'name': 'Sertifikasi Halal',
        'validity_months': 24,
        'requirements': [
            'Bahan dan proses halal',
            'Tidak ada kontaminasi haram',
            'Audit MUI',
            'Pelatihan halal awareness'
        ],
        'benefits': [
            'Akses pasar muslim',
            'Kepercayaan konsumen',
            'Ekspor ke negara muslim'
        ]
    },
    'export': {
        'name': 'Sertifikasi Ekspor',
        'validity_months': 6,
        'requirements': [
            'Memenuhi standar negara tujuan',
            'Karantina tumbuhan',
            'Dokumentasi ekspor',
            'Standar kualitas internasional'
        ],
        'benefits': [
            'Akses pasar internasional',
            'Harga premium',
            'Diversifikasi pasar'
        ]
    }
}

# Lab test types
LAB_TEST_TYPES = {
    'pesticide_residue': {
        'name': 'Residu Pestisida',
        'parameters': [
            'Organophosphate',
            'Carbamate',
            'Pyrethroid',
            'Neonicotinoid'
        ],
        'mrl': 'Maximum Residue Limit (MRL)',
        'frequency': 'Setiap batch ekspor',
        'cost_range': (500000, 2000000)
    },
    'heavy_metals': {
        'name': 'Logam Berat',
        'parameters': [
            'Lead (Pb)',
            'Cadmium (Cd)',
            'Mercury (Hg)',
            'Arsenic (As)'
        ],
        'mrl': 'WHO/FAO Standards',
        'frequency': 'Setiap 3 bulan',
        'cost_range': (300000, 1000000)
    },
    'microbiology': {
        'name': 'Mikrobiologi',
        'parameters': [
            'Total Plate Count',
            'E. coli',
            'Salmonella',
            'Coliform'
        ],
        'mrl': 'SNI Standards',
        'frequency': 'Setiap batch',
        'cost_range': (400000, 1500000)
    },
    'nutrition': {
        'name': 'Analisis Nutrisi',
        'parameters': [
            'Vitamin C',
            'Capsaicin',
            'Moisture content',
            'Protein'
        ],
        'mrl': 'N/A',
        'frequency': 'Opsional',
        'cost_range': (600000, 2000000)
    },
    'aflatoxin': {
        'name': 'Aflatoxin',
        'parameters': [
            'Aflatoxin B1',
            'Total Aflatoxin'
        ],
        'mrl': 'EU Standards',
        'frequency': 'Untuk ekspor',
        'cost_range': (800000, 2500000)
    }
}

# Pass/Fail criteria
PASS_CRITERIA = {
    'inspection_score': 80,  # Minimum 80/100
    'critical_items': 100,   # All critical items must pass
    'pesticide_residue': 'Below MRL',
    'heavy_metals': 'Within limits',
    'microbiology': 'Acceptable'
}
