"""
Budidaya Cabai - Enterprise Platform
Main Dashboard & Navigation
"""

import streamlit as st
import sys
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Chili Cultivation Enterprise Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #10b981;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .stat-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .stat-card h2 {
        color: #10b981;
        font-size: 2rem;
        margin: 0;
    }
    .stat-card p {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>Chili Cultivation Enterprise Platform</h1>
    <p style="color: #d1d5db; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
        Integrated agricultural intelligence system powered by data science. 
        Featuring standard operating procedures, financial modeling, and precision agronomy.
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h2>12</h2>
        <p>Core Modules</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h2>6</h2>
        <p>Cultivation Scenarios</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h2>10+</h2>
        <p>Disease Database</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h2>100%</h2>
        <p>Data Driven</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Features
st.markdown("### 🎯 Core Capabilities")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>Planting Calendar</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Optimal timeline recommendations based on geospatial climate data.</p>
    </div>
    <div class="feature-card">
        <h4>Price Forecasting</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Machine Learning models (Prophet) for 3-6 month market trend analysis.</p>
    </div>
    <div class="feature-card">
        <h4>AI Advisory System</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Personalized cultivation strategy recommendations.</p>
    </div>
    <div class="feature-card">
        <h4>RAB Calculator</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Comprehensive budgeting with ROI analysis for 6 scenarios.</p>
    </div>
    <div class="feature-card">
        <h4>Standard Procedures (SOP)</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Industry-standard operating procedures for consistency.</p>
    </div>
    <div class="feature-card">
        <h4>Fertilizer Calculator</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Precision NPK macro & micro nutrient calculation.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>Pest & Disease Management</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Integrated database with organic and chemical solutions.</p>
    </div>
    <div class="feature-card">
        <h4>Business Analytics</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Financial modeling including break-even and cashflow analysis.</p>
    </div>
    <div class="feature-card">
        <h4>Variety Database</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Characteristics and yield potential of top cultivars.</p>
    </div>
    <div class="feature-card">
        <h4>Best Practices</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Expert tips for yield maximization and risk mitigation.</p>
    </div>
    <div class="feature-card">
        <h4>Market Intelligence</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">Real-time price monitoring and statistical insights.</p>
    </div>
    <div class="feature-card">
        <h4>Comprehensive Guide</h4>
        <p style="color: #6b7280; font-size: 0.9rem;">End-to-end cultivation manual for all experience levels.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 6 Cultivation Scenarios
st.markdown("### 📊 Cultivation Models Comparison")

import pandas as pd

scenarios_data = {
    'Scenario': [
        '1. Organic + Open Field',
        '2. Organic + Greenhouse',
        '3. Chemical + Open Field',
        '4. Chemical + Greenhouse',
        '5. Hybrid + Open Field',
        '6. Hybrid + Greenhouse'
    ],
    'Investment/ha': [
        'IDR 30-50M',
        'IDR 250-400M',
        'IDR 20-35M',
        'IDR 200-350M',
        'IDR 25-40M',
        'IDR 220-380M'
    ],
    'Yield (ton/ha)': [
        '8-12',
        '25-35',
        '12-18',
        '35-50',
        '10-15',
        '30-45'
    ],
    'Price Potential': [
        'High',
        'Premium',
        'Standard',
        'Standard+',
        'Medium',
        'High'
    ],
    'ROI Period (months)': [
        '18-24',
        '20-30',
        '10-15',
        '15-20',
        '12-18',
        '16-24'
    ]
}

df_scenarios = pd.DataFrame(scenarios_data)
st.dataframe(df_scenarios, use_container_width=True, hide_index=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #9ca3af; padding: 2rem; border-top: 1px solid #e5e7eb;">
    <p><strong>AgriSensa Intelligence Systems</strong></p>
    <p style="font-size: 0.8rem;">© 2026 All Rights Reserved | Enterprise Edition</p>
</div>
""", unsafe_allow_html=True)
