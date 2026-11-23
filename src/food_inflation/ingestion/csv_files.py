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
