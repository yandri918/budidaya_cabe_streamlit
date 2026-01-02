# QR Product API Deployment Guide

## Overview
FastAPI backend for QR product traceability, deployed on **Streamlit Cloud** alongside main Streamlit app.

## Architecture
```
Streamlit App (Cloud) → SQLite DB ← FastAPI API (Cloud)
                           ↓
                   Vercel Website (calls API)
```

## Deployment Options

### Option 1: Streamlit Cloud (Recommended) ⭐

**Why Streamlit Cloud?**
- ✅ Same server = share SQLite database directly
- ✅ Free tier available
- ✅ Already familiar with platform
- ✅ No additional setup needed
- ✅ Same deployment workflow

**Steps:**

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Login with GitHub

2. **Deploy New App:**
   - Click "New app"
   - Repository: `budidaya_cabe_streamlit`
   - Branch: `main`
   - Main file path: `api_main.py` ⚠️ (not app.py)
   - App URL: Choose custom URL like `budidaya-cabe-api`

3. **Advanced Settings (Optional):**
   - Python version: 3.9+
   - No additional secrets needed

4. **Deploy!**
   - Click "Deploy"
   - Wait ~2 minutes

5. **Get API URL:**
   ```
   https://budidaya-cabe-api.streamlit.app
   ```

**Important Notes:**
- Main Streamlit app: `https://budidaya-cabe.streamlit.app`
- API app: `https://budidaya-cabe-api.streamlit.app`
- Both share same database file in workspace
- Both are in same GitHub repo

---

### Option 2: Railway (Alternative)

If you prefer separate hosting:

1. Create account at railway.app
2. New Project → Deploy from GitHub
3. Select `budidaya_cabe_streamlit` repository
4. Start command: `uvicorn api_main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

**URL:** `https://your-app.railway.app`

---

### Option 3: Local Testing

```bash
cd budidaya_cabe_streamlit
uvicorn api_main:app --reload --port 8000
```

**URL:** `http://localhost:8000`

---

## API Endpoints

### Health Check
```
GET /
Response: {
    "status": "ok",
    "message": "QR Product API is running",
    "database": "connected"
}
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

---

## Update Vercel Website

After deploying API to Streamlit Cloud:

1. **Edit `cabe_qr_vercel/index.html` line 471-472:**

```javascript
// BEFORE:
const API_URL = 'https://your-api-url.railway.app';
const USE_API = false;

// AFTER:
const API_URL = 'https://budidaya-cabe-api.streamlit.app'; // YOUR STREAMLIT CLOUD URL
const USE_API = true; // ENABLE API
```

2. **Commit and push:**
```bash
cd cabe_qr_vercel
git add index.html
git commit -m "Enable API integration with Streamlit Cloud"
git push origin main
```

3. **Vercel auto-deploys** (~1 minute)

---

## Testing

### 1. Test API Directly

Visit in browser:
```
https://budidaya-cabe-api.streamlit.app/
```

Should see:
```json
{
    "status": "ok",
    "message": "QR Product API is running"
}
```

### 2. Test Product Endpoint

Visit:
```
https://budidaya-cabe-api.streamlit.app/docs
```

FastAPI auto-generates interactive documentation!

### 3. End-to-End Test

1. **Generate QR in Module 19:**
   - Open: https://budidaya-cabe.streamlit.app
   - Go to Module 19
   - Generate QR with real data
   - Product ID: `CHI-H001-B001-20260102110018`

2. **Scan QR or visit Vercel:**
   - https://cabe-q-r-vercel.vercel.app/
   - Enter Product ID
   - Click Verify

3. **Verify Real Data:**
   - ✅ Farmer name matches
   - ✅ Grade matches
   - ✅ Timeline shows real data

---

## Troubleshooting

### API shows "Database not found"
**Solution:** Ensure both apps deployed from same repo and branch. Streamlit Cloud shares workspace.

### CORS errors in browser
**Solution:** API already configured to allow all origins. Check browser console for actual error.

### Product not found
**Solution:**
1. Generate QR in Module 19 first
2. Check database has qr_products table
3. Verify product_id matches exactly

### Streamlit Cloud deployment fails
**Solution:**
1. Check `api_main.py` syntax
2. Ensure `requirements.txt` has FastAPI dependencies
3. Check Streamlit Cloud logs

---

## Quick Start Guide

**5-Minute Setup:**

1. **Deploy API to Streamlit Cloud** (2 min)
   - New app → `api_main.py`
   - Copy URL

2. **Update Vercel** (1 min)
   - Edit `index.html` line 471-472
   - Set API_URL and USE_API = true
   - Push to GitHub

3. **Test** (2 min)
   - Generate QR in Module 19
   - Scan QR → Verify data matches

**Done!** 🎉

---

## Production Checklist

- [x] API code ready (`api_main.py`)
- [x] Database schema created
- [x] Streamlit saves to database
- [x] Vercel website API-ready
- [ ] **Deploy API to Streamlit Cloud** ← DO THIS
- [ ] **Update Vercel with API URL** ← THEN THIS
- [ ] **Test end-to-end** ← FINALLY THIS

---

## Support

- **API Documentation:** `https://your-api.streamlit.app/docs` (FastAPI auto-docs)
- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Issues:** Check Streamlit Cloud logs in dashboard


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
