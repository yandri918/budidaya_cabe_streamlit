"""
RAB (Rencana Anggaran Biaya) Calculator Service
For 6 Chili Cultivation Scenarios
"""

class RABCalculatorService:
    """Service untuk menghitung RAB budidaya cabai"""
    
    # RAB Templates untuk 6 skenario
    RAB_TEMPLATES = {
        "Organik_Terbuka": {
            "nama": "Organik + Terbuka",
            "deskripsi": "Budidaya organik 100% di lahan terbuka",
            "params": {
                "populasi_ha": 18000,
                "estimasi_yield_min": 8000,  # kg/ha
                "estimasi_yield_max": 12000,
                "harga_jual_min": 40000,  # Rp/kg
                "harga_jual_max": 60000,
                "lama_tanam_bulan": 4
            },
            "items": [
                # Biaya Tetap
                {"kategori": "Biaya Tetap", "item": "Sewa Lahan (per musim)", "satuan": "Ha", "volume": 1, "harga": 5000000, "wajib": True},
                {"kategori": "Biaya Tetap", "item": "Penyusutan Alat", "satuan": "Paket", "volume": 1, "harga": 1000000, "wajib": True},
                
                # Benih
                {"kategori": "Benih", "item": "Benih Organik Bersertifikat", "satuan": "Sachet", "volume": 15, "harga": 200000, "wajib": True},
                
                # Pupuk Organik
                {"kategori": "Pupuk", "item": "Pupuk Kandang Matang", "satuan": "Ton", "volume": 20, "harga": 800000, "wajib": True},
                {"kategori": "Pupuk", "item": "Kompos Premium", "satuan": "Ton", "volume": 10, "harga": 1000000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Hayati (PGPR)", "satuan": "Liter", "volume": 50, "harga": 50000, "wajib": True},
                {"kategori": "Pupuk", "item": "MOL (Mikro Organisme Lokal)", "satuan": "Liter", "volume": 100, "harga": 15000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Cair Organik", "satuan": "Liter", "volume": 200, "harga": 25000, "wajib": True},
                
                # Pestisida Organik
                {"kategori": "Pestisida", "item": "Neem Oil", "satuan": "Liter", "volume": 20, "harga": 80000, "wajib": True},
                {"kategori": "Pestisida", "item": "Trichoderma", "satuan": "Kg", "volume": 10, "harga": 150000, "wajib": True},
                {"kategori": "Pestisida", "item": "Beauveria bassiana", "satuan": "Kg", "volume": 5, "harga": 200000, "wajib": True},
                {"kategori": "Pestisida", "item": "Pestisida Nabati (Bawang-Cabai)", "satuan": "Paket", "volume": 1, "harga": 500000, "wajib": True},
                
                # Penunjang
                {"kategori": "Penunjang", "item": "Mulsa Organik (Jerami)", "satuan": "Ton", "volume": 5, "harga": 300000, "wajib": True},
                {"kategori": "Penunjang", "item": "Ajir Bambu", "satuan": "Batang", "volume": 20000, "harga": 500, "wajib": True},
                {"kategori": "Penunjang", "item": "Tali Gawar", "satuan": "Roll", "volume": 10, "harga": 45000, "wajib": True},
                
                # Tenaga Kerja
                {"kategori": "Tenaga Kerja", "item": "Olah Tanah Manual", "satuan": "HOK", "volume": 80, "harga": 100000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Penanaman", "satuan": "HOK", "volume": 30, "harga": 90000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemeliharaan", "satuan": "HOK", "volume": 100, "harga": 90000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemanenan", "satuan": "HOK", "volume": 120, "harga": 80000, "wajib": True},
                
                # Sertifikasi
                {"kategori": "Sertifikasi", "item": "Biaya Sertifikasi Organik", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
            ],
            "roi_bulan": 20
        },
        
        "Organik_Greenhouse": {
            "nama": "Organik + Greenhouse",
            "deskripsi": "Budidaya organik dalam greenhouse",
            "params": {
                "populasi_ha": 25000,
                "estimasi_yield_min": 25000,
                "estimasi_yield_max": 35000,
                "harga_jual_min": 50000,
                "harga_jual_max": 80000,
                "lama_tanam_bulan": 4
            },
            "items": [
                # Biaya Tetap
                {"kategori": "Biaya Tetap", "item": "Amortisasi Greenhouse", "satuan": "Musim", "volume": 1, "harga": 25000000, "wajib": True},
                {"kategori": "Biaya Tetap", "item": "Sistem Irigasi Otomatis", "satuan": "Paket", "volume": 1, "harga": 10000000, "wajib": True},
                
                # Benih
                {"kategori": "Benih", "item": "Benih Organik Premium", "satuan": "Sachet", "volume": 20, "harga": 250000, "wajib": True},
                
                # Media Tanam
                {"kategori": "Media", "item": "Cocopeat Organik", "satuan": "Kg", "volume": 5000, "harga": 3000, "wajib": True},
                {"kategori": "Media", "item": "Kompos Premium", "satuan": "Ton", "volume": 15, "harga": 1200000, "wajib": True},
                
                # Pupuk Organik
                {"kategori": "Pupuk", "item": "Pupuk Hayati Lengkap", "satuan": "Liter", "volume": 100, "harga": 75000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Cair Organik Premium", "satuan": "Liter", "volume": 300, "harga": 40000, "wajib": True},
                {"kategori": "Pupuk", "item": "Mikroba Pelarut Fosfat", "satuan": "Liter", "volume": 50, "harga": 60000, "wajib": True},
                
                # Pest Control
                {"kategori": "Pestisida", "item": "Paket Biopestisida Lengkap", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True},
                
                # Tenaga Kerja
                {"kategori": "Tenaga Kerja", "item": "Perawatan Greenhouse", "satuan": "HOK", "volume": 150, "harga": 100000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemanenan & Sortir", "satuan": "HOK", "volume": 180, "harga": 90000, "wajib": True},
                
                # Sertifikasi
                {"kategori": "Sertifikasi", "item": "Sertifikasi Organik Premium", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True},
            ],
            "roi_bulan": 25
        },
        
        "Kimia_Terbuka": {
            "nama": "Kimia + Terbuka",
            "deskripsi": "Budidaya konvensional dengan pupuk & pestisida kimia",
            "params": {
                "populasi_ha": 18000,
                "estimasi_yield_min": 12000,
                "estimasi_yield_max": 18000,
                "harga_jual_min": 20000,
                "harga_jual_max": 35000,
                "lama_tanam_bulan": 4
            },
            "items": [
                # Biaya Tetap
                {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Ha", "volume": 1, "harga": 5000000, "wajib": True},
                {"kategori": "Biaya Tetap", "item": "Penyusutan Alat", "satuan": "Paket", "volume": 1, "harga": 1500000, "wajib": True},
                
                # Benih
                {"kategori": "Benih", "item": "Benih Hibrida F1", "satuan": "Sachet", "volume": 15, "harga": 135000, "wajib": True},
                
                # Pupuk Kimia
                {"kategori": "Pupuk", "item": "Pupuk Kandang", "satuan": "Ton", "volume": 10, "harga": 600000, "wajib": True},
                {"kategori": "Pupuk", "item": "Urea", "satuan": "Kg", "volume": 300, "harga": 3500, "wajib": True},
                {"kategori": "Pupuk", "item": "SP-36", "satuan": "Kg", "volume": 200, "harga": 4000, "wajib": True},
                {"kategori": "Pupuk", "item": "KCl", "satuan": "Kg", "volume": 250, "harga": 5000, "wajib": True},
                {"kategori": "Pupuk", "item": "NPK 16-16-16", "satuan": "Kg", "volume": 400, "harga": 18000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Daun & Mikro", "satuan": "Paket", "volume": 1, "harga": 2000000, "wajib": True},
                
                # Pestisida Kimia
                {"kategori": "Pestisida", "item": "Insektisida (Thrips, Kutu)", "satuan": "Paket", "volume": 1, "harga": 3000000, "wajib": True},
                {"kategori": "Pestisida", "item": "Fungisida (Antraknosa)", "satuan": "Paket", "volume": 1, "harga": 2500000, "wajib": True},
                {"kategori": "Pestisida", "item": "Herbisida", "satuan": "Liter", "volume": 5, "harga": 120000, "wajib": True},
                
                # Penunjang
                {"kategori": "Penunjang", "item": "Mulsa Plastik Hitam Perak", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
                {"kategori": "Penunjang", "item": "Ajir Bambu", "satuan": "Batang", "volume": 20000, "harga": 400, "wajib": True},
                {"kategori": "Penunjang", "item": "Tali Gawar", "satuan": "Roll", "volume": 10, "harga": 45000, "wajib": True},
                
                # Tenaga Kerja
                {"kategori": "Tenaga Kerja", "item": "Olah Tanah & Bedengan", "satuan": "HOK", "volume": 60, "harga": 100000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemasangan Mulsa", "satuan": "HOK", "volume": 15, "harga": 90000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Penanaman", "satuan": "HOK", "volume": 25, "harga": 90000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemeliharaan", "satuan": "HOK", "volume": 80, "harga": 90000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemanenan", "satuan": "HOK", "volume": 120, "harga": 80000, "wajib": True},
            ],
            "roi_bulan": 12
        },
        
        "Kimia_Greenhouse": {
            "nama": "Kimia + Greenhouse",
            "deskripsi": "Budidaya intensif dalam greenhouse dengan input kimia",
            "params": {
                "populasi_ha": 30000,
                "estimasi_yield_min": 35000,
                "estimasi_yield_max": 50000,
                "harga_jual_min": 25000,
                "harga_jual_max": 40000,
                "lama_tanam_bulan": 4
            },
            "items": [
                # Biaya Tetap
                {"kategori": "Biaya Tetap", "item": "Amortisasi Greenhouse", "satuan": "Musim", "volume": 1, "harga": 20000000, "wajib": True},
                {"kategori": "Biaya Tetap", "item": "Sistem Fertigasi", "satuan": "Paket", "volume": 1, "harga": 15000000, "wajib": True},
                
                # Benih
                {"kategori": "Benih", "item": "Benih Hibrida Premium", "satuan": "Sachet", "volume": 25, "harga": 250000, "wajib": True},
                
                # Media & Pupuk
                {"kategori": "Media", "item": "Cocopeat + Sekam", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True},
                {"kategori": "Pupuk", "item": "AB Mix Premium", "satuan": "Kg", "volume": 500, "harga": 45000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Daun Lengkap", "satuan": "Paket", "volume": 1, "harga": 3000000, "wajib": True},
                
                # Pestisida
                {"kategori": "Pestisida", "item": "Paket Pestisida Intensif", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True},
                
                # Tenaga Kerja
                {"kategori": "Tenaga Kerja", "item": "Operator Greenhouse", "satuan": "HOK", "volume": 200, "harga": 100000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemanenan & QC", "satuan": "HOK", "volume": 200, "harga": 90000, "wajib": True},
            ],
            "roi_bulan": 18
        },
        
        "Campuran_Terbuka": {
            "nama": "Campuran + Terbuka",
            "deskripsi": "Kombinasi organik & kimia (IPM) di lahan terbuka",
            "params": {
                "populasi_ha": 18000,
                "estimasi_yield_min": 10000,
                "estimasi_yield_max": 15000,
                "harga_jual_min": 30000,
                "harga_jual_max": 45000,
                "lama_tanam_bulan": 4
            },
            "items": [
                # Biaya Tetap
                {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Ha", "volume": 1, "harga": 5000000, "wajib": True},
                {"kategori": "Biaya Tetap", "item": "Penyusutan Alat", "satuan": "Paket", "volume": 1, "harga": 1200000, "wajib": True},
                
                # Benih
                {"kategori": "Benih", "item": "Benih Unggul", "satuan": "Sachet", "volume": 15, "harga": 150000, "wajib": True},
                
                # Pupuk Campuran
                {"kategori": "Pupuk", "item": "Pupuk Kandang", "satuan": "Ton", "volume": 15, "harga": 700000, "wajib": True},
                {"kategori": "Pupuk", "item": "Kompos", "satuan": "Ton", "volume": 5, "harga": 900000, "wajib": True},
                {"kategori": "Pupuk", "item": "NPK 16-16-16", "satuan": "Kg", "volume": 300, "harga": 18000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Hayati", "satuan": "Liter", "volume": 50, "harga": 50000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Daun", "satuan": "Paket", "volume": 1, "harga": 1500000, "wajib": True},
                
                # Pestisida IPM
                {"kategori": "Pestisida", "item": "Biopestisida", "satuan": "Paket", "volume": 1, "harga": 2000000, "wajib": True},
                {"kategori": "Pestisida", "item": "Pestisida Kimia (Darurat)", "satuan": "Paket", "volume": 1, "harga": 2000000, "wajib": True},
                
                # Penunjang
                {"kategori": "Penunjang", "item": "Mulsa Plastik", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
                {"kategori": "Penunjang", "item": "Ajir Bambu", "satuan": "Batang", "volume": 20000, "harga": 450, "wajib": True},
                
                # Tenaga Kerja
                {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "HOK", "volume": 70, "harga": 100000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Penanaman & Pemeliharaan", "satuan": "HOK", "volume": 110, "harga": 90000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemanenan", "satuan": "HOK", "volume": 120, "harga": 80000, "wajib": True},
            ],
            "roi_bulan": 15
        },
        
        "Campuran_Greenhouse": {
            "nama": "Campuran + Greenhouse",
            "deskripsi": "IPM dalam greenhouse untuk hasil optimal",
            "params": {
                "populasi_ha": 28000,
                "estimasi_yield_min": 30000,
                "estimasi_yield_max": 45000,
                "harga_jual_min": 35000,
                "harga_jual_max": 55000,
                "lama_tanam_bulan": 4
            },
            "items": [
                # Biaya Tetap
                {"kategori": "Biaya Tetap", "item": "Amortisasi Greenhouse", "satuan": "Musim", "volume": 1, "harga": 22000000, "wajib": True},
                {"kategori": "Biaya Tetap", "item": "Sistem Irigasi", "satuan": "Paket", "volume": 1, "harga": 12000000, "wajib": True},
                
                # Benih
                {"kategori": "Benih", "item": "Benih Hibrida", "satuan": "Sachet", "volume": 22, "harga": 200000, "wajib": True},
                
                # Media & Pupuk
                {"kategori": "Media", "item": "Media Tanam Premium", "satuan": "Paket", "volume": 1, "harga": 10000000, "wajib": True},
                {"kategori": "Pupuk", "item": "Pupuk Organik + Kimia", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True},
                
                # Pest Control IPM
                {"kategori": "Pestisida", "item": "Paket IPM Lengkap", "satuan": "Paket", "volume": 1, "harga": 6000000, "wajib": True},
                
                # Tenaga Kerja
                {"kategori": "Tenaga Kerja", "item": "Operator & Maintenance", "satuan": "HOK", "volume": 180, "harga": 100000, "wajib": True},
                {"kategori": "Tenaga Kerja", "item": "Pemanenan & Sortir", "satuan": "HOK", "volume": 190, "harga": 90000, "wajib": True},
            ],
            "roi_bulan": 20
        }
    }
    
    @staticmethod
    def calculate_rab(scenario_key, luas_ha=1):
        """
        Hitung RAB untuk skenario tertentu
        
        Args:
            scenario_key: Key skenario (Organik_Terbuka, dll)
            luas_ha: Luas lahan dalam hektar
            
        Returns:
            Dict dengan breakdown biaya dan proyeksi
        """
        template = RABCalculatorService.RAB_TEMPLATES.get(scenario_key)
        if not template:
            return None
        
        # Hitung total biaya
        total_biaya = 0
        breakdown = {}
        
        for item in template['items']:
            biaya_item = item['volume'] * item['harga'] * luas_ha
            total_biaya += biaya_item
            
            kategori = item['kategori']
            if kategori not in breakdown:
                breakdown[kategori] = 0
            breakdown[kategori] += biaya_item
        
        # Proyeksi pendapatan
        params = template['params']
        yield_min = params['estimasi_yield_min'] * luas_ha
        yield_max = params['estimasi_yield_max'] * luas_ha
        harga_min = params['harga_jual_min']
        harga_max = params['harga_jual_max']
        
        pendapatan_min = yield_min * harga_min
        pendapatan_max = yield_max * harga_max
        pendapatan_avg = (pendapatan_min + pendapatan_max) / 2
        
        # ROI
        profit_min = pendapatan_min - total_biaya
        profit_max = pendapatan_max - total_biaya
        profit_avg = pendapatan_avg - total_biaya
        
        roi_min = (profit_min / total_biaya) * 100
        roi_max = (profit_max / total_biaya) * 100
        roi_avg = (profit_avg / total_biaya) * 100
        
        return {
            'scenario': template['nama'],
            'deskripsi': template['deskripsi'],
            'luas_ha': luas_ha,
            'total_biaya': total_biaya,
            'breakdown': breakdown,
            'items': template['items'],
            'proyeksi': {
                'yield_min_kg': yield_min,
                'yield_max_kg': yield_max,
                'pendapatan_min': pendapatan_min,
                'pendapatan_max': pendapatan_max,
                'pendapatan_avg': pendapatan_avg,
                'profit_min': profit_min,
                'profit_max': profit_max,
                'profit_avg': profit_avg,
                'roi_min_persen': roi_min,
                'roi_max_persen': roi_max,
                'roi_avg_persen': roi_avg,
                'payback_bulan': template['roi_bulan']
            }
        }
    
    @staticmethod
    def compare_scenarios(luas_ha=1):
        """Bandingkan semua 6 skenario"""
        comparisons = []
        
        for key in RABCalculatorService.RAB_TEMPLATES.keys():
            result = RABCalculatorService.calculate_rab(key, luas_ha)
            if result:
                comparisons.append({
                    'scenario': result['scenario'],
                    'investasi': result['total_biaya'],
                    'pendapatan_avg': result['proyeksi']['pendapatan_avg'],
                    'profit_avg': result['proyeksi']['profit_avg'],
                    'roi_avg': result['proyeksi']['roi_avg_persen'],
                    'payback_bulan': result['proyeksi']['payback_bulan']
                })
        
        return comparisons
