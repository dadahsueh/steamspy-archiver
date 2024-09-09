import json
import logging
import re
from typing import Any, Dict, List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By

from steamspy_dataclasses import SteamApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SteamSpyAPI:
    BASE_URL = 'https://steamspy.com/api.php'

    def __init__(self, driver: webdriver.Remote):
        """Initialize the API client with optional headers."""
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the WebDriver."""
        self.driver.quit()

    def _make_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Helper function to send GET requests to the Steam Spy API."""
        # Construct the URL with parameters
        url = self.BASE_URL + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        self.driver.get(url)

        # Extract JSON from the <div> element
        try:
            div_element = self.driver.find_element(By.XPATH, "//div[@hidden]")
            json_text = div_element.get_attribute('innerHTML')  # Get the inner HTML
            json_data = json.loads(json_text)
        except Exception as e:
            logger.error(f"Error extracting JSON: {e}")
            json_data = {}

        return json_data

    @staticmethod
    def _parse_owners(owners_str: str) -> Tuple[int, int]:
        """Helper function to parse the owners string into a tuple of min and max values."""
        match = re.match(r"(\d[\d,]*)\s*\.\.\s*(\d[\d,]*)", owners_str)
        if match:
            try:
                min_owners = int(match.group(1).replace(',', ''))
                max_owners = int(match.group(2).replace(',', ''))
                return min_owners, max_owners
            except ValueError as e:
                logger.error(f"Error converting owners data: {e}")
        else:
            logger.warning(f"Failed to parse owners string: '{owners_str}'")
        return 0, 0  # Default to (0, 0) if parsing fails

    def _build_steam_app(self, app_data: Dict[str, Any]) -> SteamApp:
        """Helper function to convert raw data into a SteamApp dataclass."""
        # Parse comma-separated strings into lists
        languages = app_data.get('languages')
        if languages:
            languages = [lang.strip() for lang in languages.split(',')]
        else:
            languages = None

        genre = app_data.get('genre')
        if genre:
            genre = [g.strip() for g in genre.split(',')]
        else:
            genre = None

        return SteamApp(
            appid=int(app_data['appid']),
            name=app_data['name'],
            developer=app_data['developer'],
            publisher=app_data['publisher'],
            score_rank=app_data.get('score_rank', ""),
            positive=int(app_data['positive']),
            negative=int(app_data['negative']),
            userscore=int(app_data['userscore']),
            owners=self._parse_owners(app_data.get('owners', "")),
            average_forever=int(app_data['average_forever']),
            average_2weeks=int(app_data['average_2weeks']),
            median_forever=int(app_data['median_forever']),
            median_2weeks=int(app_data['median_2weeks']),
            price=app_data['price'],
            initialprice=app_data['initialprice'],
            discount=app_data['discount'],
            ccu=int(app_data['ccu']),
            languages=languages,
            genre=genre,
            tags=app_data.get('tags', None),
        )

    def get_app_details(self, appid: int) -> SteamApp:
        """Get details for a specific application."""
        params = {
            "request": "appdetails",
            "appid": str(appid)
        }
        return self._build_steam_app(self._make_request(params))

    def get_genre(self, genre: str) -> List[SteamApp]:
        """Get games in a particular genre."""
        params = {
            "request": "genre",
            "genre": genre
        }
        # Convert the raw data into a list of SteamApp dataclass instances
        return [self._build_steam_app(app_data) for app_data in self._make_request(params).values()]

    def get_tag(self, tag: str) -> List[SteamApp]:
        """Get games with a particular tag."""
        params = {
            "request": "tag",
            "tag": tag
        }
        # Convert the raw data into a list of SteamApp dataclass instances
        return [self._build_steam_app(app_data) for app_data in self._make_request(params).values()]

    def get_top100_in_2weeks(self) -> List[SteamApp]:
        """Get the Top 100 games by players in the last two weeks."""
        params = {
            "request": "top100in2weeks"
        }
        # Convert the raw data into a list of SteamApp dataclass instances
        return [self._build_steam_app(app_data) for app_data in self._make_request(params).values()]

    def get_top100_forever(self) -> List[SteamApp]:
        """Get the Top 100 games by players since March 2009."""
        params = {
            "request": "top100forever"
        }
        # Convert the raw data into a list of SteamApp dataclass instances
        return [self._build_steam_app(app_data) for app_data in self._make_request(params).values()]

    def get_top100_owned(self) -> List[SteamApp]:
        """Get the Top 100 games by owners."""
        params = {
            "request": "top100owned"
        }

        # Convert the raw data into a list of SteamApp dataclass instances
        return [self._build_steam_app(app_data) for app_data in self._make_request(params).values()]

    def get_all(self, page: int = 0) -> List[SteamApp]:
        """Get all games with owners data sorted by owners, and return them as a list of SteamApp dataclasses."""
        params = {
            "request": "all",
            "page": str(page)
        }

        # Convert the raw data into a list of SteamApp dataclass instances
        return [self._build_steam_app(app_data) for app_data in self._make_request(params).values()]
