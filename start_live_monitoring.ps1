# ARGUS Defense Live Monitoring Script
# This script starts both the defense scraper and dashboard for live monitoring

Write-Host "🛡️  ARGUS Defense Intelligence Live Monitoring" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found. Please run setup_env.py first" -ForegroundColor Red
    exit 1
}

# Function to start defense scraper in background
function Start-DefenseScraper {
    Write-Host "🔍 Starting defense news scraper..." -ForegroundColor Yellow
    
    $scraperJob = Start-Job -ScriptBlock {
        param($workingDir)
        Set-Location $workingDir
        & ".venv\Scripts\python.exe" "defense_scraper.py" "--monitor"
    } -ArgumentList (Get-Location)
    
    return $scraperJob
}

# Function to process collected data
function Process-DefenseData {
    Write-Host "📊 Processing defense intelligence data..." -ForegroundColor Yellow
    
    try {
        & ".venv\Scripts\python.exe" "defense_intelligence.py"
        Write-Host "✅ Data processing completed" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Data processing failed: $_" -ForegroundColor Red
        return $false
    }
}

# Start the monitoring system
Write-Host "🚀 Starting live monitoring system..." -ForegroundColor Green

# Start scraper in background
$scraperJob = Start-DefenseScraper

# Wait a moment for scraper to initialize
Start-Sleep -Seconds 5

# Process initial data if available
if (Test-Path "defense_data\*.json") {
    Write-Host "📁 Found existing data, processing..." -ForegroundColor Blue
    Process-DefenseData
}

# Start the dashboard
Write-Host "🖥️  Starting defense dashboard..." -ForegroundColor Green
Write-Host "Dashboard will be available at: http://localhost:8502" -ForegroundColor Cyan

try {
    & ".venv\Scripts\python.exe" -m streamlit run defense_dashboard.py --server.port 8502
} catch {
    Write-Host "❌ Dashboard failed to start: $_" -ForegroundColor Red
} finally {
    # Clean up background jobs
    if ($scraperJob) {
        Write-Host "🛑 Stopping background scraper..." -ForegroundColor Yellow
        Stop-Job $scraperJob
        Remove-Job $scraperJob
    }
    Write-Host "👋 Live monitoring stopped" -ForegroundColor Cyan
}