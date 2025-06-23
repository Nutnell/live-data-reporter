import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from astronauts import fetch_astronauts
from iss_tracker import fetch_iss_position
from news_or_stock import fetch_ibm_stock_price

load_dotenv()

LOG_FILE_PATH = "logs.txt"

# Logs an action with a timestamp and status to the logs.txt file.
def log_action(module, action, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {module} - {action} - {status}\n"
    try:
        with open(LOG_FILE_PATH, "a") as f:
            f.write(log_entry)
    except IOError as e:
        print(f"Error writing to log file: {e}")

# Displays the main menu options to the user.
def display_menu():
    print("\n--- Live Data Reporter Menu ---")
    print("1. View Astronauts in Space")
    print("2. Track ISS Real-time Position")
    print("3. View IBM 5-min Stock Price")
    print("4. Exit")
    print("-------------------------------")

 # Runs the main application loop, displaying the menu and handling user input
def run_application():
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            fetch_astronauts(log_action)
        elif choice == "2":
            fetch_iss_position(log_action)
        elif choice == "3":
            # Call the stock fetching function
            fetch_ibm_stock_price(log_action)
        elif choice == "4":
            print("Exiting Live Data Reporter. Goodbye!")
            log_action("Main Application", "Exit Program", "Success")
            sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            log_action(
                "Main Application", "Invalid Menu Choice", f"User input: {choice}"
            )

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    run_application()
