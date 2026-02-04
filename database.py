import sqlite3
import json
from models import Quote
from config import DB_PATH
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def init_db():
    """
    Initializes the SQLite database and creates the quotes table if it doesn't exist.
    Called on application startup to ensure database schema is ready.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create quotes table with schema for storing scraped data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def insert_quote(quote: Quote):
    """
    Inserts a quote into the database with duplicate detection.
    Duplicates are identified by matching both text and author exactly.
    
    Args:
        quote (Quote): Pydantic model containing quote data
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if quote already exists to prevent duplicates
    # We consider a quote duplicate if both text and author match exactly
    cursor.execute(
        "SELECT 1 FROM quotes WHERE text = ? AND author = ?",
        (quote.text, quote.author)
    )
    exists = cursor.fetchone()
    
    if exists:
        logger.debug(f"Quote already exists, skipping: {quote.author}")
        conn.close()
        return
    
    # Convert tags list to JSON string for storage (SQLite doesn't support array types)
    tags_json = json.dumps(quote.tags)
    
    # Insert new quote into database
    cursor.execute(
        "INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)",
        (quote.text, quote.author, tags_json)
    )
    
    conn.commit()
    conn.close()


def get_all_quotes():
    """
    Retrieves all quotes from the database and converts them to Quote objects.
    
    Returns:
        List[Quote]: List of all quotes with tags converted back from JSON
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT text, author, tags FROM quotes")
    rows = cursor.fetchall()
    
    quotes = []
    for row in rows:
        # Convert database row to Quote object, deserializing JSON tags
        quote = Quote(
            text=row[0],
            author=row[1],
            tags=json.loads(row[2])  # Convert JSON string back to list
        )
        quotes.append(quote)
    
    conn.close()
    return quotes