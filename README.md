# Privacy Scanner

A web scraping application that extracts quotes from quotes.toscrape.com, stores them in a SQLite database, and exposes the data via a FastAPI REST API.

## Why I Built This

This project was built to demonstrate proficiency in Python, web scraping, FastAPI, SQL, and production-ready coding practices as part of my application for the Junior Software Engineer position at 360 Privacy.

## Technologies Used

- **Python 3.12**
- **FastAPI** - REST API framework
- **BeautifulSoup4** - Web scraping and HTML parsing
- **SQLite** - Database storage
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Features

- Web scraper with rate limiting and user-agent rotation
- Duplicate detection (prevents re-inserting the same quotes)
- RESTful API with automatic documentation
- Proper logging and error handling
- Modular architecture with separation of concerns

## Project Structure
```
privacy-scanner/
├── config.py          # Configuration settings
├── models.py          # Pydantic data models
├── database.py        # Database operations
├── scraper.py         # Web scraping logic
├── main.py            # FastAPI application
├── requirements.txt   # Python dependencies
└── README.md
```

## Setup Instructions

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd privacy-scanner
```

2. **Create a virtual environment**
```bash
   python -m venv venv
```

3. **Activate the virtual environment**
   - Windows: `.\venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Run the application**
```bash
   uvicorn main:app --reload
```

6. **Access the API**
   - API Documentation: http://127.0.0.1:8000/docs
   - Base URL: http://127.0.0.1:8000

## API Endpoints

### `POST /scan`
Triggers the web scraper to fetch quotes from the target site.

**Response:**
```json
{
  "message": "Scan completed successfully",
  "status": "success"
}
```

### `GET /results`
Returns all scraped quotes from the database.

**Response:**
```json
[
  {
    "text": "The world as we have created it...",
    "author": "Albert Einstein",
    "tags": ["change", "deep-thoughts", "thinking"]
  }
]
```

## Known Limitations

- Currently scrapes only the first page of quotes.toscrape.com
- SQLite database is suitable for development but would need migration to PostgreSQL for production scale
- No authentication/authorization implemented

## Future Improvements

- Add pagination support for scraping multiple pages
- Implement background task processing for long-running scrapes
- Add filtering and search capabilities to the API
- Deploy to AWS with proper production database
- Add monitoring and alerting

## License

MIT