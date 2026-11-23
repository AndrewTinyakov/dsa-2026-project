import os
import sys
from datetime import date
from getpass import getpass
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from dotenv import dotenv_values

from .csv_files import check_download

EVDS_URL = "https://evds3.tcmb.gov.tr/igmevdsms-dis"
FOOD_CPI_FILE = "turkish_food_cpi.csv"
USD_TRY_FILE = "usd_try_daily.csv"

FOOD_CPI_SERIES = {
    "TP.TUKFIY2025.01": "food_cpi",
    "TP.TUKFIY2025.0111": "cereals_cpi",
    "TP.TUKFIY2025.0112": "meat_cpi",
    "TP.TUKFIY2025.0114": "dairy_eggs_cpi",
    "TP.TUKFIY2025.0115": "oils_fats_cpi",
}
USD_TRY_SERIES = {"TP.DK.USD.A.YTL": "usd_try"}


def get_api_key(project_root: Path) -> str:
    key = os.getenv("EVDS_API_KEY", "").strip()
    if not key:
        key = (dotenv_values(project_root / ".env").get("EVDS_API_KEY") or "").strip()
    if not key and sys.stdin.isatty():
        key = getpass("EVDS API key: ").strip()
    if not key:
        raise ValueError("Set EVDS_API_KEY in .env or the environment to download EVDS data.")
    return key


def download_series(name: str, codes: list[str], key: str, end_date: date) -> pd.DataFrame:
    yearly_tables = []
    columns = ["Tarih", *(code.replace(".", "_") for code in codes), "UNIXTIME"]
    for year in range(2005, end_date.year + 1):
        year_end = min(date(year, 12, 31), end_date)
        url = (
            f"{EVDS_URL}/series={'-'.join(codes)}&startDate=01-01-{year}"
            f"&endDate={year_end:%d-%m-%Y}&type=csv"
        )
        response = requests.get(url, headers={"key": key}, timeout=90)
        response.raise_for_status()
        table = pd.read_csv(BytesIO(response.content))
        check_download(table, columns, f"{name} ({year})")
        yearly_tables.append(table)
    return pd.concat(yearly_tables, ignore_index=True)
