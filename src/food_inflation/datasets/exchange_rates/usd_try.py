from datetime import date
from pathlib import Path

import pandas as pd

from .. import evds_client
from ..csv_snapshots import read_indicators

USD_TRY_FILE = "usd_try_daily.csv"
USD_TRY_SERIES = {"TP.DK.USD.A.YTL": "usd_try"}


def download(key: str, end_date: date) -> pd.DataFrame:
    return evds_client.download_series(USD_TRY_FILE, USD_TRY_SERIES, key, end_date)


def load(raw_dir: Path) -> pd.DataFrame:
    columns = evds_client.csv_columns(USD_TRY_SERIES)
    return read_indicators(raw_dir / USD_TRY_FILE, "Tarih", "%d-%m-%Y", columns)


def monthly_average(daily_rates: pd.DataFrame) -> pd.DataFrame:
    return daily_rates.resample("MS").mean()
