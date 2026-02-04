"""
📊 Analisis Bisnis Budidaya Cabai
ROI, Break-even, Cashflow Analysis
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
    page_title="Analisis Bisnis Cabai",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Analisis Bisnis Budidaya Cabai")
st.markdown("**ROI, Break-even, Cashflow & Sensitivity Analysis**")

st.markdown("---")

# Input
col1, col2, col3 = st.columns(3)

with col1:
    scenario = st.selectbox(
        "Skenario Budidaya",
        ["Organik_Terbuka", "Organik_Greenhouse", "Kimia_Terbuka", 
         "Kimia_Greenhouse", "Campuran_Terbuka", "Campuran_Greenhouse"]
    )
    
    luas_ha = st.number_input("Luas (Ha)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)

with col2:
    harga_jual = st.number_input("Harga Jual (Rp/kg)", min_value=10000, max_value=100000, value=30000, step=1000)
    
    yield_ton = st.number_input("Target Yield (ton/ha)", min_value=5.0, max_value=50.0, value=15.0, step=1.0)

with col3:
    modal_sendiri = st.slider("Modal Sendiri (%)", min_value=0, max_value=100, value=100, step=10)
    
    bunga_pinjaman = st.number_input("Bunga Pinjaman (%/tahun)", min_value=0.0, max_value=30.0, value=12.0, step=0.5)

# Calculate
if st.button("📊 Analisis", type="primary"):
    # Get RAB data
    rab_result = RABCalculatorService.calculate_rab(scenario, luas_ha)
    
    if rab_result:
        total_investasi = rab_result['total_biaya']
        
        # Adjust with actual inputs
        total_pendapatan = yield_ton * luas_ha * harga_jual * 1000  # Convert to kg
        total_profit = total_pendapatan - total_investasi
        roi_persen = (total_profit / total_investasi) * 100
        
        # Display metrics
        st.subheader("💰 Ringkasan Finansial")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric("Total Investasi", f"Rp {total_investasi:,.0f}")
        
        with col_m2:
            st.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
        
        with col_m3:
            st.metric("Profit", f"Rp {total_profit:,.0f}", 
                     delta=f"{roi_persen:.1f}% ROI")
        
        with col_m4:
            payback_months = (total_investasi / (total_profit / 4)) if total_profit > 0 else 0
            st.metric("Payback Period", f"{payback_months:.1f} bulan")
        
        st.markdown("---")
        
        # Break-even Analysis
        st.subheader("⚖️ Break-Even Analysis")
        
        break_even_kg = total_investasi / harga_jual
        break_even_ton = break_even_kg / 1000
        break_even_persen = (break_even_ton / (yield_ton * luas_ha)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Break-Even Point:**
            - Produksi minimum: **{break_even_ton:.2f} ton** ({break_even_kg:,.0f} kg)
            - Persentase dari target: **{break_even_persen:.1f}%**
            - Di bawah ini = **RUGI**
            - Di atas ini = **UNTUNG**
            """)
        
        with col2:
            # Break-even chart
            production_range = list(range(0, int(yield_ton * luas_ha * 1.5) + 1))
            revenue_line = [p * harga_jual * 1000 for p in production_range]
            cost_line = [total_investasi] * len(production_range)
            
            fig_be = go.Figure()
            fig_be.add_trace(go.Scatter(x=production_range, y=revenue_line, name='Pendapatan', line=dict(color='green')))
            fig_be.add_trace(go.Scatter(x=production_range, y=cost_line, name='Biaya', line=dict(color='red', dash='dash')))
            fig_be.add_vline(x=break_even_ton, line_dash="dot", line_color="orange", annotation_text="Break-Even")
            
            fig_be.update_layout(
                title='Break-Even Chart',
                xaxis_title='Produksi (ton)',
                yaxis_title='Rupiah',
                height=300
            )
            
            st.plotly_chart(fig_be, use_container_width=True)
        
        st.markdown("---")
        
        # Cashflow Analysis
        st.subheader("💸 Cashflow Projection (4 Bulan)")
        
        # Monthly cashflow
        cashflow_data = []
        
        # Month 0: Initial investment
        cashflow_data.append({
            "Bulan": 0,
            "Pengeluaran": total_investasi * 0.6,  # 60% di awal
            "Pemasukan": 0,
            "Cashflow": -total_investasi * 0.6,
            "Kumulatif": -total_investasi * 0.6
        })
        
        # Month 1-2: Maintenance
        for month in [1, 2]:
            pengeluaran = total_investasi * 0.15
            cashflow_data.append({
                "Bulan": month,
                "Pengeluaran": pengeluaran,
                "Pemasukan": 0,
                "Cashflow": -pengeluaran,
                "Kumulatif": cashflow_data[-1]["Kumulatif"] - pengeluaran
            })
        
        # Month 3-4: Harvest
        for month in [3, 4]:
            pengeluaran = total_investasi * 0.05
            pemasukan = total_pendapatan * 0.5  # 50% per bulan panen
            cashflow = pemasukan - pengeluaran
            cashflow_data.append({
                "Bulan": month,
                "Pengeluaran": pengeluaran,
                "Pemasukan": pemasukan,
                "Cashflow": cashflow,
                "Kumulatif": cashflow_data[-1]["Kumulatif"] + cashflow
            })
        
        df_cashflow = pd.DataFrame(cashflow_data)
        
        # Format for display
        df_display = df_cashflow.copy()
        for col in ["Pengeluaran", "Pemasukan", "Cashflow", "Kumulatif"]:
            df_display[col] = df_display[col].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Cashflow chart
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Bar(x=df_cashflow["Bulan"], y=df_cashflow["Cashflow"], name='Cashflow Bulanan'))
        fig_cf.add_trace(go.Scatter(x=df_cashflow["Bulan"], y=df_cashflow["Kumulatif"], name='Kumulatif', line=dict(color='red')))
        
        fig_cf.update_layout(
            title='Cashflow Analysis',
            xaxis_title='Bulan',
            yaxis_title='Rupiah',
            height=400
        )
        
        st.plotly_chart(fig_cf, use_container_width=True)
        
        st.markdown("---")
        
        # Sensitivity Analysis
        st.subheader("📈 Sensitivity Analysis")
        
        st.markdown("**Analisis Sensitivitas: Bagaimana jika harga atau yield berubah?**")
        
        # Price sensitivity
        price_range = [harga_jual * (1 + i/10) for i in range(-5, 6)]
        profit_by_price = [(yield_ton * luas_ha * 1000 * p) - total_investasi for p in price_range]
        
        # Yield sensitivity
        yield_range = [yield_ton * (1 + i/10) for i in range(-5, 6)]
        profit_by_yield = [(y * luas_ha * 1000 * harga_jual) - total_investasi for y in yield_range]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=[f"{p:,.0f}" for p in price_range],
                y=profit_by_price,
                mode='lines+markers',
                name='Profit'
            ))
            fig_price.add_hline(y=0, line_dash="dash", line_color="red")
            fig_price.update_layout(
                title='Sensitivitas Harga',
                xaxis_title='Harga Jual (Rp/kg)',
                yaxis_title='Profit (Rp)',
                height=300
            )
            st.plotly_chart(fig_price, use_container_width=True)
        
        with col2:
            fig_yield = go.Figure()
            fig_yield.add_trace(go.Scatter(
                x=[f"{y:.1f}" for y in yield_range],
                y=profit_by_yield,
                mode='lines+markers',
                name='Profit'
            ))
            fig_yield.add_hline(y=0, line_dash="dash", line_color="red")
            fig_yield.update_layout(
                title='Sensitivitas Yield',
                xaxis_title='Produksi (ton/ha)',
                yaxis_title='Profit (Rp)',
                height=300
            )
            st.plotly_chart(fig_yield, use_container_width=True)
        
        st.markdown("---")
        
        # Scenario Comparison
        st.subheader("🆚 Perbandingan Skenario")
        
        comparisons = RABCalculatorService.compare_scenarios(luas_ha)
        
        df_comp = pd.DataFrame(comparisons)
        
        fig_comp = px.bar(
            df_comp,
            x='scenario',
            y=['investasi', 'profit_avg'],
            title='Perbandingan Investasi vs Profit',
            barmode='group',
            labels={'value': 'Rupiah', 'scenario': 'Skenario'}
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Rekomendasi Bisnis")
        
        if roi_persen > 50:
            st.success(f"""
            ✅ **SANGAT MENGUNTUNGKAN!**
            - ROI: {roi_persen:.1f}% (Excellent!)
            - Payback: {payback_months:.1f} bulan (Cepat)
            - Rekomendasi: **GO!** Segera eksekusi
            """)
        elif roi_persen > 20:
            st.info(f"""
            ✓ **MENGUNTUNGKAN**
            - ROI: {roi_persen:.1f}% (Good)
            - Payback: {payback_months:.1f} bulan
            - Rekomendasi: **Layak** untuk dijalankan
            """)
        else:
            st.warning(f"""
            ⚠️ **MARGIN TIPIS**
            - ROI: {roi_persen:.1f}% (Low)
            - Payback: {payback_months:.1f} bulan (Lama)
            - Rekomendasi: **Pertimbangkan ulang** atau optimalkan
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>📊 Analisis Bisnis Budidaya Cabai</strong></p>
    <p><small>Financial analysis & decision support</small></p>
</div>
""", unsafe_allow_html=True)
