import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from services.journal_service import JournalService
from services.growth_monitoring_service import GrowthMonitoringService
from data.activity_templates import ACTIVITY_TEMPLATES

st.set_page_config(page_title="Jurnal Budidaya", page_icon="📔", layout="wide")

st.title("📔 Jurnal Budidaya Cabai")
st.markdown("**Catat aktivitas harian dan pantau compliance dengan SOP**")

# Initialize session state
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []

if 'planting_date' not in st.session_state:
    st.session_state.planting_date = datetime.now() - timedelta(days=30)

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📝 Log Harian",
    "📊 Analisis & Laporan",
    "✅ SOP Checklist"
])

# TAB 1: Daily Log
with tab1:
    st.header("📝 Log Aktivitas Harian")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        planting_date = st.date_input(
            "Tanggal Tanam",
            value=st.session_state.planting_date
        )
        st.session_state.planting_date = planting_date
    
    with col_info2:
        current_hst = GrowthMonitoringService.calculate_hst(planting_date)
        st.metric("HST Saat Ini", f"{current_hst} hari")
    
    st.markdown("---")
    
    # Activity input
    st.subheader("➕ Tambah Aktivitas")
    
    col_act1, col_act2, col_act3 = st.columns(3)
    
    with col_act1:
        activity_date = st.date_input(
            "Tanggal",
            value=datetime.now()
        )
        
        activity_hst = GrowthMonitoringService.calculate_hst(planting_date)
        
        activity_type = st.selectbox(
            "Jenis Aktivitas",
            list(ACTIVITY_TEMPLATES.keys())
        )
        
        template = ACTIVITY_TEMPLATES[activity_type]
    
    with col_act2:
        details = st.text_area(
            "Detail Aktivitas",
            placeholder=f"Contoh: {template['description']}",
            height=100
        )
        
        cost = st.number_input(
            "Biaya (Rp)",
            min_value=0,
            value=template['default_cost'],
            step=10000
        )
    
    with col_act3:
        notes = st.text_area(
            "Catatan Tambahan",
            placeholder="Observasi, hasil, dll",
            height=100
        )
        
        st.info(f"{template['icon']} {template['description']}")
    
    if st.button("💾 Simpan Aktivitas", type="primary"):
        entry = JournalService.create_entry(
            date=activity_date.strftime("%Y-%m-%d"),
            hst=activity_hst,
            activity_type=activity_type,
            details=details,
            cost=cost,
            notes=notes
        )
        st.session_state.journal_entries.append(entry)
        st.success(f"✅ Aktivitas '{activity_type}' berhasil dicatat!")
    
    # Show recent entries
    if st.session_state.journal_entries:
        st.markdown("---")
        st.subheader("📋 Aktivitas Terbaru")
        
        # Sort by date descending
        sorted_entries = sorted(
            st.session_state.journal_entries,
            key=lambda x: x['date'],
            reverse=True
        )[:10]  # Show last 10
        
        for entry in sorted_entries:
            with st.expander(f"{entry['icon']} {entry['date']} (HST {entry['hst']}) - {entry['activity_type']}"):
                col_e1, col_e2 = st.columns([2, 1])
                
                with col_e1:
                    st.write(f"**Detail:** {entry['details']}")
                    if entry['notes']:
                        st.write(f"**Catatan:** {entry['notes']}")
                
                with col_e2:
                    st.metric("Biaya", f"Rp {entry['cost']:,.0f}")

# TAB 2: Analytics & Reports
with tab2:
    st.header("📊 Analisis & Laporan")
    
    if st.session_state.journal_entries:
        # Summary metrics
        total_cost = JournalService.calculate_total_cost(st.session_state.journal_entries)
        total_entries = len(st.session_state.journal_entries)
        
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        
        with col_sum1:
            st.metric("Total Aktivitas", f"{total_entries} entries")
        
        with col_sum2:
            st.metric("Total Biaya", f"Rp {total_cost:,.0f}")
        
        with col_sum3:
            avg_cost = total_cost / total_entries if total_entries > 0 else 0
            st.metric("Rata-rata Biaya", f"Rp {avg_cost:,.0f}")
        
        st.markdown("---")
        
        # Activity breakdown
        st.subheader("📊 Breakdown per Aktivitas")
        
        grouped = JournalService.group_by_activity(st.session_state.journal_entries)
        
        breakdown_data = []
        for activity_type, entries in grouped.items():
            template = ACTIVITY_TEMPLATES[activity_type]
            breakdown_data.append({
                'Aktivitas': f"{template['icon']} {activity_type}",
                'Jumlah': len(entries),
                'Total Biaya': sum(e['cost'] for e in entries),
                'Rata-rata': sum(e['cost'] for e in entries) / len(entries) if entries else 0
            })
        
        df_breakdown = pd.DataFrame(breakdown_data)
        df_breakdown['Total Biaya'] = df_breakdown['Total Biaya'].apply(lambda x: f"Rp {x:,.0f}")
        df_breakdown['Rata-rata'] = df_breakdown['Rata-rata'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Activity count chart
            activity_counts = {k: len(v) for k, v in grouped.items()}
            fig_count = px.pie(
                values=list(activity_counts.values()),
                names=list(activity_counts.keys()),
                title="Distribusi Aktivitas"
            )
            st.plotly_chart(fig_count, use_container_width=True)
        
        with col_chart2:
            # Cost distribution chart
            activity_costs = {k: sum(e['cost'] for e in v) for k, v in grouped.items()}
            fig_cost = px.pie(
                values=list(activity_costs.values()),
                names=list(activity_costs.keys()),
                title="Distribusi Biaya"
            )
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Export
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            csv_data = JournalService.export_to_csv(st.session_state.journal_entries)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"jurnal_budidaya_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col_exp2:
            if st.button("🗑️ Hapus Semua Data"):
                st.session_state.journal_entries = []
                st.rerun()
    
    else:
        st.info("📊 Belum ada data. Mulai catat aktivitas di tab 'Log Harian'.")

# TAB 3: SOP Checklist
with tab3:
    st.header("✅ SOP Checklist")
    
    st.info("""
    **Checklist berdasarkan SOP untuk HST saat ini.**
    Centang aktivitas yang sudah dilakukan untuk tracking compliance.
    """)
    
    current_hst = GrowthMonitoringService.calculate_hst(st.session_state.planting_date)
    
    st.metric("HST Saat Ini", f"{current_hst} hari")
    
    # Get SOP tasks for current HST
    sop_checklist = JournalService.get_sop_checklist(current_hst)
    
    if sop_checklist:
        st.subheader(f"📋 Tugas untuk HST {current_hst}")
        
        for i, task in enumerate(sop_checklist):
            col_check1, col_check2, col_check3 = st.columns([3, 1, 1])
            
            with col_check1:
                completed = st.checkbox(
                    f"{task['icon']} {task['task']}",
                    key=f"task_{i}"
                )
            
            with col_check2:
                st.caption(f"Tipe: {task['activity_type']}")
            
            with col_check3:
                st.caption(f"Est: Rp {task['default_cost']:,.0f}")
        
        # Compliance rate
        completed_count = sum(1 for i in range(len(sop_checklist)) if st.session_state.get(f"task_{i}", False))
        compliance_rate = JournalService.calculate_compliance_rate(completed_count, len(sop_checklist))
        
        st.markdown("---")
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.metric(
                "Compliance Rate",
                f"{compliance_rate:.1f}%",
                delta=f"{completed_count}/{len(sop_checklist)} tugas"
            )
        
        with col_comp2:
            if compliance_rate >= 80:
                st.success("✅ Excellent! SOP compliance tinggi")
            elif compliance_rate >= 60:
                st.warning("⚠️ Good, tingkatkan compliance")
            else:
                st.error("❌ Perlu perbaikan, banyak tugas terlewat")
    
    else:
        st.info(f"📋 Tidak ada tugas SOP spesifik untuk HST {current_hst}. Lanjutkan perawatan rutin.")

# Footer
st.markdown("---")
st.info("""
**💡 Tips Jurnal:**
- Catat aktivitas setiap hari untuk data akurat
- Gunakan SOP checklist sebagai panduan
- Review laporan mingguan untuk evaluasi
- Export data untuk analisis lebih lanjut
- Bandingkan biaya aktual dengan RAB
""")
