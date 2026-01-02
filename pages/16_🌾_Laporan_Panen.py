import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from services.harvest_report_service import HarvestReportService

st.set_page_config(page_title="Laporan Panen", page_icon="🌾", layout="wide")

st.title("🌾 Laporan Panen Berjenjang")
st.markdown("**Tracking panen per periode dengan grading, berat, dan harga**")

# Initialize session state
if 'harvest_entries' not in st.session_state:
    st.session_state.harvest_entries = []

# Sidebar - Input Parameters
st.sidebar.header("⚙️ Parameter Lahan")

land_area = st.sidebar.number_input(
    "Luas Lahan (Ha)",
    min_value=0.1,
    max_value=100.0,
    value=1.0,
    step=0.1
)

total_investment = st.sidebar.number_input(
    "Total Investasi (Rp)",
    min_value=1000000,
    max_value=1000000000,
    value=50000000,
    step=1000000,
    help="Total biaya dari RAB"
)

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📝 Input Panen",
    "📊 Laporan & Analisis",
    "📈 Visualisasi"
])

# TAB 1: Input Harvest
with tab1:
    st.header("📝 Input Data Panen")
    
    # Grade info
    with st.expander("ℹ️ Informasi Grading"):
        grade_info = HarvestReportService.get_grade_info()
        
        for grade, info in grade_info.items():
            st.markdown(f"**{info['name']}**")
            st.write(f"- {info['description']}")
            st.write(f"- Harga pasar: Rp {info['typical_price_range']}/kg")
            st.markdown("---")
    
    # Input form
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        harvest_number = st.number_input(
            "Panen Ke-",
            min_value=1,
            max_value=100,
            value=len(st.session_state.harvest_entries) + 1,
            step=1,
            help="Panen keberapa (1, 2, 3, ...)"
        )
        
        harvest_date = st.date_input(
            "Tanggal Panen",
            value=datetime.now(),
            help="Tanggal melakukan panen"
        )
        
        grading = st.selectbox(
            "Grade/Kualitas",
            ['A', 'B', 'C', 'Reject'],
            help="Pilih grade sesuai kualitas"
        )
    
    with col_input2:
        weight_kg = st.number_input(
            "Berat (kg)",
            min_value=0.0,
            max_value=10000.0,
            value=0.0,
            step=0.5,
            help="Berat total panen dalam kg"
        )
        
        price_per_kg = st.number_input(
            "Harga per kg (Rp)",
            min_value=0,
            max_value=100000,
            value=25000,
            step=1000,
            help="Harga jual per kg"
        )
        
        notes = st.text_input(
            "Catatan (Opsional)",
            placeholder="Contoh: Panen pagi, cuaca cerah",
            help="Catatan tambahan"
        )
    
    # Preview
    if weight_kg > 0:
        total_value = weight_kg * price_per_kg
        
        col_prev1, col_prev2, col_prev3 = st.columns(3)
        
        with col_prev1:
            st.metric("Total Berat", f"{weight_kg} kg")
        
        with col_prev2:
            st.metric("Harga/kg", f"Rp {price_per_kg:,}")
        
        with col_prev3:
            st.metric("Total Nilai", f"Rp {total_value:,.0f}")
    
    # Save button
    if st.button("💾 Simpan Data Panen", type="primary"):
        if weight_kg > 0:
            entry = HarvestReportService.create_harvest_entry(
                harvest_number=harvest_number,
                date=harvest_date,
                grading=grading,
                weight_kg=weight_kg,
                price_per_kg=price_per_kg,
                notes=notes
            )
            
            st.session_state.harvest_entries.append(entry)
            st.success(f"✅ Data panen ke-{harvest_number} berhasil disimpan!")
            st.rerun()
        else:
            st.warning("⚠️ Masukkan berat panen terlebih dahulu!")

# TAB 2: Report & Analysis
with tab2:
    st.header("📊 Laporan & Analisis Panen")
    
    if st.session_state.harvest_entries:
        # Summary metrics
        summary = HarvestReportService.calculate_harvest_summary(st.session_state.harvest_entries)
        
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        
        with col_sum1:
            st.metric(
                "Total Panen",
                f"{summary['total_harvests']}x",
                help="Jumlah kali panen"
            )
        
        with col_sum2:
            st.metric(
                "Total Berat",
                f"{summary['total_weight']} kg",
                delta=f"{summary['avg_weight_per_harvest']} kg/panen"
            )
        
        with col_sum3:
            st.metric(
                "Total Pendapatan",
                f"Rp {summary['total_value']:,.0f}",
                help="Total nilai penjualan"
            )
        
        with col_sum4:
            st.metric(
                "Harga Rata-rata",
                f"Rp {summary['avg_price']:,.0f}/kg"
            )
        
        # Yield per hectare
        yield_per_ha = HarvestReportService.calculate_yield_per_ha(
            summary['total_weight'],
            land_area
        )
        
        st.info(f"📊 **Yield:** {yield_per_ha} ton/ha")
        
        # ROI Calculation
        roi_data = HarvestReportService.calculate_roi(
            summary['total_value'],
            total_investment
        )
        
        st.markdown("---")
        st.subheader("💰 Analisis Profitabilitas")
        
        col_roi1, col_roi2, col_roi3 = st.columns(3)
        
        with col_roi1:
            st.metric("Total Pendapatan", f"Rp {roi_data['total_revenue']:,.0f}")
        
        with col_roi2:
            st.metric("Keuntungan", f"Rp {roi_data['profit']:,.0f}")
        
        with col_roi3:
            roi_color = "normal" if roi_data['roi_percentage'] > 0 else "inverse"
            st.metric("ROI", f"{roi_data['roi_percentage']:.1f}%")
        
        # Grade distribution
        st.markdown("---")
        st.subheader("📦 Distribusi Grade")
        
        grade_dist_data = []
        for grade, data in summary['grade_distribution'].items():
            grade_dist_data.append({
                'Grade': grade,
                'Berat (kg)': round(data['weight_kg'], 2),
                'Nilai (Rp)': f"Rp {data['total_value']:,.0f}",
                'Persentase': f"{(data['weight_kg'] / summary['total_weight'] * 100):.1f}%"
            })
        
        df_grade = pd.DataFrame(grade_dist_data)
        st.dataframe(df_grade, width="stretch", hide_index=True)
        
        # Best harvest
        if summary['best_harvest']:
            st.markdown("---")
            st.subheader("🏆 Panen Terbaik")
            
            best = summary['best_harvest']
            
            col_best1, col_best2, col_best3, col_best4 = st.columns(4)
            
            with col_best1:
                st.metric("Panen Ke-", best['harvest_number'])
            
            with col_best2:
                st.metric("Tanggal", best['date'])
            
            with col_best3:
                st.metric("Berat", f"{best['weight_kg']} kg")
            
            with col_best4:
                st.metric("Nilai", f"Rp {best['total_value']:,.0f}")
        
        # Harvest table
        st.markdown("---")
        st.subheader("📋 Rincian Panen")
        
        df_harvest = pd.DataFrame(st.session_state.harvest_entries)
        df_harvest = df_harvest[['harvest_number', 'date', 'grading', 'weight_kg', 'price_per_kg', 'total_value', 'notes']]
        df_harvest.columns = ['Panen Ke', 'Tanggal', 'Grade', 'Berat (kg)', 'Harga/kg', 'Total Nilai', 'Catatan']
        
        # Format currency
        df_harvest['Harga/kg'] = df_harvest['Harga/kg'].apply(lambda x: f"Rp {x:,.0f}")
        df_harvest['Total Nilai'] = df_harvest['Total Nilai'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(df_harvest, width="stretch", hide_index=True)
        
        # Export
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            csv_data = HarvestReportService.export_harvest_report(st.session_state.harvest_entries)
            
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"laporan_panen_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col_exp2:
            if st.button("🗑️ Hapus Semua Data"):
                st.session_state.harvest_entries = []
                st.rerun()
    
    else:
        st.info("📊 Belum ada data panen. Mulai input di tab 'Input Panen'.")

# TAB 3: Visualization
with tab3:
    st.header("📈 Visualisasi Data Panen")
    
    if st.session_state.harvest_entries:
        df = pd.DataFrame(st.session_state.harvest_entries)
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Weight trend
            fig_weight = go.Figure()
            
            fig_weight.add_trace(go.Scatter(
                x=df['harvest_number'],
                y=df['weight_kg'],
                mode='lines+markers',
                name='Berat Panen',
                line=dict(color='#2ECC71', width=3),
                marker=dict(size=10),
                text=df['weight_kg'],
                textposition='top center'
            ))
            
            fig_weight.update_layout(
                title='Tren Berat Panen',
                xaxis_title='Panen Ke-',
                yaxis_title='Berat (kg)',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_weight, use_container_width=True)
        
        with col_chart2:
            # Price trend
            fig_price = go.Figure()
            
            fig_price.add_trace(go.Scatter(
                x=df['harvest_number'],
                y=df['price_per_kg'],
                mode='lines+markers',
                name='Harga/kg',
                line=dict(color='#3498DB', width=3),
                marker=dict(size=10),
                text=df['price_per_kg'],
                textposition='top center'
            ))
            
            fig_price.update_layout(
                title='Tren Harga per kg',
                xaxis_title='Panen Ke-',
                yaxis_title='Harga (Rp/kg)',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_price, use_container_width=True)
        
        # Grade distribution pie chart
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            grade_weights = df.groupby('grading')['weight_kg'].sum()
            
            fig_grade = go.Figure(data=[go.Pie(
                labels=grade_weights.index,
                values=grade_weights.values,
                hole=0.4,
                marker=dict(colors=['#2ECC71', '#F39C12', '#E74C3C', '#95A5A6'])
            )])
            
            fig_grade.update_layout(
                title='Distribusi Berat per Grade',
                height=400
            )
            
            st.plotly_chart(fig_grade, use_container_width=True)
        
        with col_chart4:
            grade_values = df.groupby('grading')['total_value'].sum()
            
            fig_value = go.Figure(data=[go.Pie(
                labels=grade_values.index,
                values=grade_values.values,
                hole=0.4,
                marker=dict(colors=['#2ECC71', '#F39C12', '#E74C3C', '#95A5A6'])
            )])
            
            fig_value.update_layout(
                title='Distribusi Nilai per Grade',
                height=400
            )
            
            st.plotly_chart(fig_value, use_container_width=True)
        
        # Cumulative revenue
        df_sorted = df.sort_values('harvest_number')
        df_sorted['cumulative_value'] = df_sorted['total_value'].cumsum()
        
        fig_cumulative = go.Figure()
        
        fig_cumulative.add_trace(go.Scatter(
            x=df_sorted['harvest_number'],
            y=df_sorted['cumulative_value'],
            mode='lines+markers',
            name='Pendapatan Kumulatif',
            line=dict(color='#9B59B6', width=3),
            marker=dict(size=10),
            fill='tozeroy'
        ))
        
        fig_cumulative.update_layout(
            title='Pendapatan Kumulatif',
            xaxis_title='Panen Ke-',
            yaxis_title='Total Pendapatan (Rp)',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_cumulative, use_container_width=True)
    
    else:
        st.info("📈 Belum ada data untuk divisualisasikan.")

# Footer
st.markdown("---")
st.info("""
**💡 Tips Pencatatan Panen:**
- Catat setiap panen secara konsisten
- Lakukan grading dengan standar yang sama
- Timbang dengan akurat
- Catat harga jual aktual
- Gunakan data untuk evaluasi dan perencanaan musim berikutnya

**🔗 Integrasi:**
- Data panen bisa digunakan untuk update Dashboard (Module 15)
- Bandingkan dengan target yield di RAB Calculator (Module 01)
- Catat di Jurnal Budidaya (Module 11)
""")
