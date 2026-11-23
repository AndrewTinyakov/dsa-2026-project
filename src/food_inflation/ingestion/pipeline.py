from datetime import date, timedelta
from pathlib import Path

from . import evds, fao
from .csv_files import save_csv


def download_sources(project_root: Path) -> None:
    """Fetch missing source CSVs and reuse existing files."""
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    fao_path = raw_dir / fao.FAO_FILE
    if not fao_path.is_file():
        save_csv(fao.download_food_prices(), fao_path)

    evds_sources = {
        evds.FOOD_CPI_FILE: evds.FOOD_CPI_SERIES,
        evds.USD_TRY_FILE: evds.USD_TRY_SERIES,
    }
    missing_sources = [name for name in evds_sources if not (raw_dir / name).is_file()]
    if not missing_sources:
        return

    key = evds.get_api_key(project_root)
    end_date = date.today().replace(day=1) - timedelta(days=1)
    for name in missing_sources:
        table = evds.download_series(name, list(evds_sources[name]), key, end_date)
        save_csv(table, raw_dir / name)


def main() -> None:
    try:
        download_sources(Path.cwd())
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print("Source CSVs are available in data/raw/.")
