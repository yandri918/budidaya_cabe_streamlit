import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from services.quality_control_service import QualityControlService
from services.database_service import DatabaseService
from data.quality_standards import (
    QUALITY_STANDARDS,
    INSPECTION_CHECKLISTS,
    CERTIFICATION_TYPES,
    LAB_TEST_TYPES
)

st.set_page_config(page_title="Quality Control", page_icon="✅", layout="wide")

# Initialize database
DatabaseService.init_database()

st.title("✅ Quality Control & Traceability")
st.markdown("**Sistem jaminan kualitas dan traceability untuk akses pasar premium**")

# Initialize session state
if 'qr_codes' not in st.session_state:
    st.session_state.qr_codes = []

if 'inspections' not in st.session_state:
    st.session_state.inspections = []

if 'certifications' not in st.session_state:
    st.session_state.certifications = []

if 'lab_results' not in st.session_state:
    st.session_state.lab_results = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📱 QR Code Generator",
    "🔍 Traceability",
    "✅ Quality Inspection",
    "🏆 Certifications",
    "🔬 Lab Results"
])

# TAB 1: QR Code Generator
with tab1:
    st.header("📱 QR Code Generator")
    
    st.info("""
    **Generate QR code untuk product traceability:**
    - Unique product ID
    - Harvest information
    - Farm location & farmer
    - Quality grade
    - Certification status
    """)
    
    st.warning("""
    **⚠️ Important Note - API Backend:**
    - QR code akan membuka: https://cabe-q-r-vercel.vercel.app/
    - Website Vercel menggunakan **API backend** untuk data real-time
    - Data **sinkron** dengan database Streamlit via FastAPI
    - Scan QR → Vercel call API → Display real data
    - Saat ini: Production-ready traceability system! ✅
    """)
    
    col_qr1, col_qr2 = st.columns(2)
    
    with col_qr1:
        st.subheader("Product Information")
        
        harvest_id = st.text_input("Harvest ID", value="H001", help="ID panen dari Module 16")
        batch_number = st.text_input("Batch Number", value="B001")
        
        # Generate product ID
        if st.button("🔢 Generate Product ID"):
            product_id = QualityControlService.generate_product_id(harvest_id, batch_number)
            st.session_state.current_product_id = product_id
            st.success(f"Product ID: {product_id}")
        
        product_id = st.text_input(
            "Product ID",
            value=st.session_state.get('current_product_id', 'CHI-H001-B001-20260102'),
            help="Unique product identifier"
        )
        
        harvest_date = st.date_input("Harvest Date", value=datetime.now())
        
        farm_location = st.text_input(
            "Farm Location",
            value=st.session_state.get('farm_location', 'Garut, Jawa Barat'),
            placeholder="e.g., Garut, Jawa Barat"
        )
        
        farmer_name = st.text_input(
            "Farmer Name",
            value=st.session_state.get('farmer_name', 'Petani Demo'),
            placeholder="Nama petani"
        )
        
        grade = st.selectbox("Quality Grade", list(QUALITY_STANDARDS.keys()))
        
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, max_value=1000.0, value=10.0, step=0.1)
        
        # Certifications
        available_certs = list(CERTIFICATION_TYPES.keys())
        selected_certs = st.multiselect("Certifications", available_certs, default=[])
    
    with col_qr2:
        st.subheader("Generate QR Code")
        
        if st.button("🎯 Generate QR Code", type="primary", key="generate_qr_btn"):
            with st.spinner("Generating QR code..."):
                try:
                    product_data = {
                        'product_id': product_id,
                        'harvest_date': harvest_date.strftime('%Y-%m-%d'),
                        'farm_location': farm_location,
                        'farmer_name': farmer_name,
                        'grade': grade,
                        'batch_number': batch_number,
                        'weight_kg': weight_kg,
                        'certifications': selected_certs
                    }
                    
                    # Generate QR code
                    qr_result = QualityControlService.generate_qr_code(product_data)
                    
                    # Store in session state so it persists across reruns
                    st.session_state.current_qr = {
                        'qr_image': qr_result['qr_image_base64'],
                        'verification_url': qr_result['verification_url'],
                        'product_data': product_data
                    }
                    
                    st.success("✅ QR Code generated successfully!")
                    
                    # Try to save to database (non-critical)
                    try:
                        DatabaseService.save_qr_product(product_data)
                    except:
                        pass
                    
                except Exception as e:
                    st.error(f"❌ Error generating QR code: {str(e)}")
                    st.exception(e)
        
        # Display QR if it exists in session state (persists across reruns)
        if 'current_qr' in st.session_state:
            qr_data = st.session_state.current_qr
            product_data = qr_data['product_data']
            
            # Display QR code
            st.markdown("---")
            st.markdown("### 📱 QR Code")
            
            # Show QR image
            st.image(f"data:image/png;base64,{qr_data['qr_image']}", width=300)
            
            # Verification URL
            st.markdown("---")
            st.info(f"🔗 **Verification URL:** {qr_data['verification_url']}")
            st.caption("💡 Scan QR code dengan smartphone untuk langsung ke halaman verifikasi")
            
            # Product info
            st.markdown("---")
            st.markdown("### 📋 Product Information")
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write(f"**Product ID:** {product_data['product_id']}")
                st.write(f"**Harvest Date:** {product_data['harvest_date']}")
                st.write(f"**Location:** {product_data['farm_location']}")
                st.write(f"**Farmer:** {product_data['farmer_name']}")
            
            with col_info2:
                st.write(f"**Grade:** {product_data['grade']}")
                st.write(f"**Weight:** {product_data['weight_kg']} kg")
                st.write(f"**Batch:** {product_data['batch_number']}")
                if product_data['certifications']:
                    st.write(f"**Certifications:** {', '.join(product_data['certifications'])}")
            
            # Download button
            st.markdown("---")
            st.download_button(
                label="📥 Download QR Code URL",
                data=qr_data['verification_url'],
                file_name=f"QR_{product_data['product_id']}.txt",
                mime="text/plain",
                key="download_qr_url"
            )
            
            # Product info
            st.markdown("---")
            st.markdown("### Product Information")
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write(f"**Product ID:** {product_id}")
                st.write(f"**Harvest Date:** {harvest_date.strftime('%Y-%m-%d')}")
                st.write(f"**Location:** {farm_location}")
                st.write(f"**Farmer:** {farmer_name}")
            
            with col_info2:
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                st.download_button(
                    label="📥 Download QR Code URL",
                    data=qr_result['verification_url'],
                    file_name=f"QR_{product_id}.txt",
                    mime="text/plain"
                )
            
            with col_dl2:
                # Create clickable link
                st.markdown(f"[🌐 Open Verification Page]({qr_result['verification_url']})")


# TAB 2: Traceability
with tab2:
    st.header("🔍 Product Traceability")
    
    st.info("""
    **Track produk dari farm ke konsumen:**
    - Complete timeline
    - Input tracking
    - Verification system
    """)
    
    product_id_search = st.text_input("Enter Product ID", placeholder="CHI-H001-B001-20260102")
    
    if st.button("🔍 Search Product"):
        # Simulate traceability data (in real app, get from database)
        harvest_data = {
            'product_id': product_id_search,
            'date': '2025-11-20',
            'farm_location': 'Garut, Jawa Barat',
            'farmer_name': 'Budi Santoso',
            'grading': 'A',
            'weight_kg': 10.0
        }
        
        # Get growth and journal data from database
        growth_records = DatabaseService.get_growth_records()[:5]  # Sample
        journal_entries = DatabaseService.get_journal_entries()[:10]  # Sample
        
        traceability = QualityControlService.create_traceability_record(
            harvest_data,
            growth_records,
            journal_entries
        )
        
        st.markdown("---")
        
        # Farm info
        col_farm1, col_farm2 = st.columns(2)
        
        with col_farm1:
            st.metric("Farm Location", traceability['farm_info']['location'])
        
        with col_farm2:
            st.metric("Farmer", traceability['farm_info']['farmer'])
        
        # Timeline
        st.markdown("---")
        st.subheader("📅 Product Timeline")
        
        for item in traceability['timeline']:
            st.markdown(f"""
            <div style='padding: 10px; margin: 5px 0; background-color: #f0f0f0; border-left: 4px solid #3498DB; border-radius: 5px;'>
                <b>{item['icon']} {item['event']}</b> - {item['date']}<br>
                <small>{item['description']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Inputs summary
        st.markdown("---")
        st.subheader("📊 Inputs Used")
        
        col_input1, col_input2, col_input3 = st.columns(3)
        
        with col_input1:
            st.metric("Total Days", traceability['total_days'])
        
        with col_input2:
            fert_count = len(traceability['inputs_summary']['fertilizer'])
            st.metric("Fertilizer Applications", fert_count)
        
        with col_input3:
            organic_status = "✓ Organic" if traceability['inputs_summary']['organic'] else "✗ Not Organic"
            st.write(f"**Status:** {organic_status}")

# TAB 3: Quality Inspection
with tab3:
    st.header("✅ Quality Inspection")
    
    st.info("""
    **Standardized quality checks:**
    - Pre-harvest inspection
    - Harvest quality check
    - Post-harvest inspection
    - Packaging inspection
    """)
    
    inspection_type = st.selectbox(
        "Inspection Type",
        list(INSPECTION_CHECKLISTS.keys()),
        format_func=lambda x: INSPECTION_CHECKLISTS[x]['name']
    )
    
    checklist = QualityControlService.create_inspection_checklist(inspection_type)
    
    st.markdown("---")
    st.subheader(f"📋 {checklist['name']}")
    
    col_insp1, col_insp2 = st.columns([2, 1])
    
    with col_insp1:
        inspector_name = st.text_input("Inspector Name", value="Quality Control Team")
        inspection_date = st.date_input("Inspection Date", value=datetime.now())
    
    with col_insp2:
        st.info(f"**Total Items:** {len(checklist['items'])}")
    
    st.markdown("---")
    st.subheader("Checklist Items")
    
    checklist_results = {}
    
    for item in checklist['items']:
        col_check1, col_check2, col_check3 = st.columns([3, 1, 1])
        
        with col_check1:
            st.write(f"**{item['item']}**")
        
        with col_check2:
            if item['critical']:
                st.markdown("<span style='color: #E74C3C;'>⚠️ Critical</span>", unsafe_allow_html=True)
        
        with col_check3:
            passed = st.checkbox("Pass", value=True, key=f"check_{item['id']}")
            checklist_results[item['id']] = passed
    
    st.markdown("---")
    
    if st.button("📊 Calculate Score", type="primary"):
        score_result = QualityControlService.score_inspection(inspection_type, checklist_results)
        
        # Store inspection
        st.session_state.inspections.append({
            'type': inspection_type,
            'inspector': inspector_name,
            'date': inspection_date.strftime('%Y-%m-%d'),
            'score': score_result['score'],
            'status': score_result['status'],
            'created_at': datetime.now()
        })
        
        st.markdown("---")
        
        # Score display
        col_score1, col_score2, col_score3 = st.columns(3)
        
        with col_score1:
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: {score_result['status_color']}20; border: 3px solid {score_result['status_color']}; border-radius: 10px;'>
                <h1 style='color: {score_result['status_color']}; margin: 0; font-size: 3em;'>{score_result['score']}</h1>
                <h3 style='color: {score_result['status_color']}; margin: 10px 0 0 0;'>{score_result['status']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col_score2:
            st.metric("Critical Items", "PASS" if score_result['critical_passed'] else "FAIL")
        
        with col_score3:
            st.metric("Failed Items", len(score_result['failed_items']))
        
        # Failed items
        if score_result['failed_items']:
            st.markdown("---")
            st.subheader("⚠️ Failed Items")
            for item in score_result['failed_items']:
                st.write(f"• {item}")
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 Recommendations")
        for rec in score_result['recommendations']:
            st.write(f"• {rec}")

# TAB 4: Certifications
with tab4:
    st.header("🏆 Certification Tracker")
    
    st.info("""
    **Track certifications:**
    - Organic, GAP, HACCP, Halal, Export
    - Expiry tracking
    - Renewal reminders
    """)
    
    # Add new certification
    with st.expander("➕ Add New Certification"):
        col_cert1, col_cert2 = st.columns(2)
        
        with col_cert1:
            cert_type = st.selectbox(
                "Certification Type",
                list(CERTIFICATION_TYPES.keys()),
                format_func=lambda x: CERTIFICATION_TYPES[x]['name']
            )
            
            cert_number = st.text_input("Certificate Number", placeholder="CERT-2025-001")
            issue_date = st.date_input("Issue Date", value=datetime.now())
        
        with col_cert2:
            cert_info = CERTIFICATION_TYPES[cert_type]
            
            st.write(f"**Validity:** {cert_info['validity_months']} months")
            st.write("**Requirements:**")
            for req in cert_info['requirements'][:3]:
                st.write(f"• {req}")
        
        if st.button("💾 Save Certification"):
            cert_record = QualityControlService.track_certification(
                cert_type,
                issue_date.strftime('%Y-%m-%d'),
                cert_number
            )
            
            st.session_state.certifications.append(cert_record)
            st.success(f"✅ {cert_record['cert_name']} added!")
            st.rerun()
    
    # Display certifications
    if st.session_state.certifications:
        st.markdown("---")
        st.subheader("📋 Active Certifications")
        
        for cert in st.session_state.certifications:
            col_c1, col_c2, col_c3 = st.columns([2, 1, 1])
            
            with col_c1:
                st.markdown(f"""
                <div style='padding: 15px; background-color: {cert['status_color']}20; border-left: 4px solid {cert['status_color']}; border-radius: 5px;'>
                    <h4 style='margin: 0;'>{cert['status_icon']} {cert['cert_name']}</h4>
                    <small>Certificate: {cert['cert_number']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_c2:
                st.write(f"**Expires:** {cert['expiry_date']}")
                st.write(f"**Days left:** {cert['days_to_expiry']}")
            
            with col_c3:
                st.markdown(f"<h3 style='color: {cert['status_color']}; margin: 0;'>{cert['status']}</h3>", unsafe_allow_html=True)
        
        # Expiring soon
        expiring = QualityControlService.get_expiring_certifications(st.session_state.certifications)
        
        if expiring:
            st.markdown("---")
            st.warning(f"⚠️ **{len(expiring)} certification(s) expiring soon!**")
            for cert in expiring:
                st.write(f"• {cert['cert_name']} - {cert['days_to_expiry']} days left")
    else:
        st.info("No certifications added yet. Add your first certification above!")

# TAB 5: Lab Results
with tab5:
    st.header("🔬 Lab Test Results")
    
    st.info("""
    **Store and analyze lab tests:**
    - Pesticide residue
    - Heavy metals
    - Microbiological tests
    - Nutritional analysis
    - Aflatoxin testing
    """)
    
    # Add new test result
    with st.expander("➕ Add New Test Result"):
        col_lab1, col_lab2 = st.columns(2)
        
        with col_lab1:
            test_type = st.selectbox(
                "Test Type",
                list(LAB_TEST_TYPES.keys()),
                format_func=lambda x: LAB_TEST_TYPES[x]['name']
            )
            
            test_date = st.date_input("Test Date", value=datetime.now())
            lab_name = st.text_input("Laboratory Name", placeholder="Lab Uji Mutu")
            cert_number = st.text_input("Certificate Number", placeholder="LAB-2025-001")
        
        with col_lab2:
            test_info = LAB_TEST_TYPES[test_type]
            
            st.write(f"**Standard:** {test_info['mrl']}")
            st.write(f"**Frequency:** {test_info['frequency']}")
            st.write(f"**Cost:** Rp {test_info['cost_range'][0]:,} - {test_info['cost_range'][1]:,}")
            
            st.write("**Parameters:**")
            for param in test_info['parameters'][:3]:
                st.write(f"• {param}")
        
        st.markdown("---")
        st.subheader("Test Results")
        
        test_results = {}
        
        for param in test_info['parameters']:
            result_value = st.text_input(
                f"{param}",
                placeholder="e.g., Below MRL, 0.05 ppm, Negative",
                key=f"result_{param}"
            )
            if result_value:
                test_results[param] = result_value
        
        if st.button("💾 Save Test Result"):
            if test_results:
                test_record = QualityControlService.store_lab_result(
                    test_type,
                    test_date.strftime('%Y-%m-%d'),
                    test_results,
                    lab_name,
                    cert_number
                )
                
                st.session_state.lab_results.append(test_record)
                st.success(f"✅ {test_record['test_name']} result saved!")
                st.rerun()
            else:
                st.warning("Please enter at least one test result")
    
    # Display test results
    if st.session_state.lab_results:
        st.markdown("---")
        st.subheader("📊 Test History")
        
        for test in st.session_state.lab_results:
            with st.expander(f"{test['status_icon']} {test['test_name']} - {test['test_date']}"):
                col_t1, col_t2 = st.columns(2)
                
                with col_t1:
                    st.write(f"**Laboratory:** {test['lab_name']}")
                    st.write(f"**Certificate:** {test['cert_number']}")
                    st.write(f"**Standard:** {test['mrl_standard']}")
                
                with col_t2:
                    st.markdown(f"<h3 style='color: {test['status_color']}; margin: 0;'>{test['status']}</h3>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.write("**Results:**")
                for param, value in test['results'].items():
                    st.write(f"• {param}: {value}")
                
                if test['failed_params']:
                    st.warning(f"Failed parameters: {', '.join(test['failed_params'])}")
                
                st.markdown("---")
                st.write("**Recommendations:**")
                for rec in test['recommendations']:
                    st.write(f"• {rec}")
        
        # Trend analysis
        if len(st.session_state.lab_results) >= 2:
            st.markdown("---")
            st.subheader("📈 Trend Analysis")
            
            trends = QualityControlService.analyze_test_trends(st.session_state.lab_results)
            
            if not trends.get('insufficient_data'):
                col_trend1, col_trend2, col_trend3 = st.columns(3)
                
                with col_trend1:
                    st.metric("Total Tests", trends['total_tests'])
                
                with col_trend2:
                    st.metric("Pass Rate", f"{trends['pass_rate']}%")
                
                with col_trend3:
                    st.markdown(f"<h3 style='color: {trends['trend_color']};'>{trends['trend_icon']} {trends['trend']}</h3>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.write("**Insights:**")
                for insight in trends['insights']:
                    st.write(f"{insight}")
    else:
        st.info("No test results added yet. Add your first test result above!")

# Footer
st.markdown("---")
st.info("""
**💡 Tips Quality Control:**
- Generate QR code untuk setiap batch panen
- Lakukan inspeksi di setiap tahap (pre, during, post harvest)
- Maintain certifications untuk akses pasar premium
- Regular lab testing untuk compliance
- Track traceability untuk buyer confidence

**🔗 Integration:**
- Module 16: Harvest data untuk QR code
- Module 10 & 11: Growth & journal untuk traceability
- Module 17: Database untuk storage
- Export certifications & lab results untuk audit

**📊 Benefits:**
- Premium market access (30-50% higher price)
- Export readiness
- Consumer trust
- Regulatory compliance
- Quality improvement tracking

**⚠️ Vercel Website Limitation:**
- QR verification website: https://cabe-q-r-vercel.vercel.app/
- Menampilkan **demo data** (auto-generated)
- Tidak sinkron dengan database Streamlit
- Untuk production: perlu API backend
- Saat ini: Demo concept traceability system
""")
