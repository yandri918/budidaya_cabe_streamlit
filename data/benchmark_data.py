"""
Regional Benchmark Database
Provides regional performance benchmarks for comparative analysis
"""

from typing import Dict, List


class BenchmarkDatabase:
    """Database of regional agricultural benchmarks"""
    
    # Regional benchmarks for chili cultivation (ton/ha, Rp/ha, %)
    REGIONAL_BENCHMARKS = {
        'jawa_barat': {
            'name': 'Jawa Barat',
            'yield': {'p10': 6, 'p25': 8, 'p50': 10, 'p75': 12, 'p90': 14, 'p95': 16},
            'cost': {'p10': 35000000, 'p25': 42000000, 'p50': 50000000, 'p75': 58000000, 'p90': 65000000, 'p95': 70000000},
            'roi': {'p10': 60, 'p25': 80, 'p50': 100, 'p75': 120, 'p90': 150, 'p95': 180},
            'sample_size': 450,
            'characteristics': 'Lahan subur, akses pasar baik, teknologi tinggi'
        },
        'jawa_tengah': {
            'name': 'Jawa Tengah',
            'yield': {'p10': 5.5, 'p25': 7.5, 'p50': 9.5, 'p75': 11.5, 'p90': 13.5, 'p95': 15},
            'cost': {'p10': 32000000, 'p25': 40000000, 'p50': 48000000, 'p75': 55000000, 'p90': 62000000, 'p95': 68000000},
            'roi': {'p10': 55, 'p25': 75, 'p50': 95, 'p75': 115, 'p90': 140, 'p95': 170},
            'sample_size': 380,
            'characteristics': 'Lahan produktif, biaya tenaga kerja sedang'
        },
        'jawa_timur': {
            'name': 'Jawa Timur',
            'yield': {'p10': 6.5, 'p25': 8.5, 'p50': 10.5, 'p75': 12.5, 'p90': 14.5, 'p95': 16.5},
            'cost': {'p10': 33000000, 'p25': 41000000, 'p50': 49000000, 'p75': 56000000, 'p90': 63000000, 'p95': 69000000},
            'roi': {'p10': 65, 'p25': 85, 'p50': 105, 'p75': 125, 'p90': 155, 'p95': 185},
            'sample_size': 420,
            'characteristics': 'Varietas unggul, manajemen modern'
        },
        'sumatera_utara': {
            'name': 'Sumatera Utara',
            'yield': {'p10': 5, 'p25': 7, 'p50': 9, 'p75': 11, 'p90': 13, 'p95': 14.5},
            'cost': {'p10': 38000000, 'p25': 45000000, 'p50': 53000000, 'p75': 60000000, 'p90': 68000000, 'p95': 75000000},
            'roi': {'p10': 50, 'p25': 70, 'p50': 90, 'p75': 110, 'p90': 135, 'p95': 160},
            'sample_size': 280,
            'characteristics': 'Curah hujan tinggi, biaya logistik lebih tinggi'
        },
        'sulawesi_selatan': {
            'name': 'Sulawesi Selatan',
            'yield': {'p10': 4.5, 'p25': 6.5, 'p50': 8.5, 'p75': 10.5, 'p90': 12.5, 'p95': 14},
            'cost': {'p10': 36000000, 'p25': 43000000, 'p50': 51000000, 'p75': 58000000, 'p90': 66000000, 'p95': 72000000},
            'roi': {'p10': 45, 'p25': 65, 'p50': 85, 'p75': 105, 'p90': 130, 'p95': 155},
            'sample_size': 220,
            'characteristics': 'Pengembangan baru, potensi besar'
        },
        'nasional': {
            'name': 'Nasional (Rata-rata)',
            'yield': {'p10': 5.5, 'p25': 7.5, 'p50': 9.5, 'p75': 11.5, 'p90': 13.5, 'p95': 15.5},
            'cost': {'p10': 35000000, 'p25': 42000000, 'p50': 50000000, 'p75': 58000000, 'p90': 65000000, 'p95': 72000000},
            'roi': {'p10': 55, 'p25': 75, 'p50': 95, 'p75': 115, 'p90': 140, 'p95': 170},
            'sample_size': 1750,
            'characteristics': 'Agregasi semua region'
        }
    }
    
    # Variety-specific benchmarks
    VARIETY_BENCHMARKS = {
        'keriting': {
            'name': 'Cabai Keriting',
            'yield_potential': {'min': 8, 'avg': 12, 'max': 16},
            'price_range': {'min': 20000, 'avg': 30000, 'max': 50000},
            'growing_days': {'min': 90, 'avg': 110, 'max': 130},
            'characteristics': 'Populer, harga stabil, permintaan tinggi'
        },
        'rawit': {
            'name': 'Cabai Rawit',
            'yield_potential': {'min': 6, 'avg': 10, 'max': 14},
            'price_range': {'min': 25000, 'avg': 40000, 'max': 80000},
            'growing_days': {'min': 85, 'avg': 100, 'max': 120},
            'characteristics': 'Harga volatile, margin tinggi, risiko tinggi'
        },
        'merah_besar': {
            'name': 'Cabai Merah Besar',
            'yield_potential': {'min': 10, 'avg': 14, 'max': 18},
            'price_range': {'min': 18000, 'avg': 25000, 'max': 40000},
            'growing_days': {'min': 95, 'avg': 115, 'max': 135},
            'characteristics': 'Yield tinggi, harga lebih stabil'
        },
        'paprika': {
            'name': 'Paprika',
            'yield_potential': {'min': 15, 'avg': 25, 'max': 35},
            'price_range': {'min': 15000, 'avg': 25000, 'max': 40000},
            'growing_days': {'min': 100, 'avg': 120, 'max': 150},
            'characteristics': 'Teknologi tinggi, pasar premium'
        }
    }
    
    # Farm size categories
    FARM_SIZE_BENCHMARKS = {
        'small': {
            'name': 'Kecil (< 0.5 ha)',
            'area_range': (0, 0.5),
            'yield_adjustment': 0.9,  # 10% lower due to economies of scale
            'cost_adjustment': 1.1,   # 10% higher per ha
            'characteristics': 'Manajemen intensif, biaya per unit lebih tinggi'
        },
        'medium': {
            'name': 'Sedang (0.5 - 2 ha)',
            'area_range': (0.5, 2.0),
            'yield_adjustment': 1.0,  # Baseline
            'cost_adjustment': 1.0,
            'characteristics': 'Optimal untuk petani mandiri'
        },
        'large': {
            'name': 'Besar (> 2 ha)',
            'area_range': (2.0, float('inf')),
            'yield_adjustment': 1.05,  # 5% higher due to better management
            'cost_adjustment': 0.95,   # 5% lower due to bulk purchasing
            'characteristics': 'Economies of scale, manajemen profesional'
        }
    }
    
    @staticmethod
    def get_regional_benchmark(region: str) -> Dict:
        """Get benchmark data for specific region"""
        region_key = region.lower().replace(' ', '_')
        return BenchmarkDatabase.REGIONAL_BENCHMARKS.get(
            region_key,
            BenchmarkDatabase.REGIONAL_BENCHMARKS['nasional']
        )
    
    @staticmethod
    def get_variety_benchmark(variety: str) -> Dict:
        """Get benchmark data for specific variety"""
        variety_key = variety.lower().replace(' ', '_')
        return BenchmarkDatabase.VARIETY_BENCHMARKS.get(
            variety_key,
            BenchmarkDatabase.VARIETY_BENCHMARKS['keriting']
        )
    
    @staticmethod
    def get_farm_size_category(area: float) -> Dict:
        """Determine farm size category and get benchmarks"""
        for category, data in BenchmarkDatabase.FARM_SIZE_BENCHMARKS.items():
            min_area, max_area = data['area_range']
            if min_area <= area < max_area:
                return data
        return BenchmarkDatabase.FARM_SIZE_BENCHMARKS['medium']
    
    @staticmethod
    def calculate_percentile_rank(value: float, benchmark_dict: Dict, lower_is_better: bool = False) -> int:
        """
        Calculate percentile rank for a given value
        
        Args:
            value: Value to rank
            benchmark_dict: Dictionary with percentile values (p10, p25, p50, p75, p90, p95)
            lower_is_better: If True, lower values get higher percentiles
        
        Returns:
            Percentile rank (0-100)
        """
        if lower_is_better:
            if value <= benchmark_dict['p10']:
                return 95
            elif value <= benchmark_dict['p25']:
                return 85
            elif value <= benchmark_dict['p50']:
                return 65
            elif value <= benchmark_dict['p75']:
                return 40
            elif value <= benchmark_dict['p90']:
                return 20
            else:
                return 10
        else:
            if value >= benchmark_dict['p95']:
                return 98
            elif value >= benchmark_dict['p90']:
                return 93
            elif value >= benchmark_dict['p75']:
                return 80
            elif value >= benchmark_dict['p50']:
                return 60
            elif value >= benchmark_dict['p25']:
                return 35
            elif value >= benchmark_dict['p10']:
                return 15
            else:
                return 5
    
    @staticmethod
    def get_performance_tier(percentile: int) -> Dict:
        """Get performance tier based on percentile"""
        if percentile >= 90:
            return {
                'tier': 'Top Performer',
                'icon': '🏆',
                'color': '#FFD700',
                'message': 'Anda termasuk 10% petani terbaik!'
            }
        elif percentile >= 75:
            return {
                'tier': 'Above Average',
                'icon': '⭐',
                'color': '#2ECC71',
                'message': 'Performa di atas rata-rata'
            }
        elif percentile >= 50:
            return {
                'tier': 'Average',
                'icon': '✓',
                'color': '#3498DB',
                'message': 'Performa rata-rata'
            }
        elif percentile >= 25:
            return {
                'tier': 'Below Average',
                'icon': '⚠',
                'color': '#F39C12',
                'message': 'Ada ruang untuk perbaikan'
            }
        else:
            return {
                'tier': 'Needs Improvement',
                'icon': '❗',
                'color': '#E74C3C',
                'message': 'Perlu perbaikan signifikan'
            }
    
    @staticmethod
    def get_improvement_targets(
        current_value: float,
        benchmark_dict: Dict,
        metric_name: str
    ) -> List[Dict]:
        """
        Generate improvement targets based on benchmarks
        
        Args:
            current_value: Current performance value
            benchmark_dict: Benchmark percentiles
            metric_name: Name of metric (yield, cost, roi)
        
        Returns:
            List of improvement targets
        """
        targets = []
        
        # Determine if lower is better
        lower_is_better = metric_name.lower() == 'cost'
        
        if lower_is_better:
            # For cost, target lower values
            if current_value > benchmark_dict['p50']:
                targets.append({
                    'level': 'Target Awal',
                    'value': benchmark_dict['p50'],
                    'improvement': current_value - benchmark_dict['p50'],
                    'improvement_pct': ((current_value - benchmark_dict['p50']) / current_value * 100),
                    'description': 'Capai rata-rata nasional'
                })
            
            if current_value > benchmark_dict['p25']:
                targets.append({
                    'level': 'Target Menengah',
                    'value': benchmark_dict['p25'],
                    'improvement': current_value - benchmark_dict['p25'],
                    'improvement_pct': ((current_value - benchmark_dict['p25']) / current_value * 100),
                    'description': 'Masuk 25% terbaik'
                })
            
            if current_value > benchmark_dict['p10']:
                targets.append({
                    'level': 'Target Ambisius',
                    'value': benchmark_dict['p10'],
                    'improvement': current_value - benchmark_dict['p10'],
                    'improvement_pct': ((current_value - benchmark_dict['p10']) / current_value * 100),
                    'description': 'Masuk 10% terbaik'
                })
        else:
            # For yield/roi, target higher values
            if current_value < benchmark_dict['p50']:
                targets.append({
                    'level': 'Target Awal',
                    'value': benchmark_dict['p50'],
                    'improvement': benchmark_dict['p50'] - current_value,
                    'improvement_pct': ((benchmark_dict['p50'] - current_value) / current_value * 100),
                    'description': 'Capai rata-rata nasional'
                })
            
            if current_value < benchmark_dict['p75']:
                targets.append({
                    'level': 'Target Menengah',
                    'value': benchmark_dict['p75'],
                    'improvement': benchmark_dict['p75'] - current_value,
                    'improvement_pct': ((benchmark_dict['p75'] - current_value) / current_value * 100),
                    'description': 'Masuk 25% terbaik'
                })
            
            if current_value < benchmark_dict['p90']:
                targets.append({
                    'level': 'Target Ambisius',
                    'value': benchmark_dict['p90'],
                    'improvement': benchmark_dict['p90'] - current_value,
                    'improvement_pct': ((benchmark_dict['p90'] - current_value) / current_value * 100),
                    'description': 'Masuk 10% terbaik'
                })
        
        return targets
    
    @staticmethod
    def get_all_regions() -> List[str]:
        """Get list of all available regions"""
        return [data['name'] for data in BenchmarkDatabase.REGIONAL_BENCHMARKS.values()]
    
    @staticmethod
    def get_all_varieties() -> List[str]:
        """Get list of all available varieties"""
        return [data['name'] for data in BenchmarkDatabase.VARIETY_BENCHMARKS.values()]
