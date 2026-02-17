import subprocess, sys
from pathlib import Path
import warnings
import pandas as pd

def retrieve_submissions_json():
    script_path = Path("data_collection") / "retrieve_submissions_json.py"
    print("Retrieving submissions JSON...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Retrieved submissions JSON")
    except Exception as e:
        print("Failed to retrieve submissions JSON")
        raise e
    
def retrieve_financial_json():
    script_path = Path("data_collection") / "retrieve_financial_json.py"
    print("Retrieving financial JSON...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Retrieved financial JSON")
    except Exception as e:
        print("Failed to retrieve financial JSON")
        raise e

def get_filing_dates():
    script_path = Path("data_collection") / "get_filing_dates.py"
    print("Getting filing dates...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Retrieved filing dates")
    except Exception as e:
        print("Failed to retrieve filing dates")
        raise e
    
def get_stock_prices():
    script_path = Path("data_collection") / "get_stock_prices.py"
    print("Getting stock prices...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Retrieved stock prices")
    except Exception as e:
        print("Failed to retrieve stock prices")
        raise e
    
def get_financials():
    script_path = Path("data_collection") / "get_financials.py"
    print("Getting financials...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Retrieved financials")
    except Exception as e:
        print("Failed to retrieve financials")
        raise e
    
def cleanup_data():
    script_path = Path("processing") / "cleanup_data.py"
    print("Starting to clean up data...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Finished cleaning up data")
    except Exception as e:
        print("Failed to clean up data")
        raise e
    
def modeling():
    script_path = Path("modeling") / "modeling.py"
    print("Starting modeling...")
    try:
        subprocess.run([sys.executable, script_path])
        print("Finished modeling")
    except Exception as e:
        print("Failed to model")
        raise e

if __name__ == "__main__":
    print("Runner starting up...")


    # data retrieval
    retrieve_submissions_json()
    retrieve_financial_json()

    # parsing
    get_filing_dates()
    get_stock_prices()
    get_financials()

    # cleanup for modeling
    cleanup_data()

    # model training + deployment
    modeling()

    print("Runner shutting down up...")
