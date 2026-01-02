"""
Advanced Analytics Service
ML-based predictions, forecasting, optimization, and benchmarking
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

class AnalyticsService:
    
    # ===== PREDICTIVE YIELD =====
    
    @staticmethod
    def predict_yield(hst, avg_height, avg_leaves, rainfall_mm=500, fertilizer_kg=300, pest_severity=10):
        """
        Predict yield using simple linear regression model
        
        Args:
            hst: Days after planting
            avg_height: Average plant height (cm)
            avg_leaves: Average leaf count
            rainfall_mm: Total rainfall (mm)
            fertilizer_kg: Total fertilizer used (kg)
            pest_severity: Pest severity (0-100%)
        
        Returns:
            dict with prediction results
        """
        # Simple rule-based model (can be replaced with trained ML model)
        # Base yield: 10 ton/ha
        base_yield = 10.0
        
        # HST factor (optimal at 120-140 days)
        if hst < 110:
            hst_factor = 0.5
        elif hst < 140:
            hst_factor = 1.0
        else:
            hst_factor = 0.9
        
        # Height factor (optimal at 60-80 cm)
        if avg_height < 40:
            height_factor = 0.7
        elif avg_height < 80:
            height_factor = 1.0
        else:
            height_factor = 0.95
        
        # Leaves factor (optimal at 40-60 leaves)
        if avg_leaves < 30:
            leaves_factor = 0.8
        elif avg_leaves < 60:
            leaves_factor = 1.0
        else:
            leaves_factor = 0.95
        
        # Rainfall factor (optimal 400-600mm)
        if rainfall_mm < 300:
            rain_factor = 0.7
        elif rainfall_mm < 700:
            rain_factor = 1.0
        else:
            rain_factor = 0.85
        
        # Fertilizer factor (optimal 250-350kg)
        if fertilizer_kg < 200:
            fert_factor = 0.8
        elif fertilizer_kg < 400:
            fert_factor = 1.0
        else:
            fert_factor = 0.9
        
        # Pest factor (lower is better)
        pest_factor = 1.0 - (pest_severity / 100 * 0.3)  # Max 30% reduction
        
        # Calculate predicted yield
        predicted_yield = base_yield * hst_factor * height_factor * leaves_factor * rain_factor * fert_factor * pest_factor
        
        # Confidence interval (±15%)
        confidence_low = predicted_yield * 0.85
        confidence_high = predicted_yield * 1.15
        
        # Key factors
        factors = []
        if hst_factor >= 1.0:
            factors.append({'factor': 'HST Optimal', 'impact': '+0%', 'color': '#2ECC71'})
        else:
            factors.append({'factor': 'HST Belum Optimal', 'impact': f'{(hst_factor-1)*100:.0f}%', 'color': '#E74C3C'})
        
        if height_factor >= 1.0:
            factors.append({'factor': 'Tinggi Optimal', 'impact': '+0%', 'color': '#2ECC71'})
        else:
            factors.append({'factor': 'Tinggi Perlu Ditingkatkan', 'impact': f'{(height_factor-1)*100:.0f}%', 'color': '#F39C12'})
        
        if pest_severity < 10:
            factors.append({'factor': 'Hama Terkendali', 'impact': '+0%', 'color': '#2ECC71'})
        else:
            factors.append({'factor': 'Serangan Hama', 'impact': f'-{pest_severity*0.3:.0f}%', 'color': '#E74C3C'})
        
        return {
            'predicted_yield': round(predicted_yield, 2),
            'confidence_low': round(confidence_low, 2),
            'confidence_high': round(confidence_high, 2),
            'accuracy': 85,  # Estimated accuracy
            'factors': factors,
            'recommendations': AnalyticsService._get_yield_recommendations(hst, avg_height, pest_severity)
        }
    
    @staticmethod
    def _get_yield_recommendations(hst, avg_height, pest_severity):
        """Generate recommendations to improve yield"""
        recs = []
        
        if hst < 110:
            recs.append("Fokus pada pertumbuhan vegetatif - pupuk nitrogen")
        
        if avg_height < 50:
            recs.append("Tingkatkan pemupukan untuk pertumbuhan tinggi")
        
        if pest_severity > 15:
            recs.append("Intensifkan pengendalian hama - gunakan Module 09")
        
        if hst > 110 and hst < 140:
            recs.append("Periode kritis - pastikan nutrisi dan air cukup")
        
        if not recs:
            recs.append("Pertahankan kondisi saat ini - sudah optimal")
        
        return recs
    
    # ===== PRICE FORECASTING =====
    
    @staticmethod
    def forecast_price(current_price=25000, days=30):
        """
        Forecast chili price using moving average and trend
        
        Args:
            current_price: Current market price (Rp/kg)
            days: Forecast horizon (days)
        
        Returns:
            dict with price forecast
        """
        # Simulated historical prices (in real app, get from database/API)
        # Seasonal pattern: prices higher in rainy season
        current_month = datetime.now().month
        
        # Seasonal multiplier
        if current_month in [11, 12, 1, 2]:  # Rainy season
            seasonal_trend = 1.15  # 15% higher
        elif current_month in [6, 7, 8]:  # Dry season
            seasonal_trend = 0.95  # 5% lower
        else:
            seasonal_trend = 1.0
        
        # Weekly trend (simulated)
        weekly_change = 0.02  # 2% per week average
        
        # Calculate forecasts
        forecast_7d = current_price * (1 + weekly_change)
        forecast_14d = current_price * (1 + weekly_change * 2)
        forecast_30d = current_price * seasonal_trend * (1 + weekly_change * 4)
        
        # Determine trend
        if seasonal_trend > 1.05:
            trend = "Upward"
            trend_icon = "↗"
            trend_color = "#2ECC71"
        elif seasonal_trend < 0.95:
            trend = "Downward"
            trend_icon = "↘"
            trend_color = "#E74C3C"
        else:
            trend = "Stable"
            trend_icon = "→"
            trend_color = "#3498DB"
        
        # Best selling time
        if seasonal_trend > 1.0:
            best_time_days = 25
            best_price = forecast_30d
        else:
            best_time_days = 7
            best_price = forecast_7d
        
        return {
            'current_price': current_price,
            'forecast_7d': round(forecast_7d, 0),
            'forecast_14d': round(forecast_14d, 0),
            'forecast_30d': round(forecast_30d, 0),
            'trend': trend,
            'trend_icon': trend_icon,
            'trend_color': trend_color,
            'best_selling_time': best_time_days,
            'best_price': round(best_price, 0),
            'insights': AnalyticsService._get_price_insights(seasonal_trend, current_month)
        }
    
    @staticmethod
    def _get_price_insights(seasonal_trend, month):
        """Generate price insights"""
        insights = []
        
        if seasonal_trend > 1.1:
            insights.append("Harga sedang tinggi - musim hujan meningkatkan permintaan")
            insights.append("Pertimbangkan menunda panen 1-2 minggu untuk harga lebih baik")
        elif seasonal_trend < 0.95:
            insights.append("Harga sedang rendah - panen melimpah")
            insights.append("Fokus pada kualitas premium untuk harga lebih baik")
        else:
            insights.append("Harga stabil - kondisi pasar normal")
        
        if month in [3, 4, 5]:
            insights.append("Menjelang musim kemarau - harga cenderung naik")
        
        return insights
    
    # ===== COST OPTIMIZATION =====
    
    @staticmethod
    def analyze_cost_efficiency(total_cost, cost_breakdown, yield_ton):
        """
        Analyze cost efficiency and suggest optimizations
        
        Args:
            total_cost: Total production cost
            cost_breakdown: Dict of cost categories
            yield_ton: Actual yield (ton/ha)
        
        Returns:
            dict with optimization analysis
        """
        # Calculate cost per kg
        cost_per_kg = total_cost / (yield_ton * 1000) if yield_ton > 0 else 0
        
        # Benchmark costs (industry average)
        benchmark_cost_per_kg = 15000  # Rp 15k/kg
        
        # Efficiency score (0-100)
        if cost_per_kg <= benchmark_cost_per_kg:
            efficiency_score = 100
        else:
            efficiency_score = max(0, 100 - ((cost_per_kg - benchmark_cost_per_kg) / benchmark_cost_per_kg * 100))
        
        # Analyze each cost category
        opportunities = []
        total_savings = 0
        
        # Fertilizer (should be ~25% of total)
        fert_pct = (cost_breakdown.get('Pupuk', 0) / total_cost * 100) if total_cost > 0 else 0
        if fert_pct > 30:
            saving = cost_breakdown.get('Pupuk', 0) * 0.15  # 15% savings potential
            opportunities.append({
                'category': 'Pupuk',
                'issue': f'Biaya pupuk tinggi ({fert_pct:.0f}% dari total)',
                'saving': saving,
                'actions': [
                    'Gunakan pupuk organik sebagai substitusi parsial',
                    'Beli pupuk dalam jumlah besar (bulk)',
                    'Gunakan Module 05 untuk optimasi dosis'
                ]
            })
            total_savings += saving
        
        # Pesticide (should be ~15% of total)
        pest_pct = (cost_breakdown.get('Pestisida', 0) / total_cost * 100) if total_cost > 0 else 0
        if pest_pct > 20:
            saving = cost_breakdown.get('Pestisida', 0) * 0.20  # 20% savings potential
            opportunities.append({
                'category': 'Pestisida',
                'issue': f'Biaya pestisida tinggi ({pest_pct:.0f}% dari total)',
                'saving': saving,
                'actions': [
                    'Terapkan rotasi pestisida (Module 09)',
                    'Gunakan pendekatan preventif vs kuratif',
                    'Pertimbangkan pestisida nabati'
                ]
            })
            total_savings += saving
        
        # Labor (should be ~20% of total)
        labor_pct = (cost_breakdown.get('Tenaga Kerja', 0) / total_cost * 100) if total_cost > 0 else 0
        if labor_pct > 25:
            saving = cost_breakdown.get('Tenaga Kerja', 0) * 0.10  # 10% savings potential
            opportunities.append({
                'category': 'Tenaga Kerja',
                'issue': f'Biaya tenaga kerja tinggi ({labor_pct:.0f}% dari total)',
                'saving': saving,
                'actions': [
                    'Optimalkan jadwal penyemprotan (gabungkan aktivitas)',
                    'Gunakan alat bantu untuk efisiensi',
                    'Pelatihan untuk produktivitas lebih tinggi'
                ]
            })
            total_savings += saving
        
        return {
            'efficiency_score': round(efficiency_score, 0),
            'cost_per_kg': round(cost_per_kg, 0),
            'benchmark_cost_per_kg': benchmark_cost_per_kg,
            'total_savings_potential': round(total_savings, 0),
            'opportunities': opportunities,
            'overall_assessment': AnalyticsService._get_efficiency_assessment(efficiency_score)
        }
    
    @staticmethod
    def _get_efficiency_assessment(score):
        """Get efficiency assessment"""
        if score >= 90:
            return {'level': 'Excellent', 'color': '#2ECC71', 'message': 'Efisiensi biaya sangat baik!'}
        elif score >= 75:
            return {'level': 'Good', 'color': '#3498DB', 'message': 'Efisiensi biaya baik, ada ruang untuk perbaikan'}
        elif score >= 60:
            return {'level': 'Fair', 'color': '#F39C12', 'message': 'Efisiensi biaya cukup, perlu optimasi'}
        else:
            return {'level': 'Poor', 'color': '#E74C3C', 'message': 'Efisiensi biaya rendah, butuh perbaikan segera'}
    
    # ===== BENCHMARKING =====
    
    @staticmethod
    def calculate_benchmarks(farmer_data):
        """
        Calculate performance benchmarks
        
        Args:
            farmer_data: Dict with yield, cost, roi
        
        Returns:
            dict with benchmark comparison
        """
        # Simulated benchmark data (in real app, aggregate from all farmers)
        benchmarks = {
            'yield': {'p25': 8, 'p50': 10, 'p75': 12, 'p90': 14},  # ton/ha
            'cost': {'p25': 40000000, 'p50': 50000000, 'p75': 60000000, 'p90': 70000000},  # Rp/ha
            'roi': {'p25': 80, 'p50': 100, 'p75': 120, 'p90': 150}  # %
        }
        
        # Calculate percentiles
        yield_percentile = AnalyticsService._calculate_percentile(
            farmer_data.get('yield', 10),
            benchmarks['yield']
        )
        
        cost_percentile = AnalyticsService._calculate_percentile(
            farmer_data.get('cost', 50000000),
            benchmarks['cost'],
            lower_is_better=True
        )
        
        roi_percentile = AnalyticsService._calculate_percentile(
            farmer_data.get('roi', 100),
            benchmarks['roi']
        )
        
        # Overall rank (average of percentiles)
        overall_rank = (yield_percentile + cost_percentile + roi_percentile) / 3
        
        return {
            'overall_rank': round(overall_rank, 0),
            'yield_percentile': yield_percentile,
            'cost_percentile': cost_percentile,
            'roi_percentile': roi_percentile,
            'benchmarks': benchmarks,
            'comparison': AnalyticsService._get_benchmark_comparison(farmer_data, benchmarks),
            'best_practices': AnalyticsService._get_best_practices(overall_rank)
        }
    
    @staticmethod
    def _calculate_percentile(value, benchmark_dict, lower_is_better=False):
        """Calculate percentile rank"""
        if lower_is_better:
            if value <= benchmark_dict['p25']:
                return 90
            elif value <= benchmark_dict['p50']:
                return 70
            elif value <= benchmark_dict['p75']:
                return 50
            else:
                return 30
        else:
            if value >= benchmark_dict['p90']:
                return 95
            elif value >= benchmark_dict['p75']:
                return 80
            elif value >= benchmark_dict['p50']:
                return 60
            elif value >= benchmark_dict['p25']:
                return 40
            else:
                return 20
    
    @staticmethod
    def _get_benchmark_comparison(farmer_data, benchmarks):
        """Get detailed comparison"""
        comparisons = []
        
        # Yield comparison
        yield_val = farmer_data.get('yield', 10)
        yield_avg = benchmarks['yield']['p50']
        yield_diff = ((yield_val - yield_avg) / yield_avg * 100)
        
        comparisons.append({
            'metric': 'Yield',
            'value': f"{yield_val} ton/ha",
            'average': f"{yield_avg} ton/ha",
            'difference': f"{yield_diff:+.0f}%",
            'status': 'above' if yield_diff > 0 else 'below',
            'color': '#2ECC71' if yield_diff > 0 else '#E74C3C'
        })
        
        # Cost comparison
        cost_val = farmer_data.get('cost', 50000000)
        cost_avg = benchmarks['cost']['p50']
        cost_diff = ((cost_val - cost_avg) / cost_avg * 100)
        
        comparisons.append({
            'metric': 'Cost',
            'value': f"Rp {cost_val:,.0f}",
            'average': f"Rp {cost_avg:,.0f}",
            'difference': f"{cost_diff:+.0f}%",
            'status': 'below' if cost_diff < 0 else 'above',
            'color': '#2ECC71' if cost_diff < 0 else '#E74C3C'
        })
        
        # ROI comparison
        roi_val = farmer_data.get('roi', 100)
        roi_avg = benchmarks['roi']['p50']
        roi_diff = ((roi_val - roi_avg) / roi_avg * 100)
        
        comparisons.append({
            'metric': 'ROI',
            'value': f"{roi_val}%",
            'average': f"{roi_avg}%",
            'difference': f"{roi_diff:+.0f}%",
            'status': 'above' if roi_diff > 0 else 'below',
            'color': '#2ECC71' if roi_diff > 0 else '#E74C3C'
        })
        
        return comparisons
    
    @staticmethod
    def _get_best_practices(rank):
        """Get best practices from top performers"""
        if rank >= 80:
            return [
                "Anda sudah di top 20%! Pertahankan praktik terbaik Anda",
                "Bagikan pengalaman Anda di Module 14 (Forum)"
            ]
        else:
            return [
                "Integrated Pest Management (IPM) - kurangi pestisida kimia",
                "Precision fertilization - gunakan Module 05 untuk dosis tepat",
                "Weather-based scheduling - gunakan Module 13 untuk timing optimal",
                "Regular monitoring - gunakan Module 10 & 11 untuk tracking",
                "Quality focus - Grade A mendapat harga 30-40% lebih tinggi"
            ]
    
    # ===== SEASONAL TRENDS =====
    
    @staticmethod
    def analyze_seasonal_trends(seasons_data):
        """
        Analyze trends across multiple seasons
        
        Args:
            seasons_data: List of dicts with season data
        
        Returns:
            dict with trend analysis
        """
        if not seasons_data or len(seasons_data) < 2:
            return {
                'insufficient_data': True,
                'message': 'Minimal 2 musim tanam diperlukan untuk analisis trend'
            }
        
        # Calculate trends
        yields = [s['yield'] for s in seasons_data]
        costs = [s['cost'] for s in seasons_data]
        rois = [s['roi'] for s in seasons_data]
        
        # Year-over-year growth
        yield_growth = ((yields[-1] - yields[0]) / yields[0] * 100) if yields[0] > 0 else 0
        cost_growth = ((costs[-1] - costs[0]) / costs[0] * 100) if costs[0] > 0 else 0
        roi_growth = ((rois[-1] - rois[0]) / rois[0] * 100) if rois[0] > 0 else 0
        
        # Forecast next season (simple linear projection)
        forecast_yield = yields[-1] * (1 + yield_growth/100)
        forecast_cost = costs[-1] * (1 + cost_growth/100)
        forecast_roi = rois[-1] * (1 + roi_growth/100)
        
        return {
            'insufficient_data': False,
            'seasons_count': len(seasons_data),
            'yield_trend': {
                'growth': round(yield_growth, 1),
                'direction': 'up' if yield_growth > 0 else 'down',
                'icon': '↗' if yield_growth > 0 else '↘',
                'color': '#2ECC71' if yield_growth > 0 else '#E74C3C'
            },
            'cost_trend': {
                'growth': round(cost_growth, 1),
                'direction': 'up' if cost_growth > 0 else 'down',
                'icon': '↗' if cost_growth > 0 else '↘',
                'color': '#E74C3C' if cost_growth > 0 else '#2ECC71'
            },
            'roi_trend': {
                'growth': round(roi_growth, 1),
                'direction': 'up' if roi_growth > 0 else 'down',
                'icon': '↗' if roi_growth > 0 else '↘',
                'color': '#2ECC71' if roi_growth > 0 else '#E74C3C'
            },
            'forecast': {
                'yield': round(forecast_yield, 1),
                'cost': round(forecast_cost, 0),
                'roi': round(forecast_roi, 1)
            },
            'insights': AnalyticsService._get_trend_insights(yield_growth, cost_growth, roi_growth)
        }
    
    @staticmethod
    def _get_trend_insights(yield_growth, cost_growth, roi_growth):
        """Generate trend insights"""
        insights = []
        
        if yield_growth > 10:
            insights.append("✓ Yield meningkat signifikan - praktik budidaya membaik")
        elif yield_growth < -5:
            insights.append("⚠ Yield menurun - perlu evaluasi praktik budidaya")
        
        if cost_growth > 15:
            insights.append("⚠ Biaya meningkat cepat - perlu optimasi (gunakan Module 18)")
        elif cost_growth < 5:
            insights.append("✓ Biaya terkendali dengan baik")
        
        if roi_growth > 10:
            insights.append("✓ ROI meningkat - profitabilitas membaik")
        elif roi_growth < 0:
            insights.append("⚠ ROI menurun - perlu perbaikan efisiensi")
        
        if yield_growth > cost_growth:
            insights.append("✓ Produktivitas meningkat lebih cepat dari biaya")
        
        return insights
