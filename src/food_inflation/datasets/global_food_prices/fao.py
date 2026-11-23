from io import BytesIO
from pathlib import Path

import pandas as pd
import requests

from ..csv_snapshots import check_download, read_indicators

FAO_URL = (
    "https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/"
    "food_price_indices_data.csv?download=true&sfvrsn=523ebd2a_84"
)
FAO_FILE = "fao_food_prices.csv"

FAO_COLUMNS = {
    "Food Price Index": "food_price_index",
    "Meat": "meat",
    "Dairy": "dairy",
    "Cereals": "cereals",
    "Oils": "vegetable_oils",
    "Sugar": "sugar",
}


def download() -> pd.DataFrame:
    response = requests.get(FAO_URL, timeout=90)
    response.raise_for_status()
    food_prices = pd.read_csv(BytesIO(response.content), skiprows=2, usecols=range(7))
    food_prices = food_prices.dropna(how="all")
    check_download(food_prices, ["Date", *FAO_COLUMNS], FAO_FILE)
    return food_prices


def load(raw_dir: Path) -> pd.DataFrame:
    return read_indicators(raw_dir / FAO_FILE, "Date", "%Y-%m", FAO_COLUMNS)
