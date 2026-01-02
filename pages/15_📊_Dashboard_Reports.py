import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from services.dashboard_service import DashboardService

st.set_page_config(page_title="Dashboard & Reports", page_icon="📊", layout="wide")

st.title("📊 Dashboard & Reports")
st.markdown("**Ringkasan lengkap budidaya cabai Anda**")

# Input parameters
st.sidebar.header("⚙️ Parameter Budidaya")

planting_date = st.sidebar.date_input(
    "Tanggal Tanam",
    value=datetime.now() - timedelta(days=60),
    help="Tanggal mulai tanam"
)

land_area = st.sidebar.number_input(
    "Luas Lahan (Ha)",
    min_value=0.1,
    max_value=100.0,
    value=1.0,
    step=0.1
)

total_rab = st.sidebar.number_input(
    "Total RAB (Rp)",
    min_value=1000000,
    max_value=1000000000,
    value=50000000,
    step=1000000,
    help="Total investasi dari RAB Calculator"
)

actual_yield = st.sidebar.number_input(
    "Hasil Panen Aktual (ton/ha)",
    min_value=0.0,
    max_value=30.0,
    value=0.0,
    step=0.1,
    help="Isi jika sudah panen"
)

selling_price = st.sidebar.number_input(
    "Harga Jual (Rp/kg)",
    min_value=5000,
    max_value=100000,
    value=25000,
    step=1000
)

# Get metrics
metrics = DashboardService.get_summary_metrics(planting_date, land_area, total_rab)
cost_breakdown = DashboardService.get_cost_breakdown(total_rab)
profitability = DashboardService.calculate_profitability(
    total_rab, 
    actual_yield if actual_yield > 0 else metrics['expected_yield'],
    selling_price
)

# Summary Metrics
st.header("📈 Ringkasan Budidaya")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "HST (Hari Setelah Tanam)",
        f"{metrics['hst']} hari",
        delta=f"Fase: {metrics['phase']}"
    )

with col2:
    st.metric(
        "Total Investasi",
        f"Rp {metrics['total_investment']:,.0f}",
        delta=f"Rp {metrics['cost_per_ha']:,.0f}/ha"
    )

with col3:
    if actual_yield > 0:
        st.metric(
            "Hasil Panen Aktual",
            f"{actual_yield} ton/ha",
            delta=f"Target: {metrics['expected_yield']} ton/ha"
        )
    else:
        st.metric(
            "Target Yield",
            f"{metrics['expected_yield']} ton/ha",
            delta="Proyeksi"
        )

with col4:
    roi_color = "normal" if profitability['roi'] > 0 else "inverse"
    st.metric(
        "ROI",
        f"{profitability['roi']:.1f}%",
        delta=f"Profit: Rp {profitability['profit']:,.0f}"
    )

# Charts
st.markdown("---")
st.header("📊 Analisis Biaya & Pendapatan")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Cost breakdown pie chart
    fig_cost = go.Figure(data=[go.Pie(
        labels=list(cost_breakdown.keys()),
        values=list(cost_breakdown.values()),
        hole=0.4,
        marker=dict(colors=['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#95A5A6'])
    )])
    
    fig_cost.update_layout(
        title='Breakdown Biaya Produksi',
        height=400
    )
    
    st.plotly_chart(fig_cost, use_container_width=True)

with col_chart2:
    # Revenue vs Cost bar chart
    fig_revenue = go.Figure(data=[
        go.Bar(
            name='Biaya',
            x=['Total'],
            y=[profitability['total_cost']],
            marker_color='#E74C3C',
            text=[f"Rp {profitability['total_cost']:,.0f}"],
            textposition='outside'
        ),
        go.Bar(
            name='Pendapatan',
            x=['Total'],
            y=[profitability['total_revenue']],
            marker_color='#2ECC71',
            text=[f"Rp {profitability['total_revenue']:,.0f}"],
            textposition='outside'
        )
    ])
    
    fig_revenue.update_layout(
        title='Biaya vs Pendapatan',
        yaxis_title='Rupiah (Rp)',
        height=400,
        barmode='group'
    )
    
    st.plotly_chart(fig_revenue, use_container_width=True)

# Profitability Analysis
st.markdown("---")
st.header("💰 Analisis Profitabilitas")

col_prof1, col_prof2, col_prof3 = st.columns(3)

with col_prof1:
    st.metric(
        "Total Pendapatan",
        f"Rp {profitability['total_revenue']:,.0f}"
    )

with col_prof2:
    st.metric(
        "Keuntungan Bersih",
        f"Rp {profitability['profit']:,.0f}",
        delta=f"{profitability['profit_margin']:.1f}% margin"
    )

with col_prof3:
    st.metric(
        "Return on Investment",
        f"{profitability['roi']:.1f}%",
        delta="Tinggi" if profitability['roi'] > 100 else "Sedang" if profitability['roi'] > 50 else "Rendah"
    )

# Module Overview
st.markdown("---")
st.header("🎯 Status Modul")

modules = DashboardService.get_module_status()
df_modules = pd.DataFrame(modules)

# Display in 3 columns
col_mod1, col_mod2, col_mod3 = st.columns(3)

for i, module in enumerate(modules):
    col = [col_mod1, col_mod2, col_mod3][i % 3]
    with col:
        st.info(f"{module['icon']} **Module {module['no']}:** {module['name']}")

# Reports & Export
st.markdown("---")
st.header("📄 Laporan & Export")

col_report1, col_report2 = st.columns([2, 1])

with col_report1:
    st.subheader("Generate Laporan")
    
    if st.button("📋 Generate Summary Report", type="primary"):
        report = DashboardService.generate_summary_report(metrics, cost_breakdown, profitability)
        
        st.text_area(
            "Laporan Ringkasan",
            value=report,
            height=400
        )
        
        # Download button
        st.download_button(
            label="💾 Download Report (TXT)",
            data=report,
            file_name=f"laporan_budidaya_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

with col_report2:
    st.subheader("Export Data")
    
    # Export cost breakdown
    df_cost = pd.DataFrame({
        'Kategori': list(cost_breakdown.keys()),
        'Biaya (Rp)': list(cost_breakdown.values())
    })
    
    csv_cost = df_cost.to_csv(index=False)
    
    st.download_button(
        label="📊 Export Cost Breakdown (CSV)",
        data=csv_cost,
        file_name=f"cost_breakdown_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Export profitability
    df_profit = pd.DataFrame({
        'Metrik': ['Total Pendapatan', 'Total Biaya', 'Keuntungan', 'ROI (%)', 'Profit Margin (%)'],
        'Nilai': [
            profitability['total_revenue'],
            profitability['total_cost'],
            profitability['profit'],
            profitability['roi'],
            profitability['profit_margin']
        ]
    })
    
    csv_profit = df_profit.to_csv(index=False)
    
    st.download_button(
        label="💰 Export Profitability (CSV)",
        data=csv_profit,
        file_name=f"profitability_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Quick Links
st.markdown("---")
st.header("🔗 Quick Links ke Modul")

col_link1, col_link2, col_link3 = st.columns(3)

with col_link1:
    st.info("""
    **📊 Perencanaan:**
    - Module 01: RAB Calculator
    - Module 06: Kalender Tanam
    - Module 07: Analisis Bisnis
    """)

with col_link2:
    st.info("""
    **🌱 Eksekusi:**
    - Module 09: Strategi Penyemprotan
    - Module 10: Pantau Pertumbuhan
    - Module 11: Jurnal Budidaya
    """)

with col_link3:
    st.info("""
    **🔍 Monitoring:**
    - Module 12: Deteksi Penyakit AI
    - Module 13: Monitoring Cuaca
    - Module 14: Konsultasi & Forum
    """)

# Footer
st.markdown("---")
st.success("""
🎉 **Selamat! Anda telah mengakses semua 15 modul budidaya cabai!**

Website ini menyediakan solusi lengkap dari perencanaan hingga panen:
- ✅ 15 Modul Terintegrasi
- ✅ Kalkulator & Analisis Lengkap
- ✅ AI-Powered Features
- ✅ Real-time Weather Data
- ✅ Comprehensive Dashboard

**Gunakan semua fitur untuk hasil maksimal!**
""")

st.caption(f"Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
