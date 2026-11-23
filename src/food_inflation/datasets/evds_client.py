import os
import sys
from datetime import date
from getpass import getpass
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from dotenv import dotenv_values

from .csv_snapshots import check_download

EVDS_URL = "https://evds3.tcmb.gov.tr/igmevdsms-dis"


def get_api_key(project_root: Path) -> str:
    key = os.getenv("EVDS_API_KEY", "").strip()
    if not key:
        key = (dotenv_values(project_root / ".env").get("EVDS_API_KEY") or "").strip()
    if not key and sys.stdin.isatty():
        key = getpass("EVDS API key: ").strip()
    if not key:
        raise ValueError("Set EVDS_API_KEY in .env or the environment to download EVDS data.")
    return key


def csv_columns(series: dict[str, str]) -> dict[str, str]:
    return {code.replace(".", "_"): name for code, name in series.items()}


def download_series(name: str, series: dict[str, str], key: str, end_date: date) -> pd.DataFrame:
    yearly_tables = []
    columns = ["Tarih", *csv_columns(series), "UNIXTIME"]
    for year in range(2005, end_date.year + 1):
        year_end = min(date(year, 12, 31), end_date)
        url = (
            f"{EVDS_URL}/series={'-'.join(series)}&startDate=01-01-{year}"
            f"&endDate={year_end:%d-%m-%Y}&type=csv"
        )
        response = requests.get(url, headers={"key": key}, timeout=90)
        response.raise_for_status()
        table = pd.read_csv(BytesIO(response.content))
        check_download(table, columns, f"{name} ({year})")
        yearly_tables.append(table)
    return pd.concat(yearly_tables, ignore_index=True)
