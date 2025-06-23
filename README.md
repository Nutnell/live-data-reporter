# Live Data Reporter

This project is a command-line interface (CLI) application that fetches and displays real-time data from various public APIs. It allows users to:
* View a list of astronauts currently in space.
* Track the International Space Station (ISS) in real-time.
* Get the latest stock price for IBM.

All API interactions and data saving operations are logged for monitoring purposes.

## Features

* **Astronauts in Space:** Fetches and displays the names of astronauts currently in space and their spacecraft, saving the data to `data/iss_data.txt`.
* **ISS Tracker:** Fetches and displays the real-time latitude and longitude of the International Space Station, saving the data to `data/iss_data.txt`. Includes a direct Google Maps link for easy visualization.
* **IBM Stock Price:** Fetches and displays the latest 5-minute intraday trading data (Open, High, Low, Close, Volume) for IBM stock using the Alpha Vantage API.
* **Centralized Logging:** All API calls and significant application events are logged to `logs.txt`.
* **Interactive Menu:** A user-friendly command-line menu to easily navigate between data sources.

## Project Structure

live-data-reporter/
├── data/
│   └── iss_data.txt        # Stores fetched astronaut and ISS position data
├── .env.example            # Template for environment variables (API keys)
├── main.py                 # Main application entry point, CLI menu, and centralized logging
├── astronauts.py           # Module for fetching astronaut data
├── iss_tracker.py          # Module for fetching ISS position data
├── news_or_stock.py        # Module for fetching stock (or news) data
├── logs.txt                # Application logs
├── README.md               # This file
└── requirements.txt        # Lists Python package dependencies

## Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/nutnell/live-data-reporter.git](https://github.com/nutnell/live-data-reporter.git)
    cd live-data-reporter
    ```

2.  **Create and activate a virtual environment:**
    It's highly recommended to use a virtual environment to manage dependencies.

    * **macOS/Linux/Git Bash:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows (Command Prompt):**
        ```cmd
        py -m venv venv
        venv\Scripts\activate
        ```
    * **Windows (PowerShell):**
        ```powershell
        py -m venv venv
        .\venv\Scripts\Activate.ps1
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Keys:**
    This project requires API keys for certain functionalities.

    * **Alpha Vantage API Key (for IBM Stock Price):**
        * Go to [https://www.alphavantage.co/](https://www.alphavantage.co/) and get a free API key.
    * **NewsAPI Key (if you chose news over stock):**
        * Go to [https://newsapi.org/](https://newsapi.org/) and get a free API key. *(Note: This project is configured for Alpha Vantage stock data by default).*

    Create a file named `.env` in the root of your `live-data-reporter` directory (next to `main.py`). Add your API keys to this file in the following format:

    ```
    # .env
    ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY
    # NEWS_API_KEY=YOUR_NEWS_API_KEY 
    ```
    **Important:** Do NOT commit your `.env` file to version control. It's already listed in `.gitignore`.

## How to Run

After completing the setup:

1.  **Activate your virtual environment** (if not already active).
2.  **Run the main application script:**
    ```bash
    python main.py
    ```
3.  Follow the on-screen menu to interact with the application.

## Logging

All significant actions (API calls, data saves, errors, menu choices) are logged to `logs.txt` in the root directory of the project.

## Data Storage

Astronauts in space and ISS real-time position data are appended to `data/iss_data.txt`.

## License

[Optional: Add a license, e.g., MIT License]

## Acknowledgments

* [Open Notify API](http://api.open-notify.org/) (for Astronauts in Space and ISS Tracker)
* [Alpha Vantage](https://www.alphavantage.co/) (for Stock Market Data)
# OR
* [NewsAPI](https://newsapi.org/) (for News Headlines)