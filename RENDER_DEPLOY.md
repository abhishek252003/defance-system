# 🎯 FREE Render Deployment Guide

## Why Render?
- 750 hours/month free (enough for 24/7)
- Docker support included
- Automatic deployments from GitHub
- Custom domains on free tier

## Step 1: Prepare Dockerfile
Your existing `Dockerfile` works perfectly!

## Step 2: Deploy to Render
1. Go to https://render.com
2. Sign up with GitHub (free)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Select "Docker" as environment
6. Deploy!

## Configuration:
- **Build Command**: `docker build -t argus .`
- **Start Command**: `python -m streamlit run defense_dashboard.py --server.port=$PORT --server.address=0.0.0.0`
- **Port**: Auto-detected

## Free Tier Limits:
✅ 750 hours/month (24/7 usage)
✅ 512MB RAM
✅ 1 vCPU
✅ Custom domains
✅ SSL certificates

## Perfect for ARGUS because:
- Supports your Docker setup
- More RAM than Streamlit Cloud
- Doesn't sleep as often
- Professional appearance