"""
Journal Service
Manage cultivation journal entries with SOP integration
"""

from data.activity_templates import (
    ACTIVITY_TEMPLATES,
    get_activity_template,
    get_sop_tasks_for_hst,
    get_all_sop_tasks
)
from datetime import datetime
import json

class JournalService:
    
    @staticmethod
    def create_entry(date, hst, activity_type, details, cost=0, notes="", completed=True):
        """Create a journal entry"""
        template = get_activity_template(activity_type)
        
        return {
            'date': date,
            'hst': hst,
            'activity_type': activity_type,
            'icon': template['icon'],
            'color': template['color'],
            'details': details,
            'cost': cost,
            'notes': notes,
            'completed': completed,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def get_sop_checklist(hst):
        """Get SOP tasks for HST as checklist"""
        tasks = get_sop_tasks_for_hst(hst)
        
        checklist = []
        for task in tasks:
            template = get_activity_template(task['activity_type'])
            checklist.append({
                'task': task['task'],
                'activity_type': task['activity_type'],
                'icon': template['icon'],
                'default_cost': template['default_cost'],
                'completed': False
            })
        
        return checklist
    
    @staticmethod
    def calculate_total_cost(entries):
        """Calculate total cost from entries"""
        return sum(entry.get('cost', 0) for entry in entries)
    
    @staticmethod
    def group_by_activity(entries):
        """Group entries by activity type"""
        grouped = {}
        
        for entry in entries:
            activity_type = entry['activity_type']
            if activity_type not in grouped:
                grouped[activity_type] = []
            grouped[activity_type].append(entry)
        
        return grouped
    
    @staticmethod
    def calculate_compliance_rate(completed_tasks, total_tasks):
        """Calculate SOP compliance rate"""
        if total_tasks == 0:
            return 0
        return (completed_tasks / total_tasks) * 100
    
    @staticmethod
    def export_to_csv(entries):
        """Export entries to CSV format"""
        import pandas as pd
        
        df = pd.DataFrame(entries)
        return df.to_csv(index=False)
    
    @staticmethod
    def generate_summary(entries, start_date=None, end_date=None):
        """Generate summary report"""
        if start_date:
            entries = [e for e in entries if e['date'] >= start_date]
        if end_date:
            entries = [e for e in entries if e['date'] <= end_date]
        
        total_cost = JournalService.calculate_total_cost(entries)
        grouped = JournalService.group_by_activity(entries)
        
        summary = {
            'period': f"{start_date or 'Start'} - {end_date or 'Now'}",
            'total_entries': len(entries),
            'total_cost': total_cost,
            'activities_breakdown': {}
        }
        
        for activity_type, activity_entries in grouped.items():
            summary['activities_breakdown'][activity_type] = {
                'count': len(activity_entries),
                'total_cost': sum(e.get('cost', 0) for e in activity_entries)
            }
        
        return summary
