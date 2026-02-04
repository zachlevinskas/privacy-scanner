import requests
from bs4 import BeautifulSoup
import time
from models import Quote
from database import insert_quote
from config import TARGET_URL, RATE_LIMIT_SECONDS, USER_AGENT
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_quotes():
    """
    Scrapes quotes from the target URL and stores them in the database.
    Includes rate limiting and error handling for robust operation.
    """
    try:
        logger.info(f"Scraping {TARGET_URL}...")
        
        # Send HTTP request with timeout to prevent hanging
        response = requests.get(TARGET_URL, headers={"User-Agent": USER_AGENT}, timeout=10)
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes_divs = soup.find_all('div', class_='quote')
        
        # Verify quotes were found (site structure may change)
        if not quotes_divs:
            logger.warning("No quotes found - site structure may have changed")
            return
        
        logger.info(f"Found {len(quotes_divs)} quotes")
        
        # Process each quote individually with error isolation
        for quote_div in quotes_divs:
            try:
                # Extract quote components from HTML structure
                quote_text = quote_div.find('span', class_='text').get_text()
                quote_author = quote_div.find('small', class_='author').get_text()
                quote_tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
                
                # Create Quote object and save to database
                quote = Quote(
                    text=quote_text,
                    author=quote_author,
                    tags=quote_tags
                )
                insert_quote(quote)
                logger.debug(f"Processed: {quote.author} - {quote.text[:50]}...")
                
            except AttributeError as e:
                # Skip individual quotes that fail to parse (malformed HTML)
                logger.error(f"Failed to parse quote element: {e}")
                continue
            
        # Rate limiting to avoid overwhelming the server
        time.sleep(RATE_LIMIT_SECONDS)
        logger.info("Scraping complete")
        
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout while scraping {TARGET_URL}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during scraping: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")