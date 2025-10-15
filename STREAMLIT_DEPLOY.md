# 🚀 FREE Streamlit Cloud Deployment Guide

## Step 1: Prepare Your Repository
1. Create a GitHub account (free)
2. Upload your ARGUS code to GitHub repository
3. Ensure these files are in your repo:
   - `defense_dashboard.py` (main app)
   - `requirements.txt` (dependencies)
   - All your Python files

## Step 2: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `defense_dashboard.py`
6. Click "Deploy"

## Step 3: Your App is Live!
- Free URL: `https://yourapp.streamlit.app`
- Automatic updates when you push code
- Free SSL certificate included
- No server management needed

## Requirements for Streamlit Cloud:
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
requests>=2.31.0
beautifulsoup4>=4.12.0
# Note: Skip spacy/torch for faster deployment
```

## Pros:
✅ 100% Free
✅ One-click deployment
✅ Automatic updates
✅ Built-in SSL
✅ No technical knowledge needed

## Cons:
⚠️ Limited to 1GB RAM
⚠️ Apps sleep after inactivity
⚠️ Public by default