from fastapi import FastAPI, HTTPException
from database import init_db, get_all_quotes
from scraper import scrape_quotes
from models import Quote
from typing import List
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()
    logger.info("Database initialized")
    
@app.post("/scan")
def trigger_scan():
    try:
        scrape_quotes()
        logger.info("Scan endpoint triggered successfully")
        return {"message": "Scan completed successfully", "status": "success"}
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/results", response_model=List[Quote])
def get_results():
    try:
        quotes = get_all_quotes()
        logger.info(f"Retrieved {len(quotes)} quotes")
        return quotes
    except Exception as e:
        logger.error(f"Failed to retrieve quotes: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")