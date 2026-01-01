"""
Disease Detection Service
Integrate image analysis with disease pattern matching
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_processing import (
    process_uploaded_image,
    analyze_leaf_color,
    detect_spots,
    calculate_texture_score,
    create_visualization,
    auto_score_leaf_color,
    estimate_pest_severity
)
from data.disease_patterns import (
    get_disease_by_pattern,
    calculate_health_score_from_image
)

class DiseaseDetectionService:
    
    @staticmethod
    def analyze_image(uploaded_file):
        """
        Complete image analysis pipeline
        
        Returns:
            dict with all analysis results
        """
        # Process image
        image = process_uploaded_image(uploaded_file)
        
        # Color analysis
        color_analysis = analyze_leaf_color(image)
        
        # Spot detection
        spot_analysis = detect_spots(image)
        
        # Texture analysis
        texture_score = calculate_texture_score(image)
        
        # Create visualization
        vis_image = create_visualization(image, color_analysis, spot_analysis)
        
        # Disease matching
        diseases = get_disease_by_pattern(
            color_analysis['green_percentage'],
            spot_analysis['spot_density_percentage'],
            color_analysis['yellow_percentage'],
            color_analysis['brown_percentage']
        )
        
        # Calculate health score
        health_score = calculate_health_score_from_image(
            color_analysis['green_percentage'],
            spot_analysis['spot_density_percentage'],
            color_analysis['yellow_percentage']
        )
        
        # Auto-score for health assessment
        leaf_color_score = auto_score_leaf_color(
            color_analysis['green_percentage'],
            color_analysis['yellow_percentage']
        )
        
        pest_severity = estimate_pest_severity(
            spot_analysis['spot_density_percentage'],
            color_analysis['brown_percentage']
        )
        
        return {
            'color_analysis': color_analysis,
            'spot_analysis': spot_analysis,
            'texture_score': texture_score,
            'visualization': vis_image,
            'detected_diseases': diseases,
            'health_score': health_score,
            'auto_scores': {
                'leaf_color': leaf_color_score,
                'pest_severity': pest_severity
            }
        }
    
    @staticmethod
    def get_treatment_recommendations(diseases):
        """Get treatment recommendations from detected diseases"""
        if not diseases:
            return {
                'primary_treatment': "Tidak ada penyakit terdeteksi. Lanjutkan perawatan rutin.",
                'pesticides': [],
                'prevention': ["Monitoring rutin", "Sanitasi kebun", "Nutrisi seimbang"]
            }
        
        # Get top disease
        top_disease = diseases[0]
        
        # Extract pesticide recommendations
        treatment = top_disease['treatment']
        pesticides = []
        
        # Parse pesticide names from treatment string
        if 'Fungisida' in treatment:
            if 'Mankozeb' in treatment:
                pesticides.append('Mankozeb')
            if 'Klorotalonil' in treatment:
                pesticides.append('Klorotalonil')
            if 'Azoxystrobin' in treatment:
                pesticides.append('Azoxystrobin')
        elif 'Insektisida' in treatment:
            if 'Imidacloprid' in treatment:
                pesticides.append('Imidacloprid')
        elif 'Bakterisida' in treatment:
            if 'Streptomycin' in treatment:
                pesticides.append('Streptomycin')
        elif 'Pupuk' in treatment:
            if 'Urea' in treatment or 'nitrogen' in treatment.lower():
                pesticides.append('Pupuk Nitrogen (Urea)')
        
        return {
            'primary_treatment': treatment,
            'pesticides': pesticides,
            'prevention': top_disease.get('prevention', [])
        }
