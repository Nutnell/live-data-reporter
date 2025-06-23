import requests
import json
from datetime import datetime
import time  # For potential future enhancements like live updates.
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

# Define constants
ISS_POSITION_API_URL = "http://api.open-notify.org/iss-now.json"
DATA_FILE_PATH = "data/iss_data.txt"
LOG_FILE_PATH = "logs.txt"

#Logs an action with a timestamp and status to the logs.txt file.
def log_action(module, action, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {module} - {action} - {status}\n"
    try:
        with open(LOG_FILE_PATH, "a") as f:
            f.write(log_entry)
    except IOError as e:
        print(f"Error writing to log file: {e}")

#    Fetches the real-time position of the ISS from the Open Notify API, then logs the API request and saves ISS position data to data/iss_data.txt and also displays the coordinates in the console.
def fetch_iss_position():
    print("Fetching ISS position data...")
    try:
        response = requests.get(ISS_POSITION_API_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses.

        data = response.json()

        # The 'timestamp' in the API response is a Unix timestamp.
        iss_timestamp_unix = data.get("timestamp")
        # Convert Unix timestamp to a readable datetime object
        iss_datetime = (
            datetime.fromtimestamp(iss_timestamp_unix)
            if iss_timestamp_unix
            else datetime.now()
        )

        position = data.get("iss_position", {})
        latitude = position.get("latitude")
        longitude = position.get("longitude")

        if latitude is None or longitude is None:
            raise ValueError("ISS position data is incomplete.")

        log_action("ISS Tracker Module", "Fetch ISS Position API Call", "Success")

        # Prepare data for saving and printing
        output_lines = [
            f"--- ISS Position ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---",
            f"  API Timestamp (UTC): {iss_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"  Latitude: {latitude}",
            f"  Longitude: {longitude}",
            f"  Link for Map (approx): https://maps.google.com/maps?q={latitude},{longitude}&z=5",
            "-" * 50,
        ]

        # Save to file
        try:
            with open(DATA_FILE_PATH, "a") as f:
                for line in output_lines:
                    f.write(line + "\n")
            print(f"ISS position data saved to {DATA_FILE_PATH}")
            log_action("ISS Tracker Module", "Save ISS Position Data", "Success")
        except IOError as e:
            print(f"Error saving ISS position data to file: {e}")
            log_action("ISS Tracker Module", "Save ISS Position Data", f"Failure: {e}")

        # Print to console
        for line in output_lines[1:]:
            print(line)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching ISS position data: {e}")
        log_action("ISS Tracker Module", "Fetch ISS Position API Call", f"Failure: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from ISS position API: {e}")
        log_action("ISS Tracker Module", "Decode ISS JSON", f"Failure: {e}")
    except ValueError as e:
        print(f"Data processing error: {e}")
        log_action("ISS Tracker Module", "Process ISS Data", f"Failure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        log_action("ISS Tracker Module", "Unexpected Error", f"Failure: {e}")


if __name__ == "__main__":
    fetch_iss_position()
