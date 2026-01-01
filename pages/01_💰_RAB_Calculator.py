"""
💰 RAB Calculator - Rencana Anggaran Biaya
6 Skenario Budidaya Cabai
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.rab_calculator_service import RABCalculatorService

st.set_page_config(
    page_title="RAB Calculator - Budidaya Cabai",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .scenario-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .cost-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF6B6B;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💰 RAB Calculator - Rencana Anggaran Biaya")
st.markdown("**Hitung biaya & proyeksi keuntungan untuk 6 skenario budidaya cabai**")

st.markdown("---")

# Sidebar - Input
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    luas_ha = st.number_input(
        "Luas Lahan (Ha)",
        min_value=0.1,
        max_value=100.0,
        value=1.0,
        step=0.1,
        help="Masukkan luas lahan dalam hektar"
    )
    
    st.markdown("---")
    
    st.markdown("### 🆚 6 Skenario")
    st.info("""
    1. **Organik + Terbuka**
    2. **Organik + Greenhouse**
    3. **Kimia + Terbuka**
    4. **Kimia + Greenhouse**
    5. **Campuran + Terbuka**
    6. **Campuran + Greenhouse**
    """)

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Perbandingan Skenario",
    "💵 Hitung RAB Detail",
    "📈 Analisis ROI"
])

with tab1:
    st.header("📊 Perbandingan 6 Skenario")
    
    # Get comparison data
    comparisons = RABCalculatorService.compare_scenarios(luas_ha)
    
    # Display as table
    df_comp = pd.DataFrame(comparisons)
    df_comp['investasi'] = df_comp['investasi'].apply(lambda x: f"Rp {x:,.0f}")
    df_comp['pendapatan_avg'] = df_comp['pendapatan_avg'].apply(lambda x: f"Rp {x:,.0f}")
    df_comp['profit_avg'] = df_comp['profit_avg'].apply(lambda x: f"Rp {x:,.0f}")
    df_comp['roi_avg'] = df_comp['roi_avg'].apply(lambda x: f"{x:.1f}%")
    df_comp['payback_bulan'] = df_comp['payback_bulan'].apply(lambda x: f"{x} bulan")
    
    df_comp.columns = ['Skenario', 'Investasi', 'Pendapatan Rata-rata', 'Profit Rata-rata', 'ROI', 'Payback Period']
    
    st.dataframe(df_comp, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Visualization
    st.subheader("📈 Visualisasi Perbandingan")
    
    # Prepare data for charts
    comp_raw = RABCalculatorService.compare_scenarios(luas_ha)
    df_viz = pd.DataFrame(comp_raw)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment comparison
        fig1 = px.bar(
            df_viz,
            x='scenario',
            y='investasi',
            title='Perbandingan Investasi',
            labels={'investasi': 'Investasi (Rp)', 'scenario': 'Skenario'},
            color='investasi',
            color_continuous_scale='Reds'
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # ROI comparison
        fig2 = px.bar(
            df_viz,
            x='scenario',
            y='roi_avg',
            title='Perbandingan ROI',
            labels={'roi_avg': 'ROI (%)', 'scenario': 'Skenario'},
            color='roi_avg',
            color_continuous_scale='Greens'
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Profit comparison
    fig3 = px.bar(
        df_viz,
        x='scenario',
        y='profit_avg',
        title='Perbandingan Profit Rata-rata',
        labels={'profit_avg': 'Profit (Rp)', 'scenario': 'Skenario'},
        color='profit_avg',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.header("💵 Hitung RAB Detail")
    
    # Select scenario
    scenario_options = {
        "Organik + Terbuka": "Organik_Terbuka",
        "Organik + Greenhouse": "Organik_Greenhouse",
        "Kimia + Terbuka": "Kimia_Terbuka",
        "Kimia + Greenhouse": "Kimia_Greenhouse",
        "Campuran + Terbuka": "Campuran_Terbuka",
        "Campuran + Greenhouse": "Campuran_Greenhouse"
    }
    
    selected_scenario = st.selectbox(
        "Pilih Skenario",
        list(scenario_options.keys())
    )
    
    scenario_key = scenario_options[selected_scenario]
    
    # Calculate
    result = RABCalculatorService.calculate_rab(scenario_key, luas_ha)
    
    if result:
        # Display scenario info
        st.markdown(f"""
        <div class="scenario-card">
            <h3>{result['scenario']}</h3>
            <p>{result['deskripsi']}</p>
            <p><strong>Luas Lahan:</strong> {result['luas_ha']} Ha</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Investasi",
                f"Rp {result['total_biaya']:,.0f}"
            )
        
        with col2:
            st.metric(
                "Pendapatan (Avg)",
                f"Rp {result['proyeksi']['pendapatan_avg']:,.0f}"
            )
        
        with col3:
            st.metric(
                "Profit (Avg)",
                f"Rp {result['proyeksi']['profit_avg']:,.0f}",
                delta=f"{result['proyeksi']['roi_avg_persen']:.1f}% ROI"
            )
        
        with col4:
            st.metric(
                "Payback Period",
                f"{result['proyeksi']['payback_bulan']} bulan"
            )
        
        st.markdown("---")
        
        # Breakdown by category
        st.subheader("📋 Breakdown Biaya per Kategori")
        
        breakdown_data = []
        for kategori, biaya in result['breakdown'].items():
            persen = (biaya / result['total_biaya']) * 100
            breakdown_data.append({
                'Kategori': kategori,
                'Biaya': f"Rp {biaya:,.0f}",
                '% dari Total': f"{persen:.1f}%"
            })
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
        
        # Pie chart
        fig_pie = px.pie(
            values=list(result['breakdown'].values()),
            names=list(result['breakdown'].keys()),
            title='Distribusi Biaya'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed items
        st.subheader("📝 Rincian Item Detail")
        
        items_data = []
        for item in result['items']:
            total = item['volume'] * item['harga'] * luas_ha
            items_data.append({
                'Kategori': item['kategori'],
                'Item': item['item'],
                'Volume': f"{item['volume'] * luas_ha:.0f} {item['satuan']}",
                'Harga Satuan': f"Rp {item['harga']:,.0f}",
                'Total': f"Rp {total:,.0f}"
            })
        
        df_items = pd.DataFrame(items_data)
        st.dataframe(df_items, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_items.to_csv(index=False)
        st.download_button(
            label="📥 Download RAB (CSV)",
            data=csv,
            file_name=f"RAB_{scenario_key}_{luas_ha}ha.csv",
            mime="text/csv"
        )

with tab3:
    st.header("📈 Analisis ROI & Sensitivitas")
    
    # Select scenario for analysis
    selected_scenario_roi = st.selectbox(
        "Pilih Skenario untuk Analisis",
        list(scenario_options.keys()),
        key="roi_scenario"
    )
    
    scenario_key_roi = scenario_options[selected_scenario_roi]
    result_roi = RABCalculatorService.calculate_rab(scenario_key_roi, luas_ha)
    
    if result_roi:
        st.subheader("💰 Proyeksi Pendapatan & Profit")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Skenario Minimum:**
            - Yield: {result_roi['proyeksi']['yield_min_kg']:,.0f} kg
            - Pendapatan: Rp {result_roi['proyeksi']['pendapatan_min']:,.0f}
            - Profit: Rp {result_roi['proyeksi']['profit_min']:,.0f}
            - ROI: {result_roi['proyeksi']['roi_min_persen']:.1f}%
            """)
        
        with col2:
            st.markdown(f"""
            **Skenario Maksimum:**
            - Yield: {result_roi['proyeksi']['yield_max_kg']:,.0f} kg
            - Pendapatan: Rp {result_roi['proyeksi']['pendapatan_max']:,.0f}
            - Profit: Rp {result_roi['proyeksi']['profit_max']:,.0f}
            - ROI: {result_roi['proyeksi']['roi_max_persen']:.1f}%
            """)
        
        st.markdown("---")
        
        # ROI Range visualization
        st.subheader("📊 Range ROI")
        
        fig_roi = go.Figure()
        
        fig_roi.add_trace(go.Bar(
            name='ROI Range',
            x=[result_roi['scenario']],
            y=[result_roi['proyeksi']['roi_avg_persen']],
            error_y=dict(
                type='data',
                symmetric=False,
                array=[result_roi['proyeksi']['roi_max_persen'] - result_roi['proyeksi']['roi_avg_persen']],
                arrayminus=[result_roi['proyeksi']['roi_avg_persen'] - result_roi['proyeksi']['roi_min_persen']]
            ),
            marker_color='#FF6B6B'
        ))
        
        fig_roi.update_layout(
            title='ROI Range (Min - Avg - Max)',
            yaxis_title='ROI (%)',
            showlegend=False
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
        
        st.markdown("---")
        
        # Break-even analysis
        st.subheader("⚖️ Break-Even Analysis")
        
        break_even_kg = result_roi['total_biaya'] / ((result_roi['proyeksi']['pendapatan_avg'] / ((result_roi['proyeksi']['yield_min_kg'] + result_roi['proyeksi']['yield_max_kg']) / 2)))
        
        st.info(f"""
        **Break-Even Point:**
        - Produksi minimum: **{break_even_kg:,.0f} kg**
        - Dengan harga rata-rata saat ini
        - Di bawah ini = rugi, di atas ini = untung
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>💰 RAB Calculator</strong> - Budidaya Cabai Platform</p>
    <p><small>Data berdasarkan riset pasar & pengalaman petani</small></p>
</div>
""", unsafe_allow_html=True)
