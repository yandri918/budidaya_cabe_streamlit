"""
Quality Control Service
QR code generation, traceability, inspections, certifications, and lab tests
"""

import qrcode
import io
import base64
from datetime import datetime, timedelta
import json
import pandas as pd
from data.quality_standards import (
    QUALITY_STANDARDS,
    INSPECTION_CHECKLISTS,
    CERTIFICATION_TYPES,
    LAB_TEST_TYPES,
    PASS_CRITERIA
)

class QualityControlService:
    
    # ===== QR CODE GENERATION =====
    
    @staticmethod
    def generate_product_id(harvest_id, batch_number):
        """Generate unique product ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"CHI-{harvest_id}-{batch_number}-{timestamp}"
    
    @staticmethod
    def generate_qr_code(product_data):
        """
        Generate QR code for product traceability
        
        Args:
            product_data: Dict with product information
        
        Returns:
            dict with QR code image and data
        """
        # Create verification URL for Vercel website
        product_id = product_data.get('product_id', '')
        verification_url = f"https://cabe-q-r-vercel.vercel.app/?id={product_id}"
        
        # Also prepare JSON data for reference
        qr_data = {
            'product_id': product_id,
            'harvest_date': product_data.get('harvest_date', ''),
            'farm_location': product_data.get('farm_location', ''),
            'farmer_name': product_data.get('farmer_name', ''),
            'grade': product_data.get('grade', ''),
            'batch_number': product_data.get('batch_number', ''),
            'weight_kg': product_data.get('weight_kg', 0),
            'certifications': product_data.get('certifications', []),
            'verification_url': verification_url
        }
        
        # Generate QR code with Vercel URL (not JSON)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(verification_url)  # Use URL instead of JSON
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            'qr_image_base64': img_str,
            'qr_data': qr_data,
            'qr_string': verification_url,  # Return URL
            'verification_url': verification_url
        }
    
    # ===== TRACEABILITY =====
    
    @staticmethod
    def create_traceability_record(harvest_data, growth_records, journal_entries):
        """
        Create complete traceability record
        
        Args:
            harvest_data: Harvest information
            growth_records: Growth monitoring data
            journal_entries: Journal activities
        
        Returns:
            dict with complete traceability timeline
        """
        timeline = []
        
        # Planting
        if growth_records:
            first_record = growth_records[0]
            timeline.append({
                'date': first_record.get('planting_date', ''),
                'event': 'Penanaman',
                'description': f"Bibit ditanam di {harvest_data.get('farm_location', '')}",
                'type': 'planting',
                'icon': '🌱'
            })
        
        # Growth milestones
        for record in growth_records:
            timeline.append({
                'date': record.get('created_at', '')[:10] if record.get('created_at') else '',
                'event': f'Monitoring HST {record.get("hst", 0)}',
                'description': f"Tinggi: {record.get('height_cm', 0)}cm, Daun: {record.get('leaf_count', 0)}",
                'type': 'growth',
                'icon': '📏'
            })
        
        # Journal activities (fertilization, spraying, etc.)
        for entry in journal_entries:
            timeline.append({
                'date': entry.get('date', ''),
                'event': entry.get('activity_type', ''),
                'description': entry.get('description', ''),
                'type': 'activity',
                'icon': '📝'
            })
        
        # Harvest
        timeline.append({
            'date': harvest_data.get('date', ''),
            'event': 'Panen',
            'description': f"Panen {harvest_data.get('weight_kg', 0)}kg Grade {harvest_data.get('grading', '')}",
            'type': 'harvest',
            'icon': '🌾'
        })
        
        # Sort by date
        timeline.sort(key=lambda x: x['date'])
        
        # Calculate inputs summary
        inputs_summary = QualityControlService._summarize_inputs(journal_entries)
        
        return {
            'product_id': harvest_data.get('product_id', ''),
            'timeline': timeline,
            'inputs_summary': inputs_summary,
            'total_days': len(set([t['date'] for t in timeline if t['date']])),
            'farm_info': {
                'location': harvest_data.get('farm_location', ''),
                'farmer': harvest_data.get('farmer_name', '')
            }
        }
    
    @staticmethod
    def _summarize_inputs(journal_entries):
        """Summarize inputs used"""
        summary = {
            'fertilizer': [],
            'pesticide': [],
            'organic': True
        }
        
        for entry in journal_entries:
            activity_type = entry.get('activity_type', '')
            
            if 'Pupuk' in activity_type or 'Pemupukan' in activity_type:
                summary['fertilizer'].append(entry.get('description', ''))
            
            if 'Pestisida' in activity_type or 'Penyemprotan' in activity_type:
                summary['pesticide'].append(entry.get('description', ''))
                # Check if chemical pesticide used
                if 'kimia' in entry.get('description', '').lower():
                    summary['organic'] = False
        
        return summary
    
    # ===== QUALITY INSPECTION =====
    
    @staticmethod
    def create_inspection_checklist(inspection_type):
        """Get inspection checklist template"""
        return INSPECTION_CHECKLISTS.get(inspection_type, {})
    
    @staticmethod
    def score_inspection(inspection_type, checklist_results):
        """
        Score inspection based on checklist results
        
        Args:
            inspection_type: Type of inspection
            checklist_results: Dict of item_id: passed (True/False)
        
        Returns:
            dict with score and status
        """
        checklist = INSPECTION_CHECKLISTS.get(inspection_type, {})
        items = checklist.get('items', [])
        
        total_score = 0
        max_score = 0
        critical_passed = True
        failed_items = []
        
        for item in items:
            item_id = item['id']
            weight = item['weight']
            critical = item['critical']
            passed = checklist_results.get(item_id, False)
            
            max_score += weight
            
            if passed:
                total_score += weight
            else:
                failed_items.append(item['item'])
                if critical:
                    critical_passed = False
        
        # Calculate percentage
        score_pct = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Determine pass/fail
        passed = score_pct >= PASS_CRITERIA['inspection_score'] and critical_passed
        
        # Status
        if passed:
            status = 'PASS'
            status_color = '#2ECC71'
        else:
            status = 'FAIL'
            status_color = '#E74C3C'
        
        return {
            'score': round(score_pct, 1),
            'max_score': 100,
            'passed': passed,
            'status': status,
            'status_color': status_color,
            'critical_passed': critical_passed,
            'failed_items': failed_items,
            'recommendations': QualityControlService._get_inspection_recommendations(failed_items)
        }
    
    @staticmethod
    def _get_inspection_recommendations(failed_items):
        """Generate recommendations based on failed items"""
        recs = []
        
        if not failed_items:
            return ["Semua item lolos inspeksi - pertahankan standar kualitas"]
        
        for item in failed_items:
            if 'hama' in item.lower():
                recs.append("Tingkatkan pengendalian hama - gunakan Module 09")
            elif 'penyakit' in item.lower():
                recs.append("Lakukan treatment penyakit sebelum panen")
            elif 'kematangan' in item.lower():
                recs.append("Tunda panen hingga kematangan optimal")
            elif 'cuaca' in item.lower():
                recs.append("Pilih waktu panen saat cuaca cerah")
            elif 'bersih' in item.lower():
                recs.append("Pastikan kebersihan peralatan dan wadah")
        
        if not recs:
            recs.append("Perbaiki item yang gagal sebelum melanjutkan")
        
        return recs
    
    # ===== CERTIFICATION TRACKING =====
    
    @staticmethod
    def track_certification(cert_type, issue_date, cert_number, document_path=""):
        """
        Track certification
        
        Args:
            cert_type: Type of certification
            issue_date: Issue date
            cert_number: Certificate number
            document_path: Path to certificate document
        
        Returns:
            dict with certification record
        """
        cert_info = CERTIFICATION_TYPES.get(cert_type, {})
        
        # Calculate expiry
        validity_months = cert_info.get('validity_months', 12)
        issue_dt = datetime.strptime(issue_date, '%Y-%m-%d') if isinstance(issue_date, str) else issue_date
        expiry_date = issue_dt + timedelta(days=validity_months * 30)
        
        # Check status
        days_to_expiry = (expiry_date - datetime.now()).days
        
        if days_to_expiry < 0:
            status = 'Expired'
            status_color = '#E74C3C'
            status_icon = '✗'
        elif days_to_expiry < 30:
            status = 'Expiring Soon'
            status_color = '#F39C12'
            status_icon = '⚠'
        else:
            status = 'Valid'
            status_color = '#2ECC71'
            status_icon = '✓'
        
        return {
            'cert_type': cert_type,
            'cert_name': cert_info.get('name', ''),
            'cert_number': cert_number,
            'issue_date': issue_date,
            'expiry_date': expiry_date.strftime('%Y-%m-%d'),
            'days_to_expiry': days_to_expiry,
            'status': status,
            'status_color': status_color,
            'status_icon': status_icon,
            'document_path': document_path,
            'requirements': cert_info.get('requirements', []),
            'benefits': cert_info.get('benefits', [])
        }
    
    @staticmethod
    def get_expiring_certifications(certifications, days_threshold=60):
        """Get certifications expiring within threshold"""
        expiring = []
        
        for cert in certifications:
            if cert['days_to_expiry'] < days_threshold and cert['days_to_expiry'] >= 0:
                expiring.append(cert)
        
        return expiring
    
    # ===== LAB TEST RESULTS =====
    
    @staticmethod
    def store_lab_result(test_type, test_date, results, lab_name="", cert_number=""):
        """
        Store lab test result
        
        Args:
            test_type: Type of test
            test_date: Test date
            results: Dict of parameter: value
            lab_name: Laboratory name
            cert_number: Certificate number
        
        Returns:
            dict with test record
        """
        test_info = LAB_TEST_TYPES.get(test_type, {})
        
        # Check compliance
        passed = True
        failed_params = []
        
        for param, value in results.items():
            # Simple pass/fail logic (in real app, check against MRL)
            if isinstance(value, str):
                if 'fail' in value.lower() or 'exceed' in value.lower():
                    passed = False
                    failed_params.append(param)
        
        # Status
        if passed:
            status = 'PASS'
            status_color = '#2ECC71'
            status_icon = '✓'
        else:
            status = 'FAIL'
            status_color = '#E74C3C'
            status_icon = '✗'
        
        return {
            'test_type': test_type,
            'test_name': test_info.get('name', ''),
            'test_date': test_date,
            'lab_name': lab_name,
            'cert_number': cert_number,
            'results': results,
            'passed': passed,
            'status': status,
            'status_color': status_color,
            'status_icon': status_icon,
            'failed_params': failed_params,
            'mrl_standard': test_info.get('mrl', ''),
            'recommendations': QualityControlService._get_test_recommendations(test_type, passed)
        }
    
    @staticmethod
    def _get_test_recommendations(test_type, passed):
        """Generate recommendations based on test results"""
        if passed:
            return ["Hasil test memenuhi standar - produk aman untuk konsumsi"]
        
        recs = []
        
        if test_type == 'pesticide_residue':
            recs.append("Kurangi penggunaan pestisida kimia")
            recs.append("Perpanjang periode tunggu sebelum panen")
            recs.append("Gunakan pestisida nabati (Module 09)")
        elif test_type == 'heavy_metals':
            recs.append("Periksa sumber air irigasi")
            recs.append("Test tanah untuk kontaminasi")
            recs.append("Pertimbangkan remediasi tanah")
        elif test_type == 'microbiology':
            recs.append("Tingkatkan sanitasi pasca panen")
            recs.append("Gunakan air bersih untuk pencucian")
            recs.append("Perbaiki kondisi penyimpanan")
        
        return recs
    
    @staticmethod
    def analyze_test_trends(test_history):
        """Analyze trends in lab test results"""
        if len(test_history) < 2:
            return {
                'insufficient_data': True,
                'message': 'Minimal 2 test results diperlukan untuk analisis trend'
            }
        
        # Count pass/fail
        total_tests = len(test_history)
        passed_tests = sum(1 for t in test_history if t.get('passed', False))
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Recent trend
        recent_3 = test_history[-3:]
        recent_pass_rate = (sum(1 for t in recent_3 if t.get('passed', False)) / len(recent_3) * 100)
        
        # Trend direction
        if recent_pass_rate > pass_rate:
            trend = 'Improving'
            trend_icon = '↗'
            trend_color = '#2ECC71'
        elif recent_pass_rate < pass_rate:
            trend = 'Declining'
            trend_icon = '↘'
            trend_color = '#E74C3C'
        else:
            trend = 'Stable'
            trend_icon = '→'
            trend_color = '#3498DB'
        
        return {
            'insufficient_data': False,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'pass_rate': round(pass_rate, 1),
            'recent_pass_rate': round(recent_pass_rate, 1),
            'trend': trend,
            'trend_icon': trend_icon,
            'trend_color': trend_color,
            'insights': QualityControlService._get_trend_insights(pass_rate, trend)
        }
    
    @staticmethod
    def _get_trend_insights(pass_rate, trend):
        """Generate insights from trends"""
        insights = []
        
        if pass_rate >= 90:
            insights.append("✓ Kualitas produk sangat baik")
        elif pass_rate >= 75:
            insights.append("✓ Kualitas produk baik, ada ruang perbaikan")
        else:
            insights.append("⚠ Kualitas produk perlu ditingkatkan")
        
        if trend == 'Improving':
            insights.append("✓ Trend positif - praktik budidaya membaik")
        elif trend == 'Declining':
            insights.append("⚠ Trend negatif - perlu evaluasi praktik budidaya")
        
        return insights
