import sqlite3
import json
from models import Quote
from config import DB_PATH
import logging


#Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)  # Opens/creates the database file
    cursor = conn.cursor()            # Creates a cursor object to execute SQL
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    tags TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()  # Save changes
    conn.close()   # Close connection


def insert_quote(quote: Quote):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if quote already exists
    cursor.execute(
        "SELECT 1 FROM quotes WHERE text = ? AND author = ?",
        (quote.text, quote.author)
    )
    exists = cursor.fetchone()
    
    if exists:
        logger.debug(f"Quote already exists, skipping: {quote.author}")
        conn.close()
        return
    
    # Convert tags list to JSON string
    tags_json = json.dumps(quote.tags)
    
    #Insert to DB
    cursor.execute(
        "INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)",
        (quote.text, quote.author, tags_json)
    )
    
    conn.commit()
    conn.close()


def get_all_quotes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT text, author, tags FROM quotes")
    rows = cursor.fetchall()  # Returns list of tuples
    
    quotes = []  # Empty list to store Quote objects
    for row in rows:
        # row is a tuple: (text, author, tags_json_string)
        quote = Quote(
            text=row[0],
            author=row[1],
            tags=json.loads(row[2])  # Convert JSON string back to list
        )
        quotes.append(quote)
    
    conn.close()
    return quotes
