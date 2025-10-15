# 🛡️ ARGUS Defense Intelligence System - Deployment Guide

## 🚀 Quick Start (Recommended)

### Option 1: Automated Setup
```bash
# Clone or download ARGUS
# Navigate to the argus directory
python setup.py
```

### Option 2: Docker Deployment (Production Ready)
```bash
# Build and run with Docker
docker-compose up -d

# Access dashboard at: http://localhost:8502
```

### Option 3: Manual Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
python -m streamlit run defense_dashboard.py
```

## 📋 System Requirements

### Minimum Requirements
- Python 3.8+
- 2GB RAM
- 1GB free disk space
- Internet connection

### Recommended for Production
- Python 3.11+
- 4GB RAM
- 5GB free disk space
- SSD storage
- Linux/Docker environment

## 🔧 Configuration

### Environment Variables
```bash
ARGUS_PORT=8502              # Dashboard port
ARGUS_HOST=0.0.0.0          # Host binding
ARGUS_REFRESH_INTERVAL=30    # Auto-refresh seconds
ARGUS_AUTH=false            # Enable authentication
```

### Custom Configuration
Edit `config.py` to customize:
- News sources
- Threat keywords
- Processing settings
- Security options

## 🐳 Production Deployment

### Docker (Recommended)
```bash
# Build image
docker build -t argus-defense .

# Run container
docker run -d -p 8502:8502 \
  -v $(pwd)/defense_data:/app/defense_data \
  argus-defense
```

### Cloud Deployment
- **AWS**: Use ECS or EC2 with Docker
- **Google Cloud**: Use Cloud Run or GKE
- **Azure**: Use Container Instances or AKS
- **Heroku**: Use container deployment

## 📊 Features for All Users

### ✅ Ready for Deployment
- Real-time threat monitoring
- Web-based dashboard
- Automated data processing
- SQLite database (no setup needed)
- Multi-platform support
- Docker containerization

### 🎯 User-Friendly Features Added
- One-click setup script
- Automatic dependency management
- Configuration management
- Health monitoring
- Error handling and logging
- Clear documentation

## 🔒 Security Considerations

### For Production Use:
1. Enable authentication in `config.py`
2. Use HTTPS with reverse proxy
3. Implement rate limiting
4. Regular security updates
5. Monitor access logs

## 🆘 Troubleshooting

### Common Issues:
- **Port conflicts**: Change ARGUS_PORT
- **Memory issues**: Reduce batch size in config
- **Permission errors**: Run with appropriate permissions
- **Network issues**: Check firewall settings

### Support:
- Check `logs/argus.log` for detailed errors
- Ensure all dependencies are installed
- Verify Python version compatibility

## 📈 Scaling for Multiple Users

### Performance Optimizations:
- Use Docker for consistent deployment
- Implement caching mechanisms
- Add load balancing for high traffic
- Use external database for large datasets
- Monitor resource usage

Your ARGUS system is now production-ready! 🎉