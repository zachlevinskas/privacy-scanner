from fastapi import FastAPI, HTTPException
from database import init_db, get_all_quotes
from scraper import scrape_quotes
from models import Quote
from typing import List
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Privacy Scanner API",
    description="Web scraping API that extracts quotes and exposes them via REST endpoints",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    """
    Runs on application startup to initialize the database.
    Creates the quotes table if it doesn't already exist.
    """
    init_db()
    logger.info("Database initialized")

@app.get("/")
def health_check():
    """
    Health check endpoint for monitoring service status.
    
    Returns:
        dict: Service status, name, and version information
    """
    return {
        "status": "healthy",
        "service": "privacy-scanner",
        "version": "1.0.0"
    }
    
@app.post("/scan")
def trigger_scan():
    """
    Triggers the web scraper to fetch quotes from the target site.
    
    Returns:
        dict: Success message and status
        
    Raises:
        HTTPException: 500 error if scraping fails
    """
    try:
        scrape_quotes()
        logger.info("Scan endpoint triggered successfully")
        return {"message": "Scan completed successfully", "status": "success"}
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/results", response_model=List[Quote])
def get_results():
    """
    Retrieves all scraped quotes from the database.
    
    Returns:
        List[Quote]: Array of all quotes with text, author, and tags
        
    Raises:
        HTTPException: 500 error if database query fails
    """
    try:
        quotes = get_all_quotes()
        logger.info(f"Retrieved {len(quotes)} quotes")
        return quotes
    except Exception as e:
        logger.error(f"Failed to retrieve quotes: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")