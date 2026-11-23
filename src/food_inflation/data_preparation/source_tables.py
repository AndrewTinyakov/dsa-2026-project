from pathlib import Path

import pandas as pd

from ..ingestion import evds, fao


def load_sources(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load typed CPI, daily USD/TRY and FAO tables, in that order."""
    cpi_columns = {code.replace(".", "_"): name for code, name in evds.FOOD_CPI_SERIES.items()}
    fx_columns = {code.replace(".", "_"): name for code, name in evds.USD_TRY_SERIES.items()}
    cpi = _read_indicators(raw_dir / evds.FOOD_CPI_FILE, "Tarih", "%Y-%m", cpi_columns)
    usd_try = _read_indicators(raw_dir / evds.USD_TRY_FILE, "Tarih", "%d-%m-%Y", fx_columns)
    food_prices = _read_indicators(raw_dir / fao.FAO_FILE, "Date", "%Y-%m", fao.FAO_COLUMNS)
    return cpi, usd_try, food_prices


def _read_indicators(
    path: Path, date_column: str, date_format: str, columns: dict[str, str]
) -> pd.DataFrame:
    values = pd.read_csv(path, usecols=[date_column, *columns])
    dates = pd.to_datetime(values.pop(date_column), format=date_format, errors="raise")
    if dates.empty or dates.isna().any() or not dates.is_unique or not dates.is_monotonic_increasing:
        raise ValueError(f"{path.name} must contain nonempty, unique dates in order")
    values = values.rename(columns=columns).loc[:, list(columns.values())]
    values.index = pd.DatetimeIndex(dates, name="date")
    return values.apply(pd.to_numeric, errors="raise")
