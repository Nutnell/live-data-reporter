import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define constants
# --- NewsAPI Configuration ---
NEWS_API_BASE_URL = "https://newsapi.org/v2/top-headlines"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Retrieve API key from environment variables

# --- Alpha Vantage Configuration ---
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = os.getenv(
    "ALPHA_VANTAGE_API_KEY"
)

# Fetches the top 3 U.S. business news headlines from NewsAPI, logs the API request, and displays them in the console.
def fetch_top_us_business_news(logger_func):
    if not NEWS_API_KEY:
        print(
            "Error: NEWS_API_KEY not found in .env file. Please get one from newsapi.org."
        )
        logger_func("News Module", "API Key Check", "Failure: NEWS_API_KEY missing")
        return

    print("Fetching top U.S. business news...")
    params = {
        "country": "us",
        "category": "business",
        "pageSize": 3,  # Fetch top 3 headlines
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(NEWS_API_BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        articles = data.get("articles", [])

        logger_func("News Module", "Fetch News API Call", "Success")

        print("\n--- Top 3 U.S. Business Headlines ---")
        if articles:
            for i, article in enumerate(articles):
                title = article.get("title", "N/A")
                source = article.get("source", {}).get("name", "N/A")
                url = article.get("url", "#")
                print(f"{i+1}. {title}")
                print(f"   Source: {source}")
                print(f"   Link: {url}\n")
        else:
            print("No business headlines found.")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        logger_func("News Module", "Fetch News API Call", f"Failure: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from NewsAPI: {e}")
        logger_func("News Module", "Decode News JSON", f"Failure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logger_func("News Module", "Unexpected Error", f"Failure: {e}")

# Fetches the latest 5-minute stock price for IBM from Alpha Vantage, logs the API request, and displays the latest open price in the console.
def fetch_ibm_stock_price(logger_func):
    if not ALPHA_VANTAGE_API_KEY:
        print(
            "Error: ALPHA_VANTAGE_API_KEY not found in .env file. Please get one from alphavantage.co."
        )
        logger_func(
            "Stock Module", "API Key Check", "Failure: ALPHA_VANTAGE_API_KEY missing"
        )
        return

    print("Fetching IBM 5-minute stock price...")
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": "IBM",
        "interval": "5min",
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()

        # Alpha Vantage often returns an 'Error Message' or 'Note' key on failure/limits
        if "Error Message" in data:
            error_msg = data["Error Message"]
            print(f"Alpha Vantage API Error: {error_msg}")
            logger_func("Stock Module", "Fetch Stock API Call", f"Failure: {error_msg}")
            return
        if "Note" in data:  # API rate limit message
            note_msg = data["Note"]
            print(
                f"Alpha Vantage API Note: {note_msg}. Please wait a minute and try again."
            )
            logger_func("Stock Module", "Fetch Stock API Call", f"Failure: {note_msg}")
            return

        time_series = data.get("Time Series (5min)")

        if not time_series:
            print(
                "No 5-minute time series data found for IBM. API response might be empty or malformed."
            )
            logger_func(
                "Stock Module", "Process Stock Data", "Failure: No time series data"
            )
            return

        # Get the latest timestamp (first key in the ordered dict)
        latest_timestamp = list(time_series.keys())[0]
        latest_data = time_series[latest_timestamp]

        open_price = latest_data.get("1. open")
        high_price = latest_data.get("2. high")
        low_price = latest_data.get("3. low")
        close_price = latest_data.get("4. close")
        volume = latest_data.get("5. volume")

        logger_func("Stock Module", "Fetch Stock API Call", "Success")

        print(f"\n--- IBM Stock Price (5-min) as of {latest_timestamp} ---")
        print(f"  Open: ${open_price}")
        print(f"  High: ${high_price}")
        print(f"  Low: ${low_price}")
        print(f"  Close: ${close_price}")
        print(f"  Volume: {volume}")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data: {e}")
        logger_func("Stock Module", "Fetch Stock API Call", f"Failure: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from Alpha Vantage: {e}")
        logger_func("Stock Module", "Decode Stock JSON", f"Failure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logger_func("Stock Module", "Unexpected Error", f"Failure: {e}")


if __name__ == "__main__":
    def dummy_log_action(module, action, status):
        print(f"[DUMMY LOG] {module} - {action} - {status}")

    # Fetch top U.S. business news
    fetch_top_us_business_news(dummy_log_action)

    # Fetch IBM stock price
    fetch_ibm_stock_price(dummy_log_action)
    
  
