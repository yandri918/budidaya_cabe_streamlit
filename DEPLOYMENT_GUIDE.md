# 🚀 Deployment Guide - Budidaya Cabai Website

## Prerequisites
- ✅ GitHub repository: https://github.com/yandri918/budidaya_cabe_streamlit
- ✅ Code pushed to `main` branch
- ✅ Streamlit Cloud account (free)

## Step-by-Step Deployment

### 1. Login to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub account
3. Authorize Streamlit to access your repositories

### 2. Create New App
1. Click "New app" button
2. Select repository: `yandri918/budidaya_cabe_streamlit`
3. Select branch: `main`
4. Main file path: `app.py`
5. App URL: Choose custom name (e.g., `budidaya-cabai`)

### 3. Advanced Settings (Optional)
- Python version: 3.9 or higher
- No secrets needed (all data is local)

### 4. Deploy
1. Click "Deploy!" button
2. Wait 2-5 minutes for deployment
3. App will be live at: `https://[your-app-name].streamlit.app`

## Expected Deployment URL
```
https://budidaya-cabai.streamlit.app
```
or
```
https://[custom-name].streamlit.app
```

## Post-Deployment Checklist
- [ ] All pages load correctly
- [ ] Navigation works
- [ ] Calculators function properly
- [ ] Charts render
- [ ] No import errors

## Troubleshooting

### If deployment fails:
1. Check `requirements.txt` is present
2. Verify all imports are correct
3. Check Streamlit Cloud logs
4. Ensure Python version compatibility

### Common Issues:
- **Import errors**: Check all dependencies in requirements.txt
- **File not found**: Verify file paths are relative
- **Slow loading**: Normal for first deployment

## Monitoring
- View logs in Streamlit Cloud dashboard
- Check analytics for usage
- Monitor performance

## Updates
To update the app:
1. Push changes to GitHub
2. Streamlit Cloud auto-deploys (if enabled)
3. Or manually trigger redeploy

## Support
- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io

---

**Deployment Date:** January 1, 2026
**Status:** Ready for deployment ✅
