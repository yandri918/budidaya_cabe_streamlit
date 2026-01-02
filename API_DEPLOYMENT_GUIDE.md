# QR Product API Deployment Guide

## Overview
FastAPI backend for QR product traceability, deployed alongside Streamlit.

## Architecture
```
Streamlit App → SQLite DB ← FastAPI API
                    ↓
            Vercel Website (calls API)
```

## Deployment Options

### Option 1: Railway (Recommended)
1. Create account at railway.app
2. New Project → Deploy from GitHub
3. Select `budidaya_cabe_streamlit` repository
4. Set start command: `uvicorn api_main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (if needed)
6. Deploy!

**URL:** `https://your-app.railway.app`

### Option 2: Render
1. Create account at render.com
2. New Web Service
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn api_main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

**URL:** `https://your-app.onrender.com`

### Option 3: Local Testing
```bash
cd budidaya_cabe_streamlit
uvicorn api_main:app --reload --port 8000
```

**URL:** `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
Response: {"status": "ok", "message": "QR Product API is running"}
```

### Get Product by ID
```
GET /api/product/{product_id}
Example: GET /api/product/CHI-H001-B001-20260102
Response: {
    "productId": "CHI-H001-B001-20260102",
    "harvestDate": "2026-01-02",
    "farmLocation": "Garut, Jawa Barat",
    "farmerName": "andriyanto",
    "grade": "Grade B",
    "weight": "10 kg",
    "batchNumber": "B001",
    "certifications": ["Organic", "GAP"],
    "timeline": [...]
}
```

### Get All Products
```
GET /api/products
Response: [array of products]
```

### Create Product
```
POST /api/product
Body: {
    "product_id": "CHI-H001-B001-20260102",
    "harvest_date": "2026-01-02",
    "farmer_name": "andriyanto",
    ...
}
```

## Update Vercel Website

After deploying API, update `cabe_qr_vercel/index.html`:

```javascript
// Replace hardcoded database with API call
async function verifyProduct() {
    const productId = document.getElementById('productId').value.trim();
    
    // Call API
    const API_URL = 'https://your-api-url.railway.app'; // UPDATE THIS
    
    try {
        const response = await fetch(`${API_URL}/api/product/${productId}`);
        
        if (response.ok) {
            const product = await response.json();
            displayProduct(product);
        } else {
            showError('Product not found');
        }
    } catch (error) {
        console.error('API Error:', error);
        showError('Failed to connect to API');
    }
}
```

## Testing

1. **Test API locally:**
   ```bash
   curl http://localhost:8000/
   curl http://localhost:8000/api/product/CHI-H001-B001-20260102
   ```

2. **Test from Vercel:**
   - Generate QR in Module 19
   - Scan QR → Vercel website
   - Should call API and display real data

## Troubleshooting

**Database not found:**
- Ensure `data/budidaya_cabe.db` exists
- Check file permissions

**CORS errors:**
- API already configured to allow all origins
- Check browser console for errors

**Product not found:**
- Generate QR in Module 19 first
- Check database has qr_products table
- Verify product_id matches

## Next Steps

1. Deploy API to Railway/Render
2. Get API URL
3. Update Vercel website with API URL
4. Test end-to-end flow
5. Deploy Vercel website

## Production Checklist

- [ ] API deployed and running
- [ ] Database accessible
- [ ] CORS configured
- [ ] Vercel website updated with API URL
- [ ] End-to-end testing complete
- [ ] Error handling tested
- [ ] Performance acceptable

## Support

API Documentation: `https://your-api-url/docs` (FastAPI auto-docs)
