import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from services.growth_monitoring_service import GrowthMonitoringService
from services.database_service import DatabaseService
from data.growth_milestones import GROWTH_MILESTONES

st.set_page_config(page_title="Pantau Pertumbuhan", page_icon="📈", layout="wide")

# Initialize database
DatabaseService.init_database()

st.title("📈 Pantau Pertumbuhan Cabai")
st.markdown("**Track pertumbuhan tanaman dan bandingkan dengan milestone SOP**")

# Load from database on first run
if 'measurements' not in st.session_state:
    db_records = DatabaseService.get_growth_records()
    # Convert to measurements format
    st.session_state.measurements = [
        {
            'date': r['created_at'][:10] if r.get('created_at') else r.get('planting_date', ''),
            'hst': r.get('hst', 0),
            'height': r.get('height_cm', 0),
            'leaves': r.get('leaf_count', 0),
            'notes': r.get('notes', '')
        }
        for r in db_records
    ]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Input & Tracking",
    "📅 Timeline Milestone",
    "💚 Health Assessment",
    "📈 Growth Charts"
])

# TAB 1: Input & Tracking
with tab1:
    st.header("📊 Input Pengukuran")
    
    col_date1, col_date2 = st.columns(2)
    
    with col_date1:
        planting_date = st.date_input(
            "Tanggal Tanam",
            value=datetime.now() - timedelta(days=30),
            help="Kapan bibit ditanam di lahan"
        )
    
    with col_date2:
        current_hst = GrowthMonitoringService.calculate_hst(planting_date)
        st.metric("HST (Hari Setelah Tanam)", f"{current_hst} hari")
        
        current_phase = GrowthMonitoringService.get_current_milestone(current_hst)
        if current_phase:
            st.caption(f"**Fase:** {current_phase['phase']}")
    
    st.markdown("---")
    
    # Measurement input
    st.subheader("📏 Pengukuran Hari Ini")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        height = st.number_input(
            "Tinggi Tanaman (cm)",
            min_value=0.0,
            max_value=200.0,
            value=50.0,
            step=1.0
        )
    
    with col_m2:
        leaves = st.number_input(
            "Jumlah Daun",
            min_value=0,
            max_value=200,
            value=30,
            step=1
        )
    
    with col_m3:
        notes = st.text_area(
            "Catatan",
            placeholder="Kondisi tanaman, observasi, dll",
            height=100
        )
    
    if st.button("💾 Simpan Pengukuran", type="primary"):
        measurement = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'hst': current_hst,
            'height': height,
            'leaves': leaves,
            'notes': notes
        }
        
        # Save to database
        growth_data = {
            'farmer_name': st.session_state.get('farmer_name', 'Default'),
            'planting_date': planting_date.strftime("%Y-%m-%d"),
            'hst': current_hst,
            'height_cm': height,
            'leaf_count': leaves,
            'health_score': 0,  # Can be updated from health assessment
            'notes': notes
        }
        DatabaseService.save_growth_record(growth_data)
        
        # Also keep in session state
        st.session_state.measurements.append(measurement)
        st.success("✅ Pengukuran tersimpan ke database!")
    
    # Compare with milestone
    if current_hst > 0:
        st.markdown("---")
        st.subheader("🎯 Perbandingan dengan Milestone")
        
        comparison = GrowthMonitoringService.compare_with_milestone(
            current_hst,
            height,
            leaves
        )
        
        if comparison:
            # Status badge
            st.markdown(f"""
            <div style='padding: 10px; background-color: {comparison['status_color']}20; border-left: 4px solid {comparison['status_color']}; border-radius: 5px;'>
                <h3 style='color: {comparison['status_color']}; margin: 0;'>{comparison['status']}</h3>
                <p style='margin: 5px 0 0 0;'>{comparison['milestone_event']} - {comparison['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.metric(
                    "Tinggi Tanaman",
                    f"{comparison['actual_height']} cm",
                    delta=f"{comparison['height_diff']:+.0f} cm ({comparison['height_pct']:+.1f}%)",
                    help=f"Target: {comparison['expected_height']} cm"
                )
            
            with col_c2:
                st.metric(
                    "Jumlah Daun",
                    f"{comparison['actual_leaves']} helai",
                    delta=f"{comparison['leaves_diff']:+.0f} helai ({comparison['leaves_pct']:+.1f}%)",
                    help=f"Target: {comparison['expected_leaves']} helai"
                )
            
            # Recommended actions
            with st.expander("📋 Tindakan yang Disarankan"):
                for action in comparison['actions']:
                    st.write(f"- {action}")
    
    # Show saved measurements
    if st.session_state.measurements:
        st.markdown("---")
        st.subheader("📝 Riwayat Pengukuran")
        
        df_measurements = pd.DataFrame(st.session_state.measurements)
        st.dataframe(df_measurements, use_container_width=True, hide_index=True)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔄 Reload dari Database"):
                db_records = DatabaseService.get_growth_records()
                st.session_state.measurements = [
                    {
                        'date': r['created_at'][:10] if r.get('created_at') else r.get('planting_date', ''),
                        'hst': r.get('hst', 0),
                        'height': r.get('height_cm', 0),
                        'leaves': r.get('leaf_count', 0),
                        'notes': r.get('notes', '')
                    }
                    for r in db_records
                ]
                st.success("✅ Data berhasil di-reload dari database!")
                st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Hapus dari Session"):
                st.session_state.measurements = []
                st.rerun()

# TAB 2: Timeline Milestone
with tab2:
    st.header("📅 Timeline Milestone Pertumbuhan")
    
    if planting_date:
        timeline = GrowthMonitoringService.generate_growth_timeline(
            planting_date,
            current_hst
        )
        
        # Display as timeline
        for item in timeline:
            col_t1, col_t2 = st.columns([1, 3])
            
            with col_t1:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; background-color: {item['status_color']}20; border-radius: 5px;'>
                    <h3 style='margin: 0; color: {item['status_color']};'>HST {item['hst']}</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9em;'>{item['date']}</p>
                    <span style='background-color: {item['status_color']}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>{item['status']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_t2:
                with st.expander(f"📍 {item['event']} - {item['phase']}"):
                    st.write(f"**Deskripsi:** {item['description']}")
                    st.write(f"**Target Tinggi:** {item['expected_height']} cm")
                    st.write(f"**Target Daun:** {item['expected_leaves']} helai")
                    st.write("**Tindakan:**")
                    for action in item['actions']:
                        st.write(f"- {action}")
            
            st.markdown("")

# TAB 3: Health Assessment
with tab3:
    st.header("💚 Penilaian Kesehatan Tanaman")
    
    st.info("""
    **Cara Penilaian:**
    Berikan skor 1-5 untuk setiap kriteria berdasarkan observasi visual.
    Sistem akan menghitung health score dan memberikan rekomendasi.
    """)
    
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        leaf_color = st.select_slider(
            "Warna Daun",
            options=[1, 2, 3, 4, 5],
            value=4,
            format_func=lambda x: ["Kuning Kering", "Kuning Pucat", "Hijau Pucat", "Hijau Normal", "Hijau Tua"][x-1]
        )
        
        stem_strength = st.select_slider(
            "Kekuatan Batang",
            options=[1, 2, 3, 4, 5],
            value=4,
            format_func=lambda x: ["Sangat Lemah", "Lemah", "Cukup", "Kuat", "Sangat Kuat"][x-1]
        )
    
    with col_h2:
        pest_severity = st.slider(
            "Tingkat Serangan Hama/Penyakit (%)",
            min_value=0,
            max_value=100,
            value=5,
            step=5
        )
        
        growth_rate = st.select_slider(
            "Laju Pertumbuhan",
            options=[1, 2, 3, 4, 5],
            value=4,
            format_func=lambda x: ["Terhenti", "Sangat Lambat", "Lambat", "Normal", "Cepat"][x-1]
        )
    
    if st.button("🔍 Analisis Kesehatan", type="primary"):
        health = GrowthMonitoringService.assess_health(
            leaf_color,
            stem_strength,
            pest_severity,
            growth_rate
        )
        
        st.markdown("---")
        
        # Health score display
        col_score1, col_score2 = st.columns([1, 2])
        
        with col_score1:
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: {health['color']}20; border: 3px solid {health['color']}; border-radius: 10px;'>
                <h1 style='color: {health['color']}; margin: 0; font-size: 3em;'>{health['score']}</h1>
                <h3 style='color: {health['color']}; margin: 10px 0 0 0;'>{health['category']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col_score2:
            st.markdown("**Indikator:**")
            for indicator in health['indicators']:
                st.write(f"✓ {indicator}")
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 Rekomendasi Tindakan")
        
        for i, rec in enumerate(health['recommendations'], 1):
            st.write(f"{i}. {rec}")

# TAB 4: Growth Charts
with tab4:
    st.header("📈 Grafik Pertumbuhan")
    
    if len(st.session_state.measurements) >= 2:
        df_chart = pd.DataFrame(st.session_state.measurements)
        
        # Height chart
        fig_height = go.Figure()
        
        fig_height.add_trace(go.Scatter(
            x=df_chart['hst'],
            y=df_chart['height'],
            mode='lines+markers',
            name='Tinggi Aktual',
            line=dict(color='#3498DB', width=3),
            marker=dict(size=8)
        ))
        
        # Add milestone expectations
        milestones_data = []
        for phase, data in GROWTH_MILESTONES.items():
            for m in data['milestones']:
                milestones_data.append({
                    'hst': m['hst'],
                    'height': m['expected_height_cm']
                })
        
        df_milestones = pd.DataFrame(milestones_data)
        
        fig_height.add_trace(go.Scatter(
            x=df_milestones['hst'],
            y=df_milestones['height'],
            mode='lines+markers',
            name='Target Milestone',
            line=dict(color='#E74C3C', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig_height.update_layout(
            title='Pertumbuhan Tinggi Tanaman',
            xaxis_title='HST (Hari Setelah Tanam)',
            yaxis_title='Tinggi (cm)',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_height, use_container_width=True)
        
        # Leaves chart
        fig_leaves = go.Figure()
        
        fig_leaves.add_trace(go.Scatter(
            x=df_chart['hst'],
            y=df_chart['leaves'],
            mode='lines+markers',
            name='Jumlah Daun Aktual',
            line=dict(color='#2ECC71', width=3),
            marker=dict(size=8)
        ))
        
        # Add milestone expectations for leaves
        df_milestones['leaves'] = [m['expected_leaves'] for phase in GROWTH_MILESTONES.values() for m in phase['milestones']]
        
        fig_leaves.add_trace(go.Scatter(
            x=df_milestones['hst'],
            y=df_milestones['leaves'],
            mode='lines+markers',
            name='Target Milestone',
            line=dict(color='#E74C3C', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig_leaves.update_layout(
            title='Pertumbuhan Jumlah Daun',
            xaxis_title='HST (Hari Setelah Tanam)',
            yaxis_title='Jumlah Daun',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_leaves, use_container_width=True)
        
        # Growth rate
        growth_rate_data = GrowthMonitoringService.calculate_growth_rate(
            st.session_state.measurements
        )
        
        if growth_rate_data:
            st.markdown("---")
            st.subheader("📊 Laju Pertumbuhan")
            
            col_gr1, col_gr2, col_gr3 = st.columns(3)
            
            with col_gr1:
                st.metric(
                    "Periode Pengamatan",
                    f"{growth_rate_data['period_days']} hari"
                )
            
            with col_gr2:
                st.metric(
                    "Laju Tinggi",
                    f"{growth_rate_data['height_rate_cm_per_day']:.2f} cm/hari",
                    delta=f"Total: {growth_rate_data['total_height_growth']:.0f} cm"
                )
            
            with col_gr3:
                st.metric(
                    "Laju Daun",
                    f"{growth_rate_data['leaves_rate_per_day']:.2f} helai/hari",
                    delta=f"Total: {growth_rate_data['total_leaves_growth']:.0f} helai"
                )
    
    else:
        st.info("📊 Minimal 2 pengukuran diperlukan untuk menampilkan grafik. Silakan input pengukuran di tab 'Input & Tracking'.")

# Footer
st.markdown("---")
st.info("""
**💡 Tips Monitoring:**
- Ukur tanaman secara konsisten (waktu & metode yang sama)
- Catat pengukuran minimal 1x seminggu
- Foto tanaman untuk dokumentasi visual
- Bandingkan dengan milestone untuk deteksi dini masalah
- Gunakan data untuk evaluasi dan perbaikan budidaya
""")
