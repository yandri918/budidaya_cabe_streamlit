import streamlit as st
import json
from datetime import datetime
from services.database_service import DatabaseService

st.set_page_config(page_title="Data Management", page_icon="💾", layout="wide")

# Initialize database
DatabaseService.init_database()

st.title("💾 Data Management")
st.markdown("**Kelola database, backup, dan export/import data**")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Database Statistics",
    "📤 Export & Import",
    "💾 Backup Management"
])

# TAB 1: Statistics
with tab1:
    st.header("📊 Database Statistics")
    
    stats = DatabaseService.get_database_stats()
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric(
            "Total Panen",
            stats['total_harvests'],
            help="Jumlah record panen"
        )
    
    with col_stat2:
        st.metric(
            "Growth Records",
            stats['total_growth_records'],
            help="Jumlah record pertumbuhan"
        )
    
    with col_stat3:
        st.metric(
            "Journal Entries",
            stats['total_journal_entries'],
            help="Jumlah catatan jurnal"
        )
    
    with col_stat4:
        st.metric(
            "Total Users",
            stats['total_users'],
            help="Jumlah profil petani"
        )
    
    st.info(f"📁 **Database Size:** {stats['database_size_kb']:.2f} KB")
    
    # Database health
    st.markdown("---")
    st.subheader("🏥 Database Health")
    
    if stats['total_harvests'] > 0 or stats['total_growth_records'] > 0:
        st.success("✅ Database aktif dan berisi data")
    else:
        st.warning("⚠️ Database kosong - belum ada data")
    
    # Recent activity
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    recent_harvests = DatabaseService.get_all_harvests()
    
    if recent_harvests:
        st.write(f"**Last 5 Harvests:**")
        
        for harvest in recent_harvests[:5]:
            st.write(f"- {harvest['date']}: {harvest['farmer_name']} - {harvest['weight_kg']}kg Grade {harvest['grading']}")
    else:
        st.info("Belum ada data panen")

# TAB 2: Export & Import
with tab2:
    st.header("📤 Export & Import Data")
    
    # Export section
    st.subheader("📤 Export Data")
    
    st.info("""
    **Export semua data ke JSON:**
    - Semua tabel (harvests, growth, journal, profiles)
    - Format JSON untuk portability
    - Bisa di-import kembali
    """)
    
    if st.button("📥 Generate JSON Export", type="primary"):
        with st.spinner("Generating export..."):
            json_data = DatabaseService.export_to_json()
            
            st.success("✅ Export berhasil!")
            
            st.download_button(
                label="💾 Download JSON",
                data=json_data,
                file_name=f"budidaya_cabe_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Show preview
            with st.expander("👁️ Preview Export Data"):
                data = json.loads(json_data)
                st.json({
                    'export_date': data['export_date'],
                    'version': data['version'],
                    'record_counts': {
                        'harvests': len(data['data']['harvests']),
                        'growth_records': len(data['data']['growth_records']),
                        'journal_entries': len(data['data']['journal_entries']),
                        'user_profiles': len(data['data']['user_profiles'])
                    }
                })
    
    # Import section
    st.markdown("---")
    st.subheader("📥 Import Data")
    
    st.warning("""
    **⚠️ Perhatian:**
    - Import akan menambahkan data ke database existing
    - Pilih mode 'Replace' untuk mengganti semua data
    - Backup data sebelum import!
    """)
    
    uploaded_file = st.file_uploader(
        "Upload JSON file",
        type=['json'],
        help="Upload file JSON hasil export"
    )
    
    if uploaded_file:
        try:
            json_data = json.load(uploaded_file)
            
            st.success("✅ File JSON valid!")
            
            # Show preview
            st.write("**Preview Data:**")
            st.json({
                'export_date': json_data.get('export_date', 'Unknown'),
                'version': json_data.get('version', 'Unknown'),
                'record_counts': {
                    'harvests': len(json_data['data'].get('harvests', [])),
                    'growth_records': len(json_data['data'].get('growth_records', [])),
                    'journal_entries': len(json_data['data'].get('journal_entries', [])),
                    'user_profiles': len(json_data['data'].get('user_profiles', []))
                }
            })
            
            # Import mode
            import_mode = st.radio(
                "Import Mode",
                ['merge', 'replace'],
                format_func=lambda x: 'Merge (Tambahkan ke data existing)' if x == 'merge' else 'Replace (Hapus data lama, ganti dengan import)',
                help="Pilih mode import"
            )
            
            if st.button("📥 Import Data", type="primary"):
                with st.spinner("Importing data..."):
                    DatabaseService.import_from_json(json_data, mode=import_mode)
                    
                    st.success(f"✅ Data berhasil di-import (mode: {import_mode})!")
                    st.balloons()
                    
                    # Reload stats
                    st.rerun()
        
        except json.JSONDecodeError:
            st.error("❌ File JSON tidak valid!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# TAB 3: Backup Management
with tab3:
    st.header("💾 Backup Management")
    
    st.info("""
    **Auto-Backup:**
    - Backup otomatis dibuat setiap hari
    - Menyimpan 7 backup terakhir
    - Format JSON untuk portability
    """)
    
    # Manual backup
    st.subheader("📦 Create Manual Backup")
    
    if st.button("💾 Create Backup Now", type="primary"):
        with st.spinner("Creating backup..."):
            backup_file = DatabaseService.create_backup()
            
            st.success(f"✅ Backup berhasil dibuat!")
            st.info(f"📁 File: `{backup_file}`")
    
    # List backups
    st.markdown("---")
    st.subheader("📋 Backup History")
    
    import os
    
    backup_dir = DatabaseService.BACKUP_DIR
    
    if os.path.exists(backup_dir):
        backups = sorted([
            f for f in os.listdir(backup_dir)
            if f.startswith('backup_') and f.endswith('.json')
        ], reverse=True)
        
        if backups:
            st.write(f"**Found {len(backups)} backup(s):**")
            
            for backup in backups:
                backup_path = os.path.join(backup_dir, backup)
                size_kb = os.path.getsize(backup_path) / 1024
                
                col_b1, col_b2, col_b3 = st.columns([3, 1, 1])
                
                with col_b1:
                    st.write(f"📦 {backup}")
                
                with col_b2:
                    st.caption(f"{size_kb:.2f} KB")
                
                with col_b3:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        backup_data = f.read()
                    
                    st.download_button(
                        label="⬇️",
                        data=backup_data,
                        file_name=backup,
                        mime="application/json",
                        key=f"download_{backup}"
                    )
        else:
            st.info("Belum ada backup")
    else:
        st.info("Backup directory belum ada")
    
    # Clear database
    st.markdown("---")
    st.subheader("🗑️ Clear Database")
    
    st.error("""
    **⚠️ DANGER ZONE:**
    - Ini akan menghapus SEMUA data
    - Tidak bisa di-undo
    - Backup data terlebih dahulu!
    """)
    
    if st.checkbox("Saya mengerti risikonya"):
        if st.button("🗑️ Clear All Data", type="secondary"):
            # This would need implementation in database_service
            st.warning("Feature ini belum diimplementasikan untuk keamanan")

# Footer
st.markdown("---")
st.info("""
**💡 Tips Data Management:**
- Export data secara berkala untuk backup
- Gunakan JSON export untuk portability
- Auto-backup menyimpan 7 hari terakhir
- Import mode 'merge' untuk menambah data
- Import mode 'replace' untuk restore dari backup

**🔗 Integration:**
- Data dari Module 16 (Laporan Panen) tersimpan otomatis
- Module 10 & 11 akan terintegrasi di update berikutnya
- Semua data tersimpan di SQLite database lokal
""")

st.caption(f"Database: {DatabaseService.DB_PATH}")
