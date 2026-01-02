"""
FastAPI Backend for QR Product Data
Runs alongside Streamlit, shares same SQLite database
Deploy to: Railway, Render, or Streamlit Cloud (separate app)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
import os
from datetime import datetime

app = FastAPI(
    title="QR Product API",
    description="API for QR product traceability data",
    version="1.0.0"
)

# CORS configuration - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path - same as Streamlit
DB_PATH = "data/budidaya_cabe.db"

# Pydantic Models
class TimelineEvent(BaseModel):
    date: str
    event: str
    desc: str
    icon: str

class ProductResponse(BaseModel):
    productId: str
    harvestDate: str
    farmLocation: str
    farmerName: str
    grade: str
    weight: str
    batchNumber: str
    certifications: List[str]
    timeline: List[TimelineEvent]

# Helper Functions
def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database not found")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_product_timeline(farmer_name: str):
    """Get product timeline from growth and journal data"""
    conn = get_db_connection()
    timeline = []
    
    try:
        # Get growth records
        growth_records = conn.execute(
            "SELECT * FROM growth_records WHERE farmer_name = ? ORDER BY hst LIMIT 10",
            (farmer_name,)
        ).fetchall()
        
        for record in growth_records:
            timeline.append({
                'date': record['created_at'][:10] if record['created_at'] else '',
                'event': f"Monitoring HST {record['hst']}",
                'desc': f"Tinggi: {record['height_cm']}cm, Daun: {record['leaf_count']} helai",
                'icon': '📏'
            })
        
        # Get journal entries
        journal_entries = conn.execute(
            "SELECT * FROM journal_entries WHERE farmer_name = ? ORDER BY date LIMIT 10",
            (farmer_name,)
        ).fetchall()
        
        for entry in journal_entries:
            timeline.append({
                'date': entry['date'],
                'event': entry['activity_type'],
                'desc': entry['description'] or '',
                'icon': '📝'
            })
    finally:
        conn.close()
    
    # Sort by date
    timeline.sort(key=lambda x: x['date'] if x['date'] else '')
    
    return timeline

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "QR Product API is running",
        "version": "1.0.0",
        "database": "connected" if os.path.exists(DB_PATH) else "not found"
    }

@app.get("/api/product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get product by ID"""
    conn = get_db_connection()
    
    try:
        # Get product from qr_products table
        product = conn.execute(
            "SELECT * FROM qr_products WHERE product_id = ?",
            (product_id,)
        ).fetchone()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Parse certifications
        certifications = json.loads(product['certifications']) if product['certifications'] else []
        
        # Get timeline
        timeline = get_product_timeline(product['farmer_name'])
        
        # Add harvest event to timeline
        timeline.append({
            'date': product['harvest_date'],
            'event': 'Panen',
            'desc': f"Panen {product['weight_kg']}kg Grade {product['grade']}",
            'icon': '🌾'
        })
        
        # Sort timeline by date
        timeline.sort(key=lambda x: x['date'] if x['date'] else '')
        
        # Format response
        response = {
            'productId': product['product_id'],
            'harvestDate': product['harvest_date'],
            'farmLocation': product['farm_location'] or 'Garut, Jawa Barat',
            'farmerName': product['farmer_name'] or 'Petani Demo',
            'grade': product['grade'] or 'Grade A',
            'weight': f"{product['weight_kg']} kg" if product['weight_kg'] else '10 kg',
            'batchNumber': product['batch_number'] or 'B001',
            'certifications': certifications,
            'timeline': timeline
        }
        
        return response
    
    finally:
        conn.close()

@app.get("/api/products")
async def get_all_products():
    """Get all products"""
    conn = get_db_connection()
    
    try:
        products = conn.execute(
            "SELECT * FROM qr_products ORDER BY created_at DESC LIMIT 100"
        ).fetchall()
        
        result = []
        for product in products:
            certifications = json.loads(product['certifications']) if product['certifications'] else []
            result.append({
                'productId': product['product_id'],
                'harvestDate': product['harvest_date'],
                'farmLocation': product['farm_location'],
                'farmerName': product['farmer_name'],
                'grade': product['grade'],
                'weight': f"{product['weight_kg']} kg",
                'batchNumber': product['batch_number'],
                'certifications': certifications
            })
        
        return result
    
    finally:
        conn.close()

@app.post("/api/product")
async def create_product(product_data: dict):
    """Create new product (called from Streamlit)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Convert certifications to JSON
        certs_json = json.dumps(product_data.get('certifications', []))
        
        cursor.execute('''
            INSERT OR REPLACE INTO qr_products (
                product_id, harvest_id, batch_number, harvest_date,
                farm_location, farmer_name, grade, weight_kg, certifications
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product_data['product_id'],
            product_data.get('harvest_id', ''),
            product_data.get('batch_number', ''),
            product_data['harvest_date'],
            product_data.get('farm_location', ''),
            product_data.get('farmer_name', ''),
            product_data.get('grade', ''),
            product_data.get('weight_kg', 0),
            certs_json
        ))
        
        conn.commit()
        return {"status": "success", "product_id": product_data['product_id']}
    
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
