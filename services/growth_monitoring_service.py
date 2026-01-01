"""
Growth Monitoring Service
Track plant growth, compare with milestones, and calculate health scores
"""

from data.growth_milestones import (
    GROWTH_MILESTONES,
    HEALTH_CRITERIA,
    get_milestone_for_hst,
    get_phase_for_hst,
    calculate_health_score
)
from datetime import datetime, timedelta

class GrowthMonitoringService:
    
    @staticmethod
    def calculate_hst(planting_date):
        """Calculate HST (Hari Setelah Tanam) from planting date"""
        if isinstance(planting_date, str):
            planting_date = datetime.strptime(planting_date, "%Y-%m-%d")
        elif hasattr(planting_date, 'year'):  # date object
            planting_date = datetime.combine(planting_date, datetime.min.time())
        
        today = datetime.now()
        delta = today - planting_date
        return delta.days
    
    @staticmethod
    def get_current_milestone(hst):
        """Get current milestone and phase for HST"""
        return get_milestone_for_hst(hst)
    
    @staticmethod
    def get_all_milestones():
        """Get all milestones grouped by phase"""
        return GROWTH_MILESTONES
    
    @staticmethod
    def compare_with_milestone(hst, actual_height, actual_leaves):
        """
        Compare actual measurements with expected milestone
        
        Returns:
            dict with comparison results
        """
        milestone_data = get_milestone_for_hst(hst)
        
        if not milestone_data:
            return None
        
        milestone = milestone_data['milestone']
        expected_height = milestone['expected_height_cm']
        expected_leaves = milestone['expected_leaves']
        
        height_diff = actual_height - expected_height
        height_pct = (height_diff / expected_height * 100) if expected_height > 0 else 0
        
        leaves_diff = actual_leaves - expected_leaves
        leaves_pct = (leaves_diff / expected_leaves * 100) if expected_leaves > 0 else 0
        
        # Overall status
        if height_pct >= 0 and leaves_pct >= 0:
            status = "Sesuai Target" if abs(height_pct) < 20 and abs(leaves_pct) < 20 else "Di Atas Target"
            status_color = "#2ECC71"
        elif height_pct < -20 or leaves_pct < -20:
            status = "Di Bawah Target"
            status_color = "#E74C3C"
        else:
            status = "Mendekati Target"
            status_color = "#F39C12"
        
        return {
            'hst': hst,
            'phase': milestone_data['phase'],
            'milestone_event': milestone['event'],
            'expected_height': expected_height,
            'actual_height': actual_height,
            'height_diff': height_diff,
            'height_pct': round(height_pct, 1),
            'expected_leaves': expected_leaves,
            'actual_leaves': actual_leaves,
            'leaves_diff': leaves_diff,
            'leaves_pct': round(leaves_pct, 1),
            'status': status,
            'status_color': status_color,
            'description': milestone['description'],
            'actions': milestone['actions']
        }
    
    @staticmethod
    def assess_health(leaf_color, stem_strength, pest_severity, growth_rate):
        """Calculate health score and get recommendations"""
        health_result = calculate_health_score(
            leaf_color,
            stem_strength,
            pest_severity,
            growth_rate
        )
        
        # Add recommendations based on score
        score = health_result['score']
        
        if score >= 90:
            recommendations = [
                "Pertahankan perawatan rutin",
                "Lanjutkan monitoring preventif",
                "Dokumentasikan best practices"
            ]
        elif score >= 70:
            recommendations = [
                "Tingkatkan monitoring",
                "Perhatikan nutrisi tanaman",
                "Aplikasi preventif lebih intensif"
            ]
        elif score >= 50:
            recommendations = [
                "Identifikasi masalah spesifik",
                "Aplikasi pupuk/pestisida sesuai kebutuhan",
                "Perbaiki kondisi lingkungan"
            ]
        elif score >= 30:
            recommendations = [
                "Tindakan kuratif segera",
                "Konsultasi ahli jika perlu",
                "Isolasi tanaman sakit"
            ]
        else:
            recommendations = [
                "Evaluasi kelayakan tanaman",
                "Pertimbangkan replanting",
                "Perbaiki sistem budidaya"
            ]
        
        health_result['recommendations'] = recommendations
        return health_result
    
    @staticmethod
    def generate_growth_timeline(planting_date, current_hst=None):
        """
        Generate growth timeline with past and future milestones
        
        Args:
            planting_date: Date when planted
            current_hst: Current HST (if None, calculate from planting_date)
        
        Returns:
            list of milestones with dates and status
        """
        if isinstance(planting_date, str):
            planting_date = datetime.strptime(planting_date, "%Y-%m-%d")
        elif hasattr(planting_date, 'year'):  # date object
            planting_date = datetime.combine(planting_date, datetime.min.time())
        
        if current_hst is None:
            current_hst = GrowthMonitoringService.calculate_hst(planting_date)
        
        timeline = []
        
        for phase, data in GROWTH_MILESTONES.items():
            for milestone in data['milestones']:
                milestone_hst = milestone['hst']
                milestone_date = planting_date + timedelta(days=milestone_hst)
                
                # Determine status
                if milestone_hst < current_hst:
                    status = "Selesai"
                    status_color = "#95A5A6"
                elif milestone_hst == current_hst:
                    status = "Sekarang"
                    status_color = "#3498DB"
                else:
                    status = "Akan Datang"
                    status_color = "#BDC3C7"
                
                timeline.append({
                    'hst': milestone_hst,
                    'date': milestone_date.strftime("%Y-%m-%d"),
                    'phase': phase,
                    'event': milestone['event'],
                    'expected_height': milestone['expected_height_cm'],
                    'expected_leaves': milestone['expected_leaves'],
                    'description': milestone['description'],
                    'actions': milestone['actions'],
                    'status': status,
                    'status_color': status_color
                })
        
        return sorted(timeline, key=lambda x: x['hst'])
    
    @staticmethod
    def calculate_growth_rate(measurements):
        """
        Calculate growth rate from series of measurements
        
        Args:
            measurements: list of dicts with 'hst', 'height', 'leaves'
        
        Returns:
            dict with growth rates
        """
        if len(measurements) < 2:
            return None
        
        # Sort by HST
        sorted_measurements = sorted(measurements, key=lambda x: x['hst'])
        
        # Calculate rates
        first = sorted_measurements[0]
        last = sorted_measurements[-1]
        
        days_diff = last['hst'] - first['hst']
        
        if days_diff == 0:
            return None
        
        height_rate = (last['height'] - first['height']) / days_diff
        leaves_rate = (last['leaves'] - first['leaves']) / days_diff
        
        return {
            'period_days': days_diff,
            'height_rate_cm_per_day': round(height_rate, 2),
            'leaves_rate_per_day': round(leaves_rate, 2),
            'total_height_growth': last['height'] - first['height'],
            'total_leaves_growth': last['leaves'] - first['leaves']
        }
