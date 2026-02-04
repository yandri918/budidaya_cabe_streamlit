import streamlit as st
import pandas as pd
from datetime import datetime
from services.quality_control_service import QualityControlService
from services.database_service import DatabaseService
from data.quality_standards import CERTIFICATION_TYPES

st.set_page_config(page_title="QR Generator", page_icon="📱", layout="wide")

# Initialize database
DatabaseService.init_database()

# Header
st.title("📱 QR Code Generator")
st.markdown("**Generate QR codes for product traceability**")

st.info("""
**Quick QR Generation:**
- Auto-generated Product ID
- Links to Vercel verification website
- Saves to database for API access
""")

st.warning("""
⚠️ **API Backend Status:**
- QR links to: https://cabe-q-r-vercel.vercel.app/
- For real data sync: Deploy `api_main.py` to Streamlit Cloud
- See `API_DEPLOYMENT_GUIDE.md` for instructions
""")

# Input Section
st.markdown("---")
st.subheader("Product Information")

col1, col2 = st.columns([1, 1])

with col1:
    # Product details
    harvest_date = st.date_input("Harvest Date", value=datetime.now(), key="qr_harvest_date")
    batch_number = st.text_input("Batch Number", value="B001", key="qr_batch")
    
    # Auto-generate Product ID
    harvest_id = f"H{harvest_date.strftime('%j')}"
    product_id = f"CHI-{harvest_id}-{batch_number}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    st.info(f"**Product ID:** `{product_id}`")
    
    farm_location = st.text_input("Farm Location", value="Garut, Jawa Barat", key="qr_location")
    farmer_name = st.text_input("Farmer Name", value="", key="qr_farmer")

with col2:
    grade = st.selectbox(
        "Quality Grade", 
        ["Grade A (Premium)", "Grade B (Standard)", "Grade C (Economy)"],
        key="qr_grade"
    )
    
    weight_kg = st.number_input("Weight (kg)", min_value=0.0, max_value=1000.0, value=10.0, step=0.1, key="qr_weight")
    
    # Certifications
    available_certs = list(CERTIFICATION_TYPES.keys())
    selected_certs = st.multiselect("Certifications", available_certs, default=[], key="qr_certs")

# Generate Button
st.markdown("---")

if st.button("🎯 Generate QR Code", type="primary", key="qr_generate_btn", use_container_width=True):
    with st.spinner("Generating QR code..."):
        try:
            # Prepare product data
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
            
            # Store in session state
            st.session_state.qr_data = {
                'qr_image': qr_result['qr_image_base64'],
                'verification_url': qr_result['verification_url'],
                'product_data': product_data
            }
            
            # Save to database (non-blocking)
            try:
                DatabaseService.save_qr_product(product_data)
                st.session_state.db_saved = True
                
                # Export all products to JSON for Vercel sync
                try:
                    import json
                    all_products = DatabaseService.get_all_qr_products()
                    json_path = 'qr_products.json'
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(all_products, f, indent=2, ensure_ascii=False)
                    st.session_state.json_exported = True
                except Exception as json_error:
                    st.session_state.json_exported = False
                    
            except Exception as db_error:
                st.session_state.db_saved = False
                st.warning(f"⚠️ Database save failed: {str(db_error)}")
            
            st.success("✅ QR Code generated successfully!")
            
        except Exception as e:
            st.error(f"❌ Error generating QR code: {str(e)}")
            st.exception(e)

# Display Section (persists across reruns)
if 'qr_data' in st.session_state:
    st.markdown("---")
    st.markdown("### 📱 Your QR Code")
    
    qr_data = st.session_state.qr_data
    product_data = qr_data['product_data']
    
    col_display1, col_display2 = st.columns([1, 1])
    
    with col_display1:
        # QR Image
        st.image(f"data:image/png;base64,{qr_data['qr_image']}", width=300)
        
        # Download button
        st.download_button(
            label="📥 Download QR Code URL",
            data=qr_data['verification_url'],
            file_name=f"QR_{product_data['product_id']}.txt",
            mime="text/plain",
            key="qr_download_btn",
            use_container_width=True
        )
        
        if st.session_state.get('db_saved', False):
            st.caption("✅ Saved to database for API access")
            if st.session_state.get('json_exported', False):
                st.caption("✅ Exported to qr_products.json for Vercel sync")
    
    with col_display2:
        # Verification URL
        st.info(f"🔗 **Verification URL:**\n\n{qr_data['verification_url']}")
        st.caption("💡 Scan QR code dengan smartphone untuk langsung ke halaman verifikasi")
        
        # Product Summary
        st.markdown("**Product Details:**")
        st.write(f"• **ID:** {product_data['product_id']}")
        st.write(f"• **Date:** {product_data['harvest_date']}")
        st.write(f"• **Location:** {product_data['farm_location']}")
        st.write(f"• **Farmer:** {product_data['farmer_name']}")
        st.write(f"• **Grade:** {product_data['grade']}")
        st.write(f"• **Weight:** {product_data['weight_kg']} kg")
        if product_data['certifications']:
            st.write(f"• **Certifications:** {', '.join(product_data['certifications'])}")

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Generate new QR code to update the display. Previous QR codes are saved in database.")
