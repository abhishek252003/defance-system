# Deployment Options for ARGUS Defense Intelligence System

The ARGUS Defense Intelligence System can be deployed in various environments. This document outlines the different deployment options and their requirements.

## Local Deployment

### Requirements
- Python 3.8+
- 2GB+ RAM
- 100MB+ disk space for initial setup
- Internet connection for scraping

### Steps
1. Clone the repository
2. Run the setup script (`setup.sh` or `setup.bat`)
3. Configure news sources and keywords as needed
4. Run the scraper and intelligence processor
5. Launch the dashboard

## Cloud Deployment Options

### Streamlit Cloud (Recommended for Testing)

**Pros:**
- Free tier available
- Easy deployment
- Automatic SSL
- Built-in collaboration features

**Cons:**
- Limited computational resources
- 1000 CPU hours/month limit
- No persistent file system

**Steps:**
1. Push code to GitHub
2. Create new app on Streamlit Cloud
3. Select the repository and `app.py` as the main file
4. Add requirements in the advanced settings

### Railway

**Pros:**
- Good free tier
- Easy deployment from GitHub
- Persistent storage
- Custom domains

**Cons:**
- Limited resources on free tier
- Sleeps after inactivity

**Steps:**
1. Create `railway.toml` configuration file
2. Push to GitHub
3. Connect Railway to your repository
4. Deploy the application

### Render

**Pros:**
- Free tier available
- Custom domains
- Automatic SSL
- Easy environment variable management

**Cons:**
- Web services sleep after 15 minutes of inactivity on free tier
- Limited build time on free tier

**Steps:**
1. Create `render.yaml` configuration file
2. Push to GitHub
3. Connect Render to your repository
4. Deploy the web service

### Docker Deployment

**Pros:**
- Consistent environment
- Easy scaling
- Platform independence
- Better resource isolation

**Cons:**
- Requires Docker knowledge
- More complex setup

**Steps:**
1. Build the Docker image:
   ```bash
   docker build -t argus-defense .
   ```
2. Run the container:
   ```bash
   docker run -p 8501:8501 argus-defense
   ```

### Self-Hosted Server

**Pros:**
- Full control
- No usage limits
- Persistent storage
- Better performance

**Cons:**
- Requires server management
- Security responsibilities
- Higher cost

**Requirements:**
- Linux server (Ubuntu/Debian recommended)
- 4GB+ RAM
- 10GB+ disk space
- Root access

**Steps:**
1. Set up the server with required dependencies
2. Clone the repository
3. Run the setup script
4. Configure systemd service for automatic startup
5. Set up reverse proxy (nginx/Apache)
6. Configure SSL certificate

## Environment Variables

The system supports the following environment variables:

- `DATABASE_URL`: Path to the SQLite database (default: `defense_intelligence.db`)
- `SCRAPING_INTERVAL`: Time between scraping runs in seconds (default: 3600)
- `DASHBOARD_PORT`: Port for the Streamlit dashboard (default: 8501)

## Scaling Considerations

### For High Traffic
- Use a more robust database (PostgreSQL)
- Implement caching mechanisms
- Use a CDN for static assets
- Consider horizontal scaling

### For Large Data Sets
- Implement database indexing strategies
- Use data archiving for old intelligence
- Consider using a more powerful database engine
- Implement pagination in the dashboard

## Monitoring and Maintenance

### Health Checks
- Monitor database connectivity
- Check scraper functionality
- Verify dashboard availability
- Track system resource usage

### Regular Maintenance
- Database cleanup and optimization
- Update dependencies
- Rotate log files
- Backup critical data

### Backup Strategy
- Regular database backups
- Archive old intelligence data
- Backup configuration files
- Store backups in multiple locations

## Security Considerations

### Data Protection
- Use HTTPS for all communications
- Implement proper authentication if needed
- Regularly update dependencies
- Sanitize all inputs

### Access Control
- Restrict dashboard access if needed
- Use strong passwords for admin interfaces
- Implement rate limiting
- Monitor access logs

## Performance Optimization

### Database Optimization
- Use appropriate indexes
- Regularly vacuum the SQLite database
- Consider upgrading to PostgreSQL for large datasets

### Scraping Optimization
- Adjust concurrent scraping limits
- Implement retry mechanisms
- Use appropriate delays between requests
- Cache frequently accessed data

### Dashboard Optimization
- Implement pagination for large result sets
- Use efficient data loading techniques
- Optimize chart rendering
- Implement lazy loading where appropriate

## Troubleshooting Common Issues

### Database Connection Issues
- Check file permissions
- Verify database file exists
- Ensure sufficient disk space

### Scraping Failures
- Check internet connectivity
- Verify source URLs are accessible
- Check for rate limiting
- Review error logs

### Dashboard Performance
- Check system resources
- Optimize database queries
- Reduce data set sizes
- Implement caching

## Support and Community

For deployment issues, consult:
- GitHub Issues
- Community forums
- Professional support options