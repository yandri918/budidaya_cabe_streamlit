"""
Harvest Report Service
Track multiple harvests with grading, weight, and pricing
"""

from datetime import datetime
import pandas as pd

class HarvestReportService:
    
    @staticmethod
    def create_harvest_entry(harvest_number, date, grading, weight_kg, price_per_kg, notes=""):
        """
        Create a harvest entry
        
        Args:
            harvest_number: Panen ke-berapa (1, 2, 3, ...)
            date: Tanggal panen
            grading: Grade (A, B, C, Reject)
            weight_kg: Berat dalam kg
            price_per_kg: Harga per kg
            notes: Catatan tambahan
        
        Returns:
            dict with harvest entry
        """
        total_value = weight_kg * price_per_kg
        
        return {
            'harvest_number': harvest_number,
            'date': date if isinstance(date, str) else date.strftime('%Y-%m-%d'),
            'grading': grading,
            'weight_kg': round(weight_kg, 2),
            'price_per_kg': price_per_kg,
            'total_value': round(total_value, 0),
            'notes': notes,
            'timestamp': datetime.now()
        }
    
    @staticmethod
    def calculate_harvest_summary(harvest_entries):
        """Calculate summary statistics from harvest entries"""
        if not harvest_entries:
            return {
                'total_harvests': 0,
                'total_weight': 0,
                'total_value': 0,
                'avg_price': 0,
                'grade_distribution': {},
                'best_harvest': None,
                'avg_weight_per_harvest': 0
            }
        
        df = pd.DataFrame(harvest_entries)
        
        # Grade distribution
        grade_dist = df.groupby('grading').agg({
            'weight_kg': 'sum',
            'total_value': 'sum'
        }).to_dict('index')
        
        # Best harvest (highest value)
        best_idx = df['total_value'].idxmax()
        best_harvest = df.loc[best_idx].to_dict()
        
        return {
            'total_harvests': len(harvest_entries),
            'total_weight': round(df['weight_kg'].sum(), 2),
            'total_value': round(df['total_value'].sum(), 0),
            'avg_price': round(df['price_per_kg'].mean(), 0),
            'grade_distribution': grade_dist,
            'best_harvest': best_harvest,
            'avg_weight_per_harvest': round(df['weight_kg'].mean(), 2)
        }
    
    @staticmethod
    def get_grade_info():
        """Get grading information"""
        return {
            'A': {
                'name': 'Grade A (Premium)',
                'description': 'Ukuran besar, warna merah cerah, tidak cacat',
                'typical_price_range': '25,000 - 35,000',
                'color': '#2ECC71'
            },
            'B': {
                'name': 'Grade B (Standar)',
                'description': 'Ukuran sedang, warna baik, cacat minimal',
                'typical_price_range': '18,000 - 25,000',
                'color': '#F39C12'
            },
            'C': {
                'name': 'Grade C (Ekonomis)',
                'description': 'Ukuran kecil, warna kurang, cacat ringan',
                'typical_price_range': '12,000 - 18,000',
                'color': '#E74C3C'
            },
            'Reject': {
                'name': 'Reject (Afkir)',
                'description': 'Busuk, cacat berat, tidak layak jual',
                'typical_price_range': '0 - 5,000',
                'color': '#95A5A6'
            }
        }
    
    @staticmethod
    def export_harvest_report(harvest_entries):
        """Export harvest report to CSV format"""
        if not harvest_entries:
            return ""
        
        df = pd.DataFrame(harvest_entries)
        df = df[['harvest_number', 'date', 'grading', 'weight_kg', 'price_per_kg', 'total_value', 'notes']]
        df.columns = ['Panen Ke', 'Tanggal', 'Grade', 'Berat (kg)', 'Harga/kg', 'Total Nilai', 'Catatan']
        
        return df.to_csv(index=False)
    
    @staticmethod
    def calculate_yield_per_ha(total_weight_kg, land_area_ha):
        """Calculate yield per hectare"""
        if land_area_ha <= 0:
            return 0
        
        yield_per_ha = (total_weight_kg / 1000) / land_area_ha  # Convert to ton/ha
        return round(yield_per_ha, 2)
    
    @staticmethod
    def calculate_roi(total_revenue, total_investment):
        """Calculate ROI from harvest"""
        if total_investment <= 0:
            return 0
        
        profit = total_revenue - total_investment
        roi = (profit / total_investment) * 100
        
        return {
            'total_revenue': round(total_revenue, 0),
            'total_investment': total_investment,
            'profit': round(profit, 0),
            'roi_percentage': round(roi, 1)
        }
