import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from services.analytics_service import AnalyticsService
from services.database_service import DatabaseService

st.set_page_config(page_title="Advanced Analytics", page_icon="📊", layout="wide")

# Initialize database
DatabaseService.init_database()

st.title("📊 Advanced Analytics")
st.markdown("**ML-powered insights untuk keputusan budidaya berbasis data**")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Predictive Yield",
    "💰 Price Forecast",
    "💡 Cost Optimization",
    "🏆 Benchmarking",
    "📈 Seasonal Trends"
])

# TAB 1: Predictive Yield
with tab1:
    st.header("🎯 Prediksi Hasil Panen")
    
    st.info("""
    **Cara Kerja:**
    Model prediksi menggunakan data pertumbuhan, cuaca, dan input budidaya untuk memperkirakan hasil panen.
    Akurasi: ~85% berdasarkan data historis.
    """)
    
    col_input1, col_input2, col_input3 = st.columns(3)
    
    with col_input1:
        hst = st.number_input("HST (Hari Setelah Tanam)", min_value=0, max_value=200, value=120, step=1)
        avg_height = st.number_input("Tinggi Rata-rata (cm)", min_value=0.0, max_value=150.0, value=60.0, step=1.0)
    
    with col_input2:
        avg_leaves = st.number_input("Jumlah Daun Rata-rata", min_value=0, max_value=100, value=45, step=1)
        rainfall_mm = st.number_input("Total Curah Hujan (mm)", min_value=0, max_value=2000, value=500, step=10)
    
    with col_input3:
        fertilizer_kg = st.number_input("Total Pupuk (kg)", min_value=0, max_value=1000, value=300, step=10)
        pest_severity = st.slider("Tingkat Serangan Hama (%)", min_value=0, max_value=100, value=10, step=5)
    
    if st.button("🔮 Prediksi Hasil Panen", type="primary"):
        prediction = AnalyticsService.predict_yield(
            hst, avg_height, avg_leaves, rainfall_mm, fertilizer_kg, pest_severity
        )
        
        st.markdown("---")
        
        # Prediction result
        col_pred1, col_pred2, col_pred3 = st.columns(3)
        
        with col_pred1:
            st.metric(
                "Prediksi Yield",
                f"{prediction['predicted_yield']} ton/ha",
                help="Hasil panen yang diprediksi"
            )
        
        with col_pred2:
            st.metric(
                "Confidence Range",
                f"{prediction['confidence_low']} - {prediction['confidence_high']} ton/ha",
                help="Rentang kepercayaan prediksi"
            )
        
        with col_pred3:
            st.metric(
                "Akurasi Model",
                f"{prediction['accuracy']}%",
                help="Tingkat akurasi prediksi"
            )
        
        # Key factors
        st.markdown("---")
        st.subheader("📊 Faktor Kunci")
        
        for factor in prediction['factors']:
            st.markdown(f"""
            <div style='padding: 10px; background-color: {factor['color']}20; border-left: 4px solid {factor['color']}; margin: 5px 0;'>
                <b>{factor['factor']}</b>: {factor['impact']}
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 Rekomendasi")
        
        for i, rec in enumerate(prediction['recommendations'], 1):
            st.write(f"{i}. {rec}")

# TAB 2: Price Forecast
with tab2:
    st.header("💰 Prediksi Harga Pasar")
    
    st.info("""
    **Cara Kerja:**
    Analisis tren harga berdasarkan pola musiman dan kondisi pasar.
    Membantu menentukan waktu penjualan terbaik.
    """)
    
    current_price = st.number_input(
        "Harga Pasar Saat Ini (Rp/kg)",
        min_value=5000,
        max_value=100000,
        value=25000,
        step=1000
    )
    
    if st.button("📈 Forecast Harga", type="primary"):
        forecast = AnalyticsService.forecast_price(current_price)
        
        st.markdown("---")
        
        # Current and forecasts
        col_price1, col_price2, col_price3, col_price4 = st.columns(4)
        
        with col_price1:
            st.metric("Harga Saat Ini", f"Rp {forecast['current_price']:,.0f}/kg")
        
        with col_price2:
            st.metric(
                "Forecast 7 Hari",
                f"Rp {forecast['forecast_7d']:,.0f}/kg",
                delta=f"+{forecast['forecast_7d'] - forecast['current_price']:,.0f}"
            )
        
        with col_price3:
            st.metric(
                "Forecast 14 Hari",
                f"Rp {forecast['forecast_14d']:,.0f}/kg",
                delta=f"+{forecast['forecast_14d'] - forecast['current_price']:,.0f}"
            )
        
        with col_price4:
            st.metric(
                "Forecast 30 Hari",
                f"Rp {forecast['forecast_30d']:,.0f}/kg",
                delta=f"+{forecast['forecast_30d'] - forecast['current_price']:,.0f}"
            )
        
        # Trend
        st.markdown("---")
        st.markdown(f"""
        <div style='padding: 20px; background-color: {forecast['trend_color']}20; border: 2px solid {forecast['trend_color']}; border-radius: 10px; text-align: center;'>
            <h2 style='color: {forecast['trend_color']}; margin: 0;'>{forecast['trend_icon']} Trend: {forecast['trend']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Best selling time
        st.markdown("---")
        st.subheader("⏰ Waktu Jual Terbaik")
        
        st.success(f"""
        **Rekomendasi:** Jual dalam {forecast['best_selling_time']} hari  
        **Harga Prediksi:** Rp {forecast['best_price']:,.0f}/kg
        """)
        
        # Insights
        st.markdown("---")
        st.subheader("💡 Market Insights")
        
        for insight in forecast['insights']:
            st.write(f"• {insight}")
        
        # Price chart
        st.markdown("---")
        
        fig_price = go.Figure()
        
        days = [0, 7, 14, 30]
        prices = [
            forecast['current_price'],
            forecast['forecast_7d'],
            forecast['forecast_14d'],
            forecast['forecast_30d']
        ]
        
        fig_price.add_trace(go.Scatter(
            x=days,
            y=prices,
            mode='lines+markers',
            name='Harga',
            line=dict(color=forecast['trend_color'], width=3),
            marker=dict(size=10)
        ))
        
        fig_price.update_layout(
            title='Tren Harga 30 Hari',
            xaxis_title='Hari',
            yaxis_title='Harga (Rp/kg)',
            height=400
        )
        
        st.plotly_chart(fig_price, use_container_width=True)

# TAB 3: Cost Optimization
with tab3:
    st.header("💡 Optimasi Biaya Produksi")
    
    st.info("""
    **Cara Kerja:**
    Analisis breakdown biaya dan identifikasi peluang penghematan.
    Bandingkan dengan benchmark industri.
    """)
    
    # Input costs
    col_cost1, col_cost2 = st.columns(2)
    
    with col_cost1:
        total_cost = st.number_input(
            "Total Biaya Produksi (Rp)",
            min_value=1000000,
            max_value=1000000000,
            value=50000000,
            step=1000000
        )
        
        yield_ton = st.number_input(
            "Hasil Panen (ton/ha)",
            min_value=0.0,
            max_value=30.0,
            value=12.0,
            step=0.1
        )
    
    with col_cost2:
        st.write("**Breakdown Biaya:**")
        
        bibit = st.number_input("Bibit (Rp)", value=int(total_cost * 0.20), step=100000)
        pupuk = st.number_input("Pupuk (Rp)", value=int(total_cost * 0.25), step=100000)
        pestisida = st.number_input("Pestisida (Rp)", value=int(total_cost * 0.15), step=100000)
        mulsa = st.number_input("Mulsa & Ajir (Rp)", value=int(total_cost * 0.10), step=100000)
        labor = st.number_input("Tenaga Kerja (Rp)", value=int(total_cost * 0.20), step=100000)
        lainnya = st.number_input("Lain-lain (Rp)", value=int(total_cost * 0.10), step=100000)
    
    cost_breakdown = {
        'Bibit': bibit,
        'Pupuk': pupuk,
        'Pestisida': pestisida,
        'Mulsa & Ajir': mulsa,
        'Tenaga Kerja': labor,
        'Lain-lain': lainnya
    }
    
    if st.button("🔍 Analisis Efisiensi", type="primary"):
        analysis = AnalyticsService.analyze_cost_efficiency(total_cost, cost_breakdown, yield_ton)
        
        st.markdown("---")
        
        # Efficiency score
        col_eff1, col_eff2, col_eff3 = st.columns(3)
        
        with col_eff1:
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: {analysis['overall_assessment']['color']}20; border: 3px solid {analysis['overall_assessment']['color']}; border-radius: 10px;'>
                <h1 style='color: {analysis['overall_assessment']['color']}; margin: 0; font-size: 3em;'>{analysis['efficiency_score']}</h1>
                <h3 style='color: {analysis['overall_assessment']['color']}; margin: 10px 0 0 0;'>{analysis['overall_assessment']['level']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col_eff2:
            st.metric(
                "Biaya per kg",
                f"Rp {analysis['cost_per_kg']:,.0f}",
                delta=f"Benchmark: Rp {analysis['benchmark_cost_per_kg']:,.0f}",
                delta_color="inverse"
            )
        
        with col_eff3:
            st.metric(
                "Potensi Penghematan",
                f"Rp {analysis['total_savings_potential']:,.0f}",
                help="Total penghematan yang bisa dicapai"
            )
        
        st.info(analysis['overall_assessment']['message'])
        
        # Optimization opportunities
        if analysis['opportunities']:
            st.markdown("---")
            st.subheader("💰 Peluang Optimasi")
            
            for opp in analysis['opportunities']:
                with st.expander(f"💡 {opp['category']} - Hemat Rp {opp['saving']:,.0f}"):
                    st.warning(f"**Masalah:** {opp['issue']}")
                    st.write("**Tindakan yang Disarankan:**")
                    for action in opp['actions']:
                        st.write(f"• {action}")
        else:
            st.success("✅ Efisiensi biaya sudah optimal!")

# TAB 4: Benchmarking
with tab4:
    st.header("🏆 Perbandingan dengan Petani Lain")
    
    st.info("""
    **Cara Kerja:**
    Bandingkan performa Anda dengan rata-rata petani lain.
    Data di-anonymize untuk privasi.
    """)
    
    # Input farmer data
    col_bench1, col_bench2, col_bench3 = st.columns(3)
    
    with col_bench1:
        farmer_yield = st.number_input("Yield Anda (ton/ha)", min_value=0.0, max_value=30.0, value=12.0, step=0.1)
    
    with col_bench2:
        farmer_cost = st.number_input("Biaya Anda (Rp/ha)", min_value=1000000, max_value=200000000, value=50000000, step=1000000)
    
    with col_bench3:
        farmer_roi = st.number_input("ROI Anda (%)", min_value=0, max_value=500, value=120, step=5)
    
    if st.button("📊 Bandingkan Performa", type="primary"):
        farmer_data = {
            'yield': farmer_yield,
            'cost': farmer_cost,
            'roi': farmer_roi
        }
        
        benchmarks = AnalyticsService.calculate_benchmarks(farmer_data)
        
        st.markdown("---")
        
        # Overall rank
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #3498DB20; border: 3px solid #3498DB; border-radius: 10px;'>
            <h1 style='color: #3498DB; margin: 0;'>Ranking Anda: Top {100 - benchmarks['overall_rank']:.0f}%</h1>
            <p style='margin: 10px 0 0 0;'>Anda berada di percentile ke-{benchmarks['overall_rank']:.0f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed comparison
        st.markdown("---")
        st.subheader("📊 Perbandingan Detail")
        
        for comp in benchmarks['comparison']:
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            with col_c1:
                st.write(f"**{comp['metric']}**")
            
            with col_c2:
                st.write(f"Anda: {comp['value']}")
            
            with col_c3:
                st.write(f"Rata-rata: {comp['average']}")
            
            with col_c4:
                st.markdown(f"<span style='color: {comp['color']}; font-weight: bold;'>{comp['difference']}</span>", unsafe_allow_html=True)
        
        # Best practices
        st.markdown("---")
        st.subheader("💡 Best Practices dari Top Performers")
        
        for practice in benchmarks['best_practices']:
            st.write(f"• {practice}")

# TAB 5: Seasonal Trends
with tab5:
    st.header("📈 Analisis Tren Musiman")
    
    st.info("""
    **Cara Kerja:**
    Analisis performa across multiple musim tanam.
    Identifikasi pola dan forecast musim berikutnya.
    """)
    
    # Input seasonal data
    st.subheader("📝 Input Data Musim Tanam")
    
    num_seasons = st.number_input("Jumlah Musim", min_value=2, max_value=10, value=3, step=1)
    
    seasons_data = []
    
    for i in range(num_seasons):
        with st.expander(f"Musim {i+1}"):
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                s_yield = st.number_input(f"Yield (ton/ha)", min_value=0.0, max_value=30.0, value=10.0 + i, step=0.1, key=f"yield_{i}")
            
            with col_s2:
                s_cost = st.number_input(f"Biaya (Rp)", min_value=1000000, max_value=200000000, value=45000000 + (i * 2000000), step=1000000, key=f"cost_{i}")
            
            with col_s3:
                s_roi = st.number_input(f"ROI (%)", min_value=0, max_value=500, value=100 + (i * 5), step=5, key=f"roi_{i}")
            
            seasons_data.append({
                'season': i + 1,
                'yield': s_yield,
                'cost': s_cost,
                'roi': s_roi
            })
    
    if st.button("📊 Analisis Tren", type="primary"):
        trends = AnalyticsService.analyze_seasonal_trends(seasons_data)
        
        if trends.get('insufficient_data'):
            st.warning(trends['message'])
        else:
            st.markdown("---")
            
            # Trends summary
            col_trend1, col_trend2, col_trend3 = st.columns(3)
            
            with col_trend1:
                st.metric(
                    "Tren Yield",
                    f"{trends['yield_trend']['icon']} {trends['yield_trend']['growth']:+.1f}%",
                    help="Year-over-year growth"
                )
            
            with col_trend2:
                st.metric(
                    "Tren Biaya",
                    f"{trends['cost_trend']['icon']} {trends['cost_trend']['growth']:+.1f}%",
                    help="Year-over-year growth"
                )
            
            with col_trend3:
                st.metric(
                    "Tren ROI",
                    f"{trends['roi_trend']['icon']} {trends['roi_trend']['growth']:+.1f}%",
                    help="Year-over-year growth"
                )
            
            # Forecast
            st.markdown("---")
            st.subheader("🔮 Forecast Musim Berikutnya")
            
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                st.metric("Prediksi Yield", f"{trends['forecast']['yield']} ton/ha")
            
            with col_f2:
                st.metric("Prediksi Biaya", f"Rp {trends['forecast']['cost']:,.0f}")
            
            with col_f3:
                st.metric("Prediksi ROI", f"{trends['forecast']['roi']}%")
            
            # Insights
            st.markdown("---")
            st.subheader("💡 Insights")
            
            for insight in trends['insights']:
                st.write(f"{insight}")
            
            # Trend chart
            st.markdown("---")
            
            df_seasons = pd.DataFrame(seasons_data)
            
            fig_trends = go.Figure()
            
            fig_trends.add_trace(go.Scatter(
                x=df_seasons['season'],
                y=df_seasons['yield'],
                mode='lines+markers',
                name='Yield (ton/ha)',
                line=dict(color='#2ECC71', width=3),
                marker=dict(size=10)
            ))
            
            fig_trends.update_layout(
                title='Tren Yield Across Seasons',
                xaxis_title='Musim',
                yaxis_title='Yield (ton/ha)',
                height=400
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)

# Footer
st.markdown("---")
st.info("""
**💡 Tips Menggunakan Advanced Analytics:**
- Update data secara berkala untuk prediksi lebih akurat
- Gunakan insights untuk perencanaan musim berikutnya
- Bandingkan performa dengan benchmark untuk improvement
- Kombinasikan dengan Module lain untuk hasil optimal

**🔗 Integration:**
- Module 10: Data pertumbuhan untuk prediksi yield
- Module 11: Data biaya untuk optimasi
- Module 16: Data panen untuk benchmarking
- Module 17: Export data untuk analisis eksternal
""")
