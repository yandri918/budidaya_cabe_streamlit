"""
Dashboard Service
Consolidate data from all modules for comprehensive dashboard
"""

from datetime import datetime
import pandas as pd

class DashboardService:
    
    @staticmethod
    def get_summary_metrics(planting_date=None, land_area=1.0, total_rab=50000000):
        """
        Get summary metrics for dashboard
        
        Args:
            planting_date: Date when planted
            land_area: Land area in hectares
            total_rab: Total RAB investment
        
        Returns:
            dict with summary metrics
        """
        # Calculate HST
        if planting_date:
            if isinstance(planting_date, str):
                planting_date = datetime.strptime(planting_date, "%Y-%m-%d")
            hst = (datetime.now() - planting_date).days
        else:
            hst = 0
        
        # Determine phase
        if hst < 22:
            phase = "Persemaian"
        elif hst < 61:
            phase = "Vegetatif"
        elif hst < 91:
            phase = "Berbunga"
        elif hst < 150:
            phase = "Berbuah"
        else:
            phase = "Selesai"
        
        # Estimate expected yield (ton/ha)
        if hst < 110:
            expected_yield = 0
        elif hst < 150:
            # Linear growth from 110-150 HST
            progress = (hst - 110) / 40
            expected_yield = 12 * progress  # Target 12 ton/ha
        else:
            expected_yield = 12
        
        # Calculate expected revenue (Rp 25,000/kg average)
        expected_revenue = expected_yield * 1000 * 25000 * land_area
        
        # Calculate ROI
        if total_rab > 0:
            roi = ((expected_revenue - total_rab) / total_rab) * 100
        else:
            roi = 0
        
        return {
            'hst': hst,
            'phase': phase,
            'land_area': land_area,
            'total_investment': total_rab,
            'expected_yield': round(expected_yield, 1),
            'expected_revenue': round(expected_revenue, 0),
            'roi': round(roi, 1),
            'cost_per_ha': round(total_rab / land_area, 0) if land_area > 0 else 0
        }
    
    @staticmethod
    def get_cost_breakdown(total_rab=50000000):
        """
        Get cost breakdown for pie chart
        
        Returns:
            dict with cost categories
        """
        # Typical cost distribution for chili cultivation
        breakdown = {
            'Bibit': total_rab * 0.20,  # 20%
            'Pupuk': total_rab * 0.25,  # 25%
            'Pestisida': total_rab * 0.15,  # 15%
            'Mulsa & Ajir': total_rab * 0.10,  # 10%
            'Tenaga Kerja': total_rab * 0.20,  # 20%
            'Lain-lain': total_rab * 0.10   # 10%
        }
        
        return breakdown
    
    @staticmethod
    def calculate_profitability(total_rab, actual_yield, selling_price=25000):
        """
        Calculate profitability metrics
        
        Args:
            total_rab: Total investment
            actual_yield: Actual yield in ton/ha
            selling_price: Selling price per kg
        
        Returns:
            dict with profitability metrics
        """
        total_revenue = actual_yield * 1000 * selling_price
        profit = total_revenue - total_rab
        roi = (profit / total_rab * 100) if total_rab > 0 else 0
        
        return {
            'total_revenue': round(total_revenue, 0),
            'total_cost': total_rab,
            'profit': round(profit, 0),
            'roi': round(roi, 1),
            'profit_margin': round((profit / total_revenue * 100) if total_revenue > 0 else 0, 1)
        }
    
    @staticmethod
    def get_module_status():
        """Get status of all modules"""
        modules = [
            {"no": 1, "name": "RAB Calculator", "icon": "💰", "status": "Active"},
            {"no": 2, "name": "Panduan Budidaya", "icon": "📚", "status": "Active"},
            {"no": 3, "name": "Hama & Penyakit", "icon": "🐛", "status": "Active"},
            {"no": 4, "name": "SOP Lengkap", "icon": "📋", "status": "Active"},
            {"no": 5, "name": "Kalkulator Pupuk", "icon": "🧪", "status": "Active"},
            {"no": 6, "name": "Kalender Tanam", "icon": "📅", "status": "Active"},
            {"no": 7, "name": "Analisis Bisnis", "icon": "💼", "status": "Active"},
            {"no": 8, "name": "Varietas Cabai", "icon": "🌶️", "status": "Active"},
            {"no": 9, "name": "Strategi Penyemprotan", "icon": "💦", "status": "Active"},
            {"no": 10, "name": "Pantau Pertumbuhan", "icon": "📈", "status": "Active"},
            {"no": 11, "name": "Jurnal Budidaya", "icon": "📔", "status": "Active"},
            {"no": 12, "name": "Deteksi Penyakit AI", "icon": "📸", "status": "Active"},
            {"no": 13, "name": "Monitoring Cuaca", "icon": "🌡️", "status": "Active"},
            {"no": 14, "name": "Konsultasi & Forum", "icon": "💬", "status": "Active"},
            {"no": 15, "name": "Dashboard & Reports", "icon": "📊", "status": "Active"}
        ]
        
        return modules
    
    @staticmethod
    def generate_summary_report(metrics, cost_breakdown, profitability):
        """Generate text summary report"""
        report = f"""
# LAPORAN BUDIDAYA CABAI
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## RINGKASAN BUDIDAYA
- Luas Lahan: {metrics['land_area']} Ha
- HST (Hari Setelah Tanam): {metrics['hst']} hari
- Fase Pertumbuhan: {metrics['phase']}

## INVESTASI & BIAYA
- Total Investasi: Rp {metrics['total_investment']:,.0f}
- Biaya per Hektar: Rp {metrics['cost_per_ha']:,.0f}

### Breakdown Biaya:
"""
        for category, amount in cost_breakdown.items():
            percentage = (amount / metrics['total_investment'] * 100) if metrics['total_investment'] > 0 else 0
            report += f"- {category}: Rp {amount:,.0f} ({percentage:.1f}%)\n"
        
        report += f"""
## PROYEKSI HASIL
- Target Yield: {metrics['expected_yield']} ton/ha
- Estimasi Pendapatan: Rp {metrics['expected_revenue']:,.0f}
- Proyeksi ROI: {metrics['roi']:.1f}%

## PROFITABILITAS
- Total Pendapatan: Rp {profitability['total_revenue']:,.0f}
- Total Biaya: Rp {profitability['total_cost']:,.0f}
- Keuntungan: Rp {profitability['profit']:,.0f}
- ROI: {profitability['roi']:.1f}%
- Profit Margin: {profitability['profit_margin']:.1f}%

## REKOMENDASI
1. Monitoring rutin untuk mencapai target yield
2. Kontrol biaya sesuai RAB
3. Optimasi kualitas untuk harga premium
4. Dokumentasi lengkap untuk evaluasi

---
Generated by Budidaya Cabai Management System
https://budidayacabe.streamlit.app/
"""
        return report
