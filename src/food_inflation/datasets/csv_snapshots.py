from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd


def check_download(table: pd.DataFrame, columns: list[str], name: str) -> None:
    missing = set(columns) - set(table.columns)
    if missing:
        raise ValueError(f"{name} is missing source columns: {', '.join(sorted(missing))}")
    if table.empty:
        raise ValueError(f"{name} contains no observations")


def save_csv(table: pd.DataFrame, path: Path) -> None:
    with TemporaryDirectory(dir=path.parent) as directory:
        temporary = Path(directory) / path.name
        table.to_csv(temporary, index=False)
        temporary.replace(path)


def read_indicators(
    path: Path, date_column: str, date_format: str, columns: dict[str, str]
) -> pd.DataFrame:
    values = pd.read_csv(path, usecols=[date_column, *columns])
    dates = pd.to_datetime(values.pop(date_column), format=date_format, errors="raise")
    if dates.empty or dates.isna().any() or not dates.is_unique or not dates.is_monotonic_increasing:
        raise ValueError(f"{path.name} must contain nonempty, unique dates in order")
    values = values.rename(columns=columns).loc[:, list(columns.values())]
    values.index = pd.DatetimeIndex(dates, name="date")
    return values.apply(pd.to_numeric, errors="raise")
