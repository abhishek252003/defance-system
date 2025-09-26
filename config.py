#!/usr/bin/env python3
"""
ARGUS Configuration Management
Centralized configuration for easy deployment and customization.
"""

import os
from pathlib import Path

class ARGUSConfig:
    """Configuration settings for ARGUS Defense Intelligence System."""
    
    # System Information
    SYSTEM_NAME = "ARGUS Defense Intelligence System"
    VERSION = "1.0.0"
    DESCRIPTION = "Advanced Reconnaissance and General Understanding System"
    
    # Directories
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "defense_data"
    DATABASE_PATH = BASE_DIR / "defense_intelligence.db"
    
    # Dashboard Settings
    DASHBOARD_PORT = 8502
    DASHBOARD_HOST = "0.0.0.0"  # For deployment, use "localhost" for local only
    AUTO_REFRESH_INTERVAL = 30  # seconds
    
    # Data Processing
    MIN_CONTENT_LENGTH = 50  # Minimum article content length
    MAX_ARTICLES_PER_BATCH = 100  # Process in batches to avoid memory issues
    SUPPORTED_FILE_TYPES = [".json"]
    
    # Threat Classification
    THREAT_KEYWORDS = {
        'HIGH': [
            'terrorist attack', 'imminent threat', 'security breach', 'bomb threat',
            'missile strike', 'cyber attack', 'data breach', 'emergency alert',
            'invasion', 'assassination', 'hijack', 'hostage'
        ],
        'MEDIUM': [
            'security alert', 'military exercise', 'border incident', 'protest',
            'surveillance', 'intelligence report', 'weapon smuggling',
            'suspicious activity', 'security concern'
        ],
        'LOW': [
            'routine patrol', 'training exercise', 'diplomatic meeting',
            'peacekeeping', 'humanitarian aid', 'joint operation'
        ]
    }
    
    # News Sources (can be customized by users)
    NEWS_SOURCES = [
        "https://www.defense.gov/News/",
        "https://indianexpress.com/section/india/",
        "https://timesofindia.indiatimes.com/india",
        "https://www.hindustantimes.com/india-news",
        # Add more sources as needed
    ]
    
    # API Settings (for future integrations)
    API_RATE_LIMIT = 60  # requests per minute
    API_TIMEOUT = 30  # seconds
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = BASE_DIR / "argus.log"
    
    # Security Settings
    ENABLE_AUTHENTICATION = False  # Set to True for production
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # Performance Settings
    CACHE_TIMEOUT = 300  # 5 minutes
    MAX_MEMORY_USAGE = 1024  # MB
    
    @classmethod
    def get_database_url(cls):
        """Get database connection URL."""
        return f"sqlite:///{cls.DATABASE_PATH}"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.BASE_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_dashboard_url(cls):
        """Get dashboard URL."""
        return f"http://{cls.DASHBOARD_HOST}:{cls.DASHBOARD_PORT}"
    
    @classmethod
    def load_from_env(cls):
        """Load configuration from environment variables (for deployment)."""
        cls.DASHBOARD_PORT = int(os.getenv('ARGUS_PORT', cls.DASHBOARD_PORT))
        cls.DASHBOARD_HOST = os.getenv('ARGUS_HOST', cls.DASHBOARD_HOST)
        cls.AUTO_REFRESH_INTERVAL = int(os.getenv('ARGUS_REFRESH_INTERVAL', cls.AUTO_REFRESH_INTERVAL))
        cls.ENABLE_AUTHENTICATION = os.getenv('ARGUS_AUTH', 'false').lower() == 'true'

# Initialize configuration
config = ARGUSConfig()
config.load_from_env()
config.ensure_directories()