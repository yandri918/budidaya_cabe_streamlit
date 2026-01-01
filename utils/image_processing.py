"""
Image Processing Utilities
Color analysis and pattern detection for disease identification
"""

import cv2
import numpy as np
from PIL import Image
import io

def process_uploaded_image(uploaded_file, target_size=(640, 640)):
    """
    Process uploaded image file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        target_size: Resize to this size
    
    Returns:
        numpy array (BGR format for OpenCV)
    """
    # Read image
    image = Image.open(uploaded_file)
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array (RGB)
    img_array = np.array(image)
    
    # Convert RGB to BGR for OpenCV
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    return img_bgr

def analyze_leaf_color(image):
    """
    Analyze leaf color using HSV color space
    
    Returns:
        dict with color analysis results
    """
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define color ranges
    # Green (healthy leaf)
    green_lower = np.array([35, 40, 40])
    green_upper = np.array([85, 255, 255])
    
    # Yellow (deficiency/disease)
    yellow_lower = np.array([20, 40, 40])
    yellow_upper = np.array([35, 255, 255])
    
    # Brown (disease/dead)
    brown_lower = np.array([10, 40, 20])
    brown_upper = np.array([20, 255, 200])
    
    # Create masks
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)
    
    # Calculate percentages
    total_pixels = image.shape[0] * image.shape[1]
    green_pct = (np.sum(green_mask > 0) / total_pixels) * 100
    yellow_pct = (np.sum(yellow_mask > 0) / total_pixels) * 100
    brown_pct = (np.sum(brown_mask > 0) / total_pixels) * 100
    
    # Calculate average green intensity
    green_pixels = hsv[green_mask > 0]
    if len(green_pixels) > 0:
        avg_green_saturation = np.mean(green_pixels[:, 1])
        avg_green_value = np.mean(green_pixels[:, 2])
    else:
        avg_green_saturation = 0
        avg_green_value = 0
    
    return {
        'green_percentage': round(green_pct, 2),
        'yellow_percentage': round(yellow_pct, 2),
        'brown_percentage': round(brown_pct, 2),
        'avg_green_saturation': round(avg_green_saturation, 2),
        'avg_green_value': round(avg_green_value, 2),
        'green_mask': green_mask,
        'yellow_mask': yellow_mask,
        'brown_mask': brown_mask
    }

def detect_spots(image, min_area=50):
    """
    Detect dark spots (potential disease indicators)
    
    Returns:
        dict with spot analysis
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Threshold to find dark spots
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by area
    spots = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    # Calculate spot density
    total_spot_area = sum(cv2.contourArea(cnt) for cnt in spots)
    total_image_area = image.shape[0] * image.shape[1]
    spot_density = (total_spot_area / total_image_area) * 100
    
    return {
        'spot_count': len(spots),
        'spot_density_percentage': round(spot_density, 2),
        'spots': spots,
        'spot_mask': thresh
    }

def calculate_texture_score(image):
    """
    Calculate texture irregularity (simple variance-based)
    
    Returns:
        texture score (0-100, higher = more irregular)
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate Laplacian variance (edge detection)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    variance = laplacian.var()
    
    # Normalize to 0-100 scale (empirical scaling)
    texture_score = min(100, variance / 10)
    
    return round(texture_score, 2)

def create_visualization(image, color_analysis, spot_analysis):
    """
    Create visualization with overlays
    
    Returns:
        annotated image (RGB format)
    """
    # Create copy
    vis_image = image.copy()
    
    # Overlay green mask (semi-transparent)
    green_overlay = np.zeros_like(vis_image)
    green_overlay[color_analysis['green_mask'] > 0] = [0, 255, 0]
    vis_image = cv2.addWeighted(vis_image, 0.7, green_overlay, 0.3, 0)
    
    # Overlay yellow mask
    yellow_overlay = np.zeros_like(vis_image)
    yellow_overlay[color_analysis['yellow_mask'] > 0] = [0, 255, 255]
    vis_image = cv2.addWeighted(vis_image, 0.7, yellow_overlay, 0.3, 0)
    
    # Draw spot contours
    cv2.drawContours(vis_image, spot_analysis['spots'], -1, (0, 0, 255), 2)
    
    # Convert BGR to RGB for display
    vis_image_rgb = cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)
    
    return vis_image_rgb

def auto_score_leaf_color(green_pct, yellow_pct):
    """
    Auto-score leaf color (1-5) for health assessment
    
    Returns:
        score (1-5)
    """
    if green_pct >= 70 and yellow_pct < 10:
        return 5  # Hijau tua
    elif green_pct >= 50 and yellow_pct < 25:
        return 4  # Hijau normal
    elif green_pct >= 30 and yellow_pct < 40:
        return 3  # Hijau pucat
    elif green_pct >= 10 and yellow_pct < 60:
        return 2  # Kuning pucat
    else:
        return 1  # Kuning kering

def estimate_pest_severity(spot_density, brown_pct):
    """
    Estimate pest/disease severity (0-100%)
    
    Returns:
        severity percentage
    """
    # Combine spot density and browning
    severity = (spot_density * 0.6 + brown_pct * 0.4)
    
    return min(100, round(severity, 1))
