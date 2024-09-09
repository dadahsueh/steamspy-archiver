import json
import os
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from steamspy_api import SteamSpyAPI


def save_to_json(df: pd.DataFrame, save_path: str, file_name: str) -> None:
    """Save data to a JSON file with beautification in a specified folder."""
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file_name)

    data = df.to_dict(orient='records')

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def save_to_csv(df: pd.DataFrame, save_path: str, file_name: str) -> None:
    """Save data to a CSV file."""
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file_name)

    df.to_csv(file_path, index=False)


def save_all_data(api: SteamSpyAPI, start_page: int = 0, max_pages: int = 10,
                  save_path: str = 'steamspy-archive', file_format: str = 'json', sleep_padding=10) -> None:
    """Fetch all pages of data and save each page in the specified format."""
    page = start_page

    while page < start_page + max_pages:
        print(f"Fetching page {page}...")

        try:
            data = api.get_all(page)
            # Convert the data to a DataFrame
            df = pd.DataFrame([app.__dict__ for app in data])
            # Save each page's data in the specified format
            if file_format == 'json':
                file_name = f'steam_apps_page_{page}.json'
                save_to_json(df, save_path, file_name)
            elif file_format == 'csv':
                file_name = f'steam_apps_page_{page}.csv'
                save_to_csv(df, save_path, file_name)
            else:
                print(f"Unsupported file format: {file_format}")
                break

            print(f"Page {page} saved to {os.path.join(save_path, file_name)}")
            page += 1
            if page < start_page + max_pages:
                time.sleep(60 + sleep_padding)

        except RuntimeError as e:
            print(f"Failed to fetch page {page}: {e}")
            break  # Exit the loop on failure


# Example usage
if __name__ == "__main__":
    # Path to the msedgedriver executable
    edge_driver_path = './msedgedriver'
    user_agent = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81'
    )
    # Setup WebDriver options
    edge_options = Options()
    edge_options.add_argument(f'--user-agent={user_agent}')

    with SteamSpyAPI(webdriver.Edge(service=Service(edge_driver_path), options=edge_options)) as api_session:
        date_folder = datetime.now().strftime('%y%m%d')
        folder_path = os.path.join('steamspy-archive', date_folder)
        save_all_data(api_session, start_page=0, max_pages=200, save_path=folder_path, file_format='json')
        print("Data fetching completed.")
