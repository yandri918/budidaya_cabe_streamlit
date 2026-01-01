import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.spraying_strategy_service import SprayingStrategyService
from data.pesticide_database import PESTICIDE_DATABASE, SPRAY_SCHEDULE

st.set_page_config(page_title="Strategi Penyemprotan", page_icon="💦", layout="wide")

st.title("💦 Strategi Penyemprotan Cabai")
st.markdown("**Panduan lengkap penyemprotan: jadwal, dosis, rotasi, dan analisis biaya**")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Jadwal Spray",
    "🧮 Kalkulator Dosis",
    "🔄 Rotasi Pestisida",
    "📚 Database Pestisida",
    "💰 Analisis Biaya"
])

# TAB 1: Spray Schedule
with tab1:
    st.header("📅 Jadwal Penyemprotan per Fase")
    
    st.info("""
    **💡 Tips Penyemprotan:**
    - Semprot pagi (06:00-09:00) atau sore (16:00-18:00)
    - Hindari saat hujan atau angin kencang
    - Gunakan APD lengkap (masker, sarung tangan, baju lengan panjang)
    - Perhatikan PHI (Pre-Harvest Interval) menjelang panen
    """)
    
    # Select growth phase
    phase = st.selectbox(
        "Pilih Fase Pertumbuhan",
        list(SPRAY_SCHEDULE.keys())
    )
    
    schedule = SprayingStrategyService.get_spray_schedule(phase)
    
    if schedule:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Frekuensi Spray", schedule['frequency'])
            st.caption(f"**Fokus:** {schedule['focus']}")
        
        with col2:
            st.markdown("### Rekomendasi Penyemprotan")
            
            for rec in schedule['recommended']:
                with st.expander(f"📍 Minggu {rec['week']} - {rec['target']}"):
                    st.write(f"**Pestisida:** {', '.join(rec['pesticides'])}")
                    st.write(f"**Target:** {rec['target']}")
                    st.write(f"**Metode:** {rec['method']}")
                    if 'note' in rec:
                        st.warning(f"⚠️ {rec['note']}")
        
        # Timeline visualization
        st.markdown("---")
        st.subheader("📊 Timeline Penyemprotan")
        
        # Create timeline data
        timeline_data = []
        for rec in schedule['recommended']:
            week_str = str(rec['week'])
            if '-' in week_str:
                weeks = week_str.split('-')
                for w in range(int(weeks[0]), int(weeks[1]) + 1):
                    timeline_data.append({
                        'Minggu': w,
                        'Pestisida': ', '.join(rec['pesticides'][:2]),  # First 2
                        'Target': rec['target']
                    })
            else:
                timeline_data.append({
                    'Minggu': int(week_str),
                    'Pestisida': ', '.join(rec['pesticides'][:2]),
                    'Target': rec['target']
                })
        
        if timeline_data:
            df_timeline = pd.DataFrame(timeline_data)
            st.dataframe(df_timeline, use_container_width=True, hide_index=True)

# TAB 2: Dosage Calculator
with tab2:
    st.header("🧮 Kalkulator Dosis Pestisida")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("Input Lahan")
        
        luas_m2 = st.number_input(
            "Luas Lahan (m²)",
            min_value=100,
            max_value=100000,
            value=10000,
            step=1000,
            help="1 Ha = 10,000 m²"
        )
        
        luas_ha = luas_m2 / 10000
        st.caption(f"= {luas_ha:.2f} Ha")
        
        tank_capacity = st.number_input(
            "Kapasitas Tangki (Liter)",
            min_value=5,
            max_value=100,
            value=16,
            step=1,
            help="Kapasitas tangki semprot (standar 16L)"
        )
        
        method = st.radio(
            "Metode Aplikasi",
            ["Semprot (Foliar)", "Kocor (Drench)"],
            help="Semprot untuk daun, Kocor untuk tanah/akar"
        )
        
        application_method = "Semprot" if "Semprot" in method else "Kocor"
    
    with col_input2:
        st.subheader("Pilih Pestisida")
        
        # Group pesticides by type
        grouped = SprayingStrategyService.get_all_pesticides()
        
        pesticide_type = st.selectbox(
            "Tipe Pestisida",
            list(grouped.keys())
        )
        
        pesticide_name = st.selectbox(
            "Nama Pestisida",
            grouped[pesticide_type]
        )
        
        # Show pesticide info
        pest_info = PESTICIDE_DATABASE[pesticide_name]
        
        st.info(f"""
        **{pest_info['active_ingredient']}**
        - Mode: {pest_info['mode_of_action']}
        - Target: {', '.join(pest_info.get('target_pests', pest_info.get('target_diseases', [])))}
        - PHI: {pest_info['phi_days']} hari
        - Kelas: {pest_info['safety_class']}
        """)
    
    # Calculate button
    if st.button("🧮 Hitung Dosis", type="primary"):
        result = SprayingStrategyService.calculate_dosage(
            pesticide_name,
            luas_m2,
            tank_capacity,
            application_method
        )
        
        if result:
            st.markdown("---")
            st.subheader("📊 Hasil Perhitungan")
            
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            
            with col_r1:
                st.metric(
                    "Total Air",
                    f"{result['total_water_L']:.1f} L",
                    help="Total volume air yang dibutuhkan"
                )
            
            with col_r2:
                st.metric(
                    "Total Pestisida",
                    f"{result['total_pesticide']:.1f} {result['unit']}",
                    help="Total pestisida yang dibutuhkan"
                )
            
            with col_r3:
                st.metric(
                    "Jumlah Tangki",
                    f"{result['num_tanks']:.1f} tangki",
                    help=f"Dengan kapasitas {tank_capacity}L per tangki"
                )
            
            with col_r4:
                st.metric(
                    "Biaya",
                    f"Rp {result['cost']:,.0f}",
                    help="Estimasi biaya pestisida"
                )
            
            # Detailed breakdown
            with st.expander("📋 Rincian Detail"):
                st.markdown(f"""
                **Dosis per Tangki:**
                - Air: {tank_capacity} L
                - Pestisida: {result['pesticide_per_tank']:.2f} {result['unit']}
                - Konsentrasi: {result['dosage_per_liter']} {result['unit']}/L
                
                **Total untuk {luas_ha:.2f} Ha:**
                - Total air: {result['total_water_L']:.1f} L
                - Total pestisida: {result['total_pesticide']:.1f} {result['unit']}
                - Jumlah tangki: {result['num_tanks']:.1f} tangki
                
                **Biaya:**
                - Total: Rp {result['cost']:,.0f}
                - Per Ha: Rp {result['cost_per_ha']:,.0f}
                - Per tangki: Rp {result['cost'] / result['num_tanks']:,.0f}
                """)
            
            # Safety reminder
            st.warning(f"""
            ⚠️ **Perhatian Keamanan:**
            - Gunakan APD lengkap (masker, sarung tangan, baju lengan panjang)
            - Kelas bahaya: {pest_info['safety_class']}
            - PHI: {pest_info['phi_days']} hari (jangan panen sebelum {pest_info['phi_days']} hari setelah spray)
            - Interval aplikasi: {pest_info['application_interval']}
            """)

# TAB 3: Pesticide Rotation
with tab3:
    st.header("🔄 Rotasi Pestisida")
    
    st.info("""
    **Mengapa Rotasi Penting?**
    - Mencegah resistensi hama/penyakit
    - Meningkatkan efektivitas pengendalian
    - Mengurangi risiko kegagalan
    - Menjaga keseimbangan ekosistem
    """)
    
    weeks = st.slider(
        "Rencanakan untuk berapa minggu?",
        min_value=4,
        max_value=20,
        value=8,
        step=1
    )
    
    rotation_plan = SprayingStrategyService.get_rotation_plan(weeks)
    
    st.subheader(f"📅 Rencana Rotasi {weeks} Minggu")
    
    # Display as table
    rotation_data = []
    for plan in rotation_plan:
        rotation_data.append({
            'Minggu': plan['week'],
            'Grup Insektisida': plan['insecticide_group'],
            'Rekomendasi Insektisida': ', '.join(plan['recommended_insecticides']),
            'Grup Fungisida': plan['fungicide_group'],
            'Rekomendasi Fungisida': ', '.join(plan['recommended_fungicides'])
        })
    
    df_rotation = pd.DataFrame(rotation_data)
    st.dataframe(df_rotation, use_container_width=True, hide_index=True)
    
    # Visualization
    st.markdown("---")
    st.subheader("📊 Visualisasi Rotasi")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        # Insecticide rotation
        insect_groups = [p['insecticide_group'] for p in rotation_plan]
        fig_insect = px.bar(
            x=list(range(1, weeks + 1)),
            y=[1] * weeks,
            color=insect_groups,
            title="Rotasi Insektisida",
            labels={'x': 'Minggu', 'y': '', 'color': 'Grup'},
            height=300
        )
        fig_insect.update_layout(showlegend=True, yaxis_visible=False)
        st.plotly_chart(fig_insect, use_container_width=True)
    
    with col_v2:
        # Fungicide rotation
        fungi_groups = [p['fungicide_group'] for p in rotation_plan]
        fig_fungi = px.bar(
            x=list(range(1, weeks + 1)),
            y=[1] * weeks,
            color=fungi_groups,
            title="Rotasi Fungisida",
            labels={'x': 'Minggu', 'y': '', 'color': 'Grup'},
            height=300
        )
        fig_fungi.update_layout(showlegend=True, yaxis_visible=False)
        st.plotly_chart(fig_fungi, use_container_width=True)

# TAB 4: Pesticide Database
with tab4:
    st.header("📚 Database Pestisida")
    
    # Filter by type
    filter_type = st.multiselect(
        "Filter by Type",
        ["Insektisida", "Fungisida", "Bakterisida", "Organik"],
        default=["Insektisida", "Fungisida"]
    )
    
    # Display pesticides
    for name, data in PESTICIDE_DATABASE.items():
        pest_type = data['type']
        
        # Check if matches filter
        show = False
        for f in filter_type:
            if f in pest_type or (f == "Organik" and ("Organik" in pest_type or "Bio" in pest_type)):
                show = True
                break
        
        if show:
            with st.expander(f"🧪 {name} - {data['type']}"):
                col_db1, col_db2 = st.columns(2)
                
                with col_db1:
                    st.markdown(f"""
                    **Bahan Aktif:** {data['active_ingredient']}
                    
                    **Mode of Action:** {data['mode_of_action']}
                    
                    **Target:**
                    """)
                    targets = data.get('target_pests', data.get('target_diseases', []))
                    for target in targets:
                        st.write(f"- {target}")
                
                with col_db2:
                    st.markdown(f"""
                    **Dosis:** {data.get('dosage_range', 'N/A')}
                    
                    **PHI:** {data['phi_days']} hari
                    
                    **Interval:** {data['application_interval']}
                    
                    **Kelas Bahaya:** {data['safety_class']}
                    
                    **Harga:** Rp {data.get('price_per_liter', data.get('price_per_kg', 0)):,.0f}
                    """)
                
                if data.get('notes'):
                    st.info(f"💡 {data['notes']}")

# TAB 5: Cost Analysis
with tab5:
    st.header("💰 Analisis Biaya Penyemprotan")
    
    col_cost1, col_cost2 = st.columns(2)
    
    with col_cost1:
        land_area_ha = st.number_input(
            "Luas Lahan (Ha)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1
        )
        
        spray_freq = st.number_input(
            "Frekuensi Spray per Bulan",
            min_value=1,
            max_value=8,
            value=4,
            step=1,
            help="Rata-rata: 4x per bulan (1x seminggu)"
        )
    
    with col_cost2:
        cost_per_spray = st.number_input(
            "Biaya per Spray per Ha (Rp)",
            min_value=50000,
            max_value=500000,
            value=150000,
            step=10000,
            help="Estimasi biaya pestisida per aplikasi per hektar"
        )
    
    # Calculate
    cost_analysis = SprayingStrategyService.calculate_monthly_cost(
        land_area_ha,
        spray_freq,
        cost_per_spray
    )
    
    st.markdown("---")
    st.subheader("📊 Hasil Analisis Biaya")
    
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    
    with col_a1:
        st.metric(
            "Per Spray",
            f"Rp {cost_analysis['cost_per_spray_total']:,.0f}"
        )
    
    with col_a2:
        st.metric(
            "Per Bulan",
            f"Rp {cost_analysis['cost_per_month']:,.0f}"
        )
    
    with col_a3:
        st.metric(
            "Per Siklus (5 bulan)",
            f"Rp {cost_analysis['cost_per_cycle']:,.0f}"
        )
    
    with col_a4:
        st.metric(
            "Per Tahun",
            f"Rp {cost_analysis['cost_per_year']:,.0f}"
        )
    
    # Chart
    st.markdown("---")
    st.subheader("📈 Proyeksi Biaya")
    
    months = list(range(1, 13))
    cumulative_cost = [cost_analysis['cost_per_month'] * m for m in months]
    
    fig_cost = go.Figure()
    fig_cost.add_trace(go.Scatter(
        x=months,
        y=cumulative_cost,
        mode='lines+markers',
        name='Biaya Kumulatif',
        line=dict(color='#FF6B6B', width=3)
    ))
    
    fig_cost.update_layout(
        title='Proyeksi Biaya Penyemprotan per Bulan',
        xaxis_title='Bulan',
        yaxis_title='Biaya Kumulatif (Rp)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_cost, use_container_width=True)
    
    # Breakdown
    with st.expander("📋 Breakdown Detail"):
        st.markdown(f"""
        **Asumsi:**
        - Luas lahan: {land_area_ha} Ha
        - Frekuensi spray: {spray_freq}x per bulan
        - Biaya per spray per Ha: Rp {cost_per_spray:,.0f}
        
        **Perhitungan:**
        - Biaya per spray total: {land_area_ha} Ha × Rp {cost_per_spray:,.0f} = Rp {cost_analysis['cost_per_spray_total']:,.0f}
        - Biaya per bulan: {spray_freq}x × Rp {cost_analysis['cost_per_spray_total']:,.0f} = Rp {cost_analysis['cost_per_month']:,.0f}
        - Biaya per siklus (5 bulan): 5 × Rp {cost_analysis['cost_per_month']:,.0f} = Rp {cost_analysis['cost_per_cycle']:,.0f}
        - Biaya per tahun: 12 × Rp {cost_analysis['cost_per_month']:,.0f} = Rp {cost_analysis['cost_per_year']:,.0f}
        
        **Tips Hemat:**
        - Gunakan pestisida organik untuk aplikasi rutin
        - Rotasi dengan biopestisida (lebih murah)
        - Aplikasi preventif lebih murah dari kuratif
        - Monitoring rutin untuk deteksi dini
        """)

# Footer
st.markdown("---")
st.info("""
**💡 Tips Penting:**
- Selalu baca label pestisida sebelum aplikasi
- Gunakan APD lengkap untuk keselamatan
- Perhatikan PHI (Pre-Harvest Interval) menjelang panen
- Rotasi pestisida untuk mencegah resistensi
- Simpan pestisida di tempat aman, jauh dari jangkauan anak-anak
- Buang kemasan bekas pestisida dengan benar
""")
