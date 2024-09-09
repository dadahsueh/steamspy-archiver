from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class SteamApp:
    appid: int
    name: str
    developer: str
    publisher: str
    score_rank: str
    owners: Tuple[int, int]  # (min_owners, max_owners)
    positive: int
    negative: int
    userscore: int
    average_forever: int
    average_2weeks: int
    median_forever: int
    median_2weeks: int
    price: str
    initialprice: str
    discount: str
    ccu: int
    languages: Optional[List[str]] = None
    genre: Optional[List[str]] = None
    tags: Optional[Dict[str, int]] = None
