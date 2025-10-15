# ARGUS Defense Intelligence Dashboard - Live Monitoring Guide

## 🛡️ Enhanced Real-Time Features

Your ARGUS Defense Intelligence Dashboard now includes powerful real-time monitoring capabilities!

## 🚀 Quick Start - Live Monitoring

### Option 1: Automated Live Monitoring (Recommended)
```powershell
# Run this script to start everything automatically
.\start_live_monitoring.ps1
```

### Option 2: Manual Setup
```powershell
# Terminal 1: Start Live Monitor (data collection + processing)
.venv\Scripts\python.exe live_monitor.py

# Terminal 2: Start Dashboard (in a separate terminal)
.venv\Scripts\python.exe -m streamlit run defense_dashboard.py --server.port 8502
```

## 🎯 New Live Features in Dashboard

### 🔴 Auto-Refresh Controls
- **Enable Auto-Refresh**: Checkbox in sidebar (refreshes every 30 seconds)
- **Manual Refresh**: "🔄 Refresh Now" button for instant updates
- **Live Status Indicator**: Shows current time and live connection status

### 🚀 Live Monitoring Controls
- **Start Live Monitor**: Launches background news scraping
- **Process New Data**: Manually processes newly collected data
- **New Data Detection**: Automatic notification when new data is available

### 📊 Real-Time Status
- **Live Dashboard Header**: Shows "🔴 LIVE" indicator with timestamp
- **Auto-Refresh Timer**: Countdown showing next refresh in sidebar
- **System Status**: Real-time database and monitoring status

## 📈 How Live Updates Work

1. **Background Scraping**: Continuously monitors defense news sources
2. **Smart Detection**: Automatically detects new data files
3. **Auto-Processing**: Processes new intelligence data automatically
4. **Live Database**: Updates defense_intelligence.db in real-time
5. **Dashboard Sync**: Dashboard auto-refreshes to show latest data

## 🎛️ Dashboard Controls

### Sidebar Controls:
- ✅ **Enable Auto-Refresh**: Automatic 30-second updates
- 🔄 **Refresh Now**: Manual immediate refresh
- 🚀 **Start Live Monitor**: Begin background monitoring
- ⏹️ **Process New Data**: Process collected data files
- 🎯 **Generate Defense Report**: Create detailed analysis
- 🔍 **Start Monitoring**: Launch continuous news monitoring

### Live Status Indicators:
- 🟢 **New data detected!** - New intelligence available
- 🟡 **System monitoring...** - Normal operation
- ⏱️ **Next Refresh Timer** - Countdown to auto-refresh

## 📊 Live Data Sources

The system continuously monitors:

### Indian Defense Sources:
- Indian Defence News (defence, security, terrorism, border-security)
- Financial Express Defence
- Economic Times Defence
- Hindustan Times India News
- Times of India India

### International Sources:
- BBC Security
- Reuters World
- CNN Security

## 🔧 Troubleshooting Live Features

### Dashboard Not Auto-Refreshing:
1. Ensure "Enable Auto-Refresh" is checked
2. Click "🔄 Refresh Now" to force update
3. Check if live_monitor.py is running

### No New Data Detected:
1. Verify live_monitor.py is running
2. Check internet connection
3. Some news sources may be temporarily unavailable

### Live Monitor Not Working:
1. Restart live_monitor.py
2. Check if defense_scraper.py is executable
3. Verify virtual environment is activated

## 💡 Best Practices

1. **Always enable auto-refresh** for live intelligence
2. **Run live_monitor.py** in background for continuous updates
3. **Check system status** regularly in sidebar
4. **Process new data** when notified by dashboard
5. **Monitor threat levels** for real-time alerts

## 🎯 Advanced Usage

### Continuous Monitoring:
```powershell
# For 24/7 monitoring (runs until stopped)
.venv\Scripts\python.exe live_monitor.py
```

### Manual Data Processing:
```powershell
# Process specific data batch
.venv\Scripts\python.exe defense_intelligence.py
```

### Generate Detailed Reports:
```powershell
# Create comprehensive intelligence report
.venv\Scripts\python.exe defense_intelligence.py --report
```

## 🛡️ Security Features

- **Real-time threat analysis**
- **Automatic entity extraction**
- **Live alert generation**
- **Threat level assessment**
- **Intelligence categorization**

Your ARGUS Defense Intelligence Dashboard is now a fully live, real-time intelligence monitoring system! 🚀

Access the dashboard at: http://localhost:8502