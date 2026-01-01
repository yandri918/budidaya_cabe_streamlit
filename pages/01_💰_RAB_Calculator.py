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
tab1, tab2, tab3, tab4 = st.tabs([
    "🧮 Kalkulator Teknis",
    "📊 Perbandingan Skenario",
    "💵 Hitung RAB Detail",
    "📈 Analisis ROI"
])

with tab1:
    st.header("🧮 Kalkulator Teknis")
    st.markdown("**Hitung kebutuhan bibit, jarak tanam, dan panjang mulsa**")
    
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Input Lahan")
        
        luas_m2 = st.number_input(
            "Luas Lahan (m²)",
            min_value=100,
            max_value=1000000,
            value=10000,
            step=100,
            help="1 Ha = 10,000 m²"
        )
        
        luas_ha_calc = luas_m2 / 10000
        st.info(f"= {luas_ha_calc:.2f} Ha")
        
        panjang_bedengan = st.number_input(
            "Panjang Bedengan (m)",
            min_value=1,
            max_value=1000,
            value=50,
            step=1
        )
        
        lebar_bedengan = st.number_input(
            "Lebar Bedengan (m)",
            min_value=0.5,
            max_value=5.0,
            value=1.2,
            step=0.1,
            help="Standar: 1.0 - 1.2 m"
        )
    
    with col2:
        st.subheader("🌱 Jarak Tanam")
        
        jarak_dalam_baris = st.number_input(
            "Jarak Dalam Baris (cm)",
            min_value=20,
            max_value=100,
            value=60,
            step=5,
            help="Jarak antar tanaman dalam 1 baris"
        )
        
        jarak_antar_baris = st.number_input(
            "Jarak Antar Baris (cm)",
            min_value=20,
            max_value=100,
            value=70,
            step=5,
            help="Jarak antar baris tanaman"
        )
        
        jumlah_baris = st.number_input(
            "Jumlah Baris per Bedengan",
            min_value=1,
            max_value=5,
            value=2,
            step=1,
            help="Biasanya 2 baris untuk bedengan 1-1.2m"
        )
    
    # Intercropping section
    st.markdown("---")
    st.subheader("🌾 Tumpang Sari (Opsional)")
    
    use_intercrop = st.checkbox(
        "Gunakan Tumpang Sari",
        help="Tanam tanaman sela di tengah baris untuk optimasi lahan"
    )
    
    intercrop_type = None
    intercrop_spacing = 0
    intercrop_price = 0
    
    if use_intercrop:
        col_ic1, col_ic2 = st.columns(2)
        
        with col_ic1:
            intercrop_type = st.selectbox(
                "Pilih Tanaman Sela",
                ["Kobis", "Bawang Daun", "Jagung Manis", "Tomat"],
                help="Tanaman yang ditanam di tengah baris cabai"
            )
            
            # Default spacing based on crop type
            default_spacing = {
                "Kobis": 40,
                "Bawang Daun": 20,
                "Jagung Manis": 30,
                "Tomat": 50
            }
            
            intercrop_spacing = st.number_input(
                f"Jarak Tanam {intercrop_type} (cm)",
                min_value=15,
                max_value=60,
                value=default_spacing.get(intercrop_type, 30),
                step=5,
                help="Jarak antar tanaman sela"
            )
        
        with col_ic2:
            # Default prices
            default_prices = {
                "Kobis": 300,
                "Bawang Daun": 200,
                "Jagung Manis": 500,
                "Tomat": 400
            }
            
            intercrop_price = st.number_input(
                f"Harga Bibit {intercrop_type} (Rp/batang)",
                min_value=100,
                max_value=2000,
                value=default_prices.get(intercrop_type, 300),
                step=50
            )
            
            st.info(f"""
            **Info {intercrop_type}:**
            - Umur panen: {"60-90 hari" if intercrop_type == "Kobis" else "45-60 hari" if intercrop_type == "Bawang Daun" else "70-90 hari" if intercrop_type == "Jagung Manis" else "80-100 hari"}
            - Cocok untuk: Fase vegetatif cabai
            - Manfaat: Optimasi lahan, tambahan income
            """)
    
    
    if st.button("🧮 Hitung", type="primary"):
        st.markdown("---")
        st.subheader("📊 Hasil Perhitungan")
        
        # Calculate seedling count
        jarak_dalam_m = jarak_dalam_baris / 100
        jarak_antar_m = jarak_antar_baris / 100
        
        # Tanaman per bedengan
        tanaman_per_baris = int(panjang_bedengan / jarak_dalam_m)
        tanaman_per_bedengan = tanaman_per_baris * jumlah_baris
        
        # Total bedengan
        jarak_antar_bedengan = 0.5  # meter (standar)
        lebar_total_per_bedengan = lebar_bedengan + jarak_antar_bedengan
        
        jumlah_bedengan = int(luas_m2 / (panjang_bedengan * lebar_total_per_bedengan))
        
        # Total tanaman
        total_tanaman = tanaman_per_bedengan * jumlah_bedengan
        
        # Populasi per ha
        populasi_per_ha = int((10000 / (jarak_dalam_m * jarak_antar_m)))
        
        # Mulsa calculation
        panjang_mulsa_per_bedengan = panjang_bedengan + 0.5  # Extra 0.5m
        total_panjang_mulsa = panjang_mulsa_per_bedengan * jumlah_bedengan
        
        # Mulsa in rolls (assuming 200m per roll, 1.2m width)
        lebar_mulsa_standar = 1.2  # meter
        panjang_per_roll = 200  # meter
        jumlah_roll_mulsa = int(total_panjang_mulsa / panjang_per_roll) + 1
        
        # Display results
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.metric(
                "Total Bibit Dibutuhkan",
                f"{total_tanaman:,} batang",
                help="Tambah 10-20% untuk cadangan"
            )
            st.info(f"**Cadangan 15%:** {int(total_tanaman * 1.15):,} batang")
        
        with col_r2:
            st.metric(
                "Populasi per Ha",
                f"{populasi_per_ha:,} tanaman/ha",
                help="Berdasarkan jarak tanam"
            )
            st.info(f"**Jumlah Bedengan:** {jumlah_bedengan} bedengan")
        
        with col_r3:
            st.metric(
                "Panjang Mulsa",
                f"{total_panjang_mulsa:,.0f} m",
                help="Total panjang mulsa yang dibutuhkan"
            )
            st.info(f"**Jumlah Roll:** {jumlah_roll_mulsa} roll (@200m)")
        
        st.markdown("---")
        
        # Detailed breakdown
        st.subheader("📋 Rincian Detail")
        
        detail_data = {
            "Parameter": [
                "Luas Lahan",
                "Panjang Bedengan",
                "Lebar Bedengan",
                "Jumlah Bedengan",
                "Jarak Dalam Baris",
                "Jarak Antar Baris",
                "Jumlah Baris per Bedengan",
                "Tanaman per Baris",
                "Tanaman per Bedengan",
                "Total Tanaman",
                "Populasi per Ha",
                "Panjang Mulsa Total",
                "Jumlah Roll Mulsa (200m)"
            ],
            "Nilai": [
                f"{luas_ha_calc:.2f} Ha ({luas_m2:,} m²)",
                f"{panjang_bedengan} m",
                f"{lebar_bedengan} m",
                f"{jumlah_bedengan} bedengan",
                f"{jarak_dalam_baris} cm",
                f"{jarak_antar_baris} cm",
                f"{jumlah_baris} baris",
                f"{tanaman_per_baris} batang",
                f"{tanaman_per_bedengan} batang",
                f"{total_tanaman:,} batang",
                f"{populasi_per_ha:,} tanaman/ha",
                f"{total_panjang_mulsa:,.0f} m",
                f"{jumlah_roll_mulsa} roll"
            ]
        }
        
        df_detail = pd.DataFrame(detail_data)
        st.dataframe(df_detail, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Cost estimation
        st.subheader("💰 Estimasi Biaya")
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("**Bibit:**")
            harga_bibit = st.number_input(
                "Harga per batang (Rp)",
                min_value=100,
                max_value=5000,
                value=500,
                step=100
            )
            
            bibit_dengan_cadangan = int(total_tanaman * 1.15)
            total_biaya_bibit = bibit_dengan_cadangan * harga_bibit
            
            st.success(f"Total Biaya Bibit: **Rp {total_biaya_bibit:,}**")
            st.caption(f"{bibit_dengan_cadangan:,} batang × Rp {harga_bibit:,}")
        
        with col_c2:
            st.markdown("**Mulsa:**")
            harga_mulsa_per_roll = st.number_input(
                "Harga per roll (Rp)",
                min_value=50000,
                max_value=500000,
                value=180000,
                step=10000,
                help="1 roll = 200m × 1.2m"
            )
            
            total_biaya_mulsa = jumlah_roll_mulsa * harga_mulsa_per_roll
            
            st.success(f"Total Biaya Mulsa: **Rp {total_biaya_mulsa:,}**")
            st.caption(f"{jumlah_roll_mulsa} roll × Rp {harga_mulsa_per_roll:,}")
        
        # Intercrop calculations
        if use_intercrop and intercrop_type:
            st.markdown("---")
            st.subheader(f"🌾 Tumpang Sari: {intercrop_type}")
            
            # Calculate intercrop seedlings
            # Intercrop ditanam di tengah baris (between rows)
            intercrop_spacing_m = intercrop_spacing / 100
            
            # Number of intercrop plants per bed length
            intercrop_per_bed = int(panjang_bedengan / intercrop_spacing_m)
            
            # Total intercrop plants (1 row per bed, di tengah)
            total_intercrop = intercrop_per_bed * jumlah_bedengan
            
            # With buffer
            intercrop_dengan_cadangan = int(total_intercrop * 1.15)
            total_biaya_intercrop = intercrop_dengan_cadangan * intercrop_price
            
            col_ic1, col_ic2, col_ic3 = st.columns(3)
            
            with col_ic1:
                st.metric(
                    f"Bibit {intercrop_type}",
                    f"{total_intercrop:,} batang",
                    help="Tanaman sela di tengah baris"
                )
                st.caption(f"Cadangan 15%: {intercrop_dengan_cadangan:,} batang")
            
            with col_ic2:
                st.metric(
                    "Jarak Tanam",
                    f"{intercrop_spacing} cm",
                    help=f"Jarak antar {intercrop_type}"
                )
                st.caption(f"{intercrop_per_bed} tanaman/bedengan")
            
            with col_ic3:
                st.metric(
                    f"Biaya Bibit {intercrop_type}",
                    f"Rp {total_biaya_intercrop:,}"
                )
                st.caption(f"{intercrop_dengan_cadangan:,} × Rp {intercrop_price:,}")
            
            st.info(f"""
            **💡 Manfaat Tumpang Sari {intercrop_type}:**
            - Optimasi penggunaan lahan
            - Tambahan pendapatan saat fase vegetatif cabai
            - Mengurangi gulma
            - Diversifikasi risiko
            
            **⚠️ Perhatian:**
            - Jangan sampai menaungi cabai
            - Panen {intercrop_type} sebelum cabai berbuah
            - Sesuaikan pemupukan untuk 2 tanaman
            """)

        
        # Total
        total_biaya_teknis = total_biaya_bibit + total_biaya_mulsa
        
        if use_intercrop and intercrop_type:
            total_biaya_teknis += total_biaya_intercrop
        
        st.markdown("---")
        
        if use_intercrop and intercrop_type:
            st.success(f"""
            ### 💵 Total Biaya (Bibit Cabai + {intercrop_type} + Mulsa)
            **Rp {total_biaya_teknis:,}**
            
            - Bibit Cabai: Rp {total_biaya_bibit:,}
            - Bibit {intercrop_type}: Rp {total_biaya_intercrop:,}
            - Mulsa: Rp {total_biaya_mulsa:,}
            """)
        else:
            st.success(f"""
            ### 💵 Total Biaya (Bibit + Mulsa)
            **Rp {total_biaya_teknis:,}**
            
            - Bibit: Rp {total_biaya_bibit:,}
            - Mulsa: Rp {total_biaya_mulsa:,}
            """)
        
        # Download
        csv_detail = df_detail.to_csv(index=False)
        st.download_button(
            label="📥 Download Perhitungan (CSV)",
            data=csv_detail,
            file_name=f"Perhitungan_Teknis_{luas_ha_calc:.2f}ha.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>💰 RAB Calculator</strong> - Budidaya Cabai Platform</p>
    <p><small>Data berdasarkan riset pasar & pengalaman petani</small></p>
</div>
""", unsafe_allow_html=True)


with tab2:
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



with tab3:
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
        
        # Detailed items - EDITABLE
        st.subheader("📝 Rincian Item Detail (Editable)")
        
        st.info("💡 **Tip:** Klik pada cell Harga atau Volume untuk mengedit. Total akan otomatis terupdate!")
        
        # Prepare editable data
        items_edit_data = []
        for idx, item in enumerate(result['items']):
            items_edit_data.append({
                'No': idx + 1,
                'Kategori': item['kategori'],
                'Item': item['item'],
                'Volume': item['volume'] * luas_ha,
                'Satuan': item['satuan'],
                'Harga': item['harga'],
                'Total': item['volume'] * item['harga'] * luas_ha
            })
        
        df_items_edit = pd.DataFrame(items_edit_data)
        
        # Editable dataframe
        edited_df = st.data_editor(
            df_items_edit,
            column_config={
                "No": st.column_config.NumberColumn("No", width="small", disabled=True),
                "Kategori": st.column_config.TextColumn("Kategori", width="medium", disabled=True),
                "Item": st.column_config.TextColumn("Item", width="large", disabled=True),
                "Volume": st.column_config.NumberColumn(
                    "Volume",
                    width="medium",
                    min_value=0,
                    format="%.2f",
                    help="Edit volume sesuai kebutuhan"
                ),
                "Satuan": st.column_config.TextColumn("Satuan", width="small", disabled=True),
                "Harga": st.column_config.NumberColumn(
                    "Harga Satuan (Rp)",
                    width="medium",
                    min_value=0,
                    format="Rp %,.0f",
                    help="Edit harga sesuai harga pasar"
                ),
                "Total": st.column_config.NumberColumn(
                    "Total (Rp)",
                    width="large",
                    disabled=True,
                    format="Rp %,.0f"
                )
            },
            hide_index=True,
            use_container_width=True,
            num_rows="fixed"
        )
        
        # Recalculate totals based on edited values
        edited_df['Total'] = edited_df['Volume'] * edited_df['Harga']
        
        # Calculate new totals
        new_total_biaya = edited_df['Total'].sum()
        original_total = result['total_biaya']
        difference = new_total_biaya - original_total
        difference_pct = (difference / original_total) * 100 if original_total > 0 else 0
        
        # Display updated totals
        st.markdown("---")
        st.subheader("💰 Total Biaya (Updated)")
        
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            st.metric(
                "Total Biaya Original",
                f"Rp {original_total:,.0f}"
            )
        
        with col_t2:
            st.metric(
                "Total Biaya Edited",
                f"Rp {new_total_biaya:,.0f}",
                delta=f"Rp {difference:,.0f}" if difference != 0 else None
            )
        
        with col_t3:
            if difference != 0:
                st.metric(
                    "Perubahan",
                    f"{difference_pct:+.1f}%",
                    delta=f"{'Hemat' if difference < 0 else 'Tambah'} Rp {abs(difference):,.0f}"
                )
            else:
                st.metric("Perubahan", "0%")
        
        # Updated breakdown by category
        if difference != 0:
            st.markdown("---")
            st.subheader("📊 Breakdown Updated (per Kategori)")
            
            # Group by category
            category_totals = edited_df.groupby('Kategori')['Total'].sum().reset_index()
            category_totals.columns = ['Kategori', 'Total']
            category_totals['Persentase'] = (category_totals['Total'] / new_total_biaya * 100).round(1)
            category_totals['Total'] = category_totals['Total'].apply(lambda x: f"Rp {x:,.0f}")
            category_totals['Persentase'] = category_totals['Persentase'].apply(lambda x: f"{x}%")
            
            st.dataframe(category_totals, use_container_width=True, hide_index=True)
        
        # Download button with edited data
        csv_edited = edited_df.to_csv(index=False)
        st.download_button(
            label="📥 Download RAB Edited (CSV)",
            data=csv_edited,
            file_name=f"RAB_{scenario_key}_{luas_ha}ha_edited.csv",
            mime="text/csv"
        )



with tab4:
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

