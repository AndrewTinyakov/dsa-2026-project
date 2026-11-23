from datetime import date
from pathlib import Path

import pandas as pd

from .. import evds_client
from ..csv_snapshots import read_indicators

FOOD_CPI_FILE = "turkish_food_cpi.csv"
FOOD_CPI_SERIES = {
    "TP.TUKFIY2025.01": "food_cpi",
    "TP.TUKFIY2025.0111": "cereals_cpi",
    "TP.TUKFIY2025.0112": "meat_cpi",
    "TP.TUKFIY2025.0114": "dairy_eggs_cpi",
    "TP.TUKFIY2025.0115": "oils_fats_cpi",
}


def download(key: str, end_date: date) -> pd.DataFrame:
    return evds_client.download_series(FOOD_CPI_FILE, FOOD_CPI_SERIES, key, end_date)


def load(raw_dir: Path) -> pd.DataFrame:
    columns = evds_client.csv_columns(FOOD_CPI_SERIES)
    return read_indicators(raw_dir / FOOD_CPI_FILE, "Tarih", "%Y-%m", columns)
