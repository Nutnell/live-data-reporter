import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define constants
ASTRONAUTS_API_URL = "http://api.open-notify.org/astros.json"
DATA_FILE_PATH = "data/iss_data.txt"

# Fetches the list of astronauts currently in space from the Open Notify API then logs the API request and saves astronaut data to data/iss_data.txt.
def fetch_astronauts(logger_func):
    print("Fetching astronauts data...")
    try:
        response = requests.get(ASTRONAUTS_API_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        number_of_people = data.get("number", 0)
        people = data.get("people", [])

        logger_func("Astronauts Module", "Fetch Astronauts API Call", "Success")

        # Prepare data for saving and printing
        output_lines = [
            f"--- Astronauts in Space ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---",
            f"Total astronauts: {number_of_people}",
        ]
        if people:
            output_lines.append("Astronauts currently in space:")
            for person in people:
                output_lines.append(
                    f"  - Name: {person['name']}, Craft: {person['craft']}"
                )
        else:
            output_lines.append("No astronauts data available.")
        output_lines.append("-" * 50)  # Separator for readability

        # Save to file
        try:
            with open(DATA_FILE_PATH, "a") as f:
                for line in output_lines:
                    f.write(line + "\n")
            print(f"Astronauts data saved to {DATA_FILE_PATH}")
            logger_func("Astronauts Module", "Save Astronauts Data", "Success")
        except IOError as e:
            print(f"Error saving astronauts data to file: {e}")
            logger_func("Astronauts Module", "Save Astronauts Data", f"Failure: {e}")

        # Print to console
        for line in output_lines[1:]:  # Skip the first timestamp line for console print
            print(line)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching astronauts data: {e}")
        logger_func("Astronauts Module", "Fetch Astronauts API Call", f"Failure: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from astronauts API: {e}")
        logger_func("Astronauts Module", "Decode Astronauts JSON", f"Failure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logger_func("Astronauts Module", "Unexpected Error", f"Failure: {e}")


if __name__ == "__main__":
    def dummy_log_action(module, action, status):
        print(f"[DUMMY LOG] {module} - {action} - {status}")
        fetch_astronauts(dummy_log_action)
