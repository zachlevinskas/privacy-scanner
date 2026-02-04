import requests
from bs4 import BeautifulSoup
import time
from models import Quote
from database import insert_quote
from config import TARGET_URL, RATE_LIMIT_SECONDS, USER_AGENT
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_quotes():
    try:
        #Connect to target url and pull in HTML body
        logger.info(f"Scraping {TARGET_URL}...")
        response = requests.get(TARGET_URL, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        
        #Store found data into iterable data
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes_divs = soup.find_all('div', class_='quote')
        
        logger.info(f"Found {len(quotes_divs)} quotes")
        
        #Iterate through divs and insert into DB when they match quote defined schema
        for quote_div in quotes_divs:
            quote_text = quote_div.find('span', class_='text').get_text()
            quote_author = quote_div.find('small', class_='author').get_text()
            quote_tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
            
            quote = Quote(
                text=quote_text,
                author=quote_author,
                tags=quote_tags
            )
            insert_quote(quote)
            logger.debug(f"Inserted: {quote.author} - {quote.text[:50]}...")

        #Rate limit from config 
        time.sleep(RATE_LIMIT_SECONDS)
        logger.info("Scraping complete")
        
        #Catch any errors during scraping and save to log
    except Exception as e:
        logger.error(f"Error during scraping: {e}")


if __name__ == "__main__":
    logger.info("Scraper module loaded successfully")
    scrape_quotes()