from datetime import date, timedelta
from pathlib import Path

from .datasets import evds_client
from .datasets.csv_snapshots import save_csv
from .datasets.exchange_rates import usd_try
from .datasets.food_cpi import source as food_cpi
from .datasets.global_food_prices import fao
from .monthly_dataset.build import load_sources, monthly_indicators, save_monthly_indicators


def download_sources(project_root: Path) -> None:
    """Fetch missing source CSVs and reuse existing files."""
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    fao_path = raw_dir / fao.FAO_FILE
    if not fao_path.is_file():
        save_csv(fao.download(), fao_path)

    evds_downloads = {
        raw_dir / food_cpi.FOOD_CPI_FILE: food_cpi.download,
        raw_dir / usd_try.USD_TRY_FILE: usd_try.download,
    }
    missing = [(path, fetch) for path, fetch in evds_downloads.items() if not path.is_file()]
    if not missing:
        return

    key = evds_client.get_api_key(project_root)
    end_date = date.today().replace(day=1) - timedelta(days=1)
    for path, fetch in missing:
        save_csv(fetch(key, end_date), path)


def download() -> None:
    try:
        download_sources(Path.cwd())
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print("Source CSVs are available in data/raw/.")


def prepare() -> None:
    project_root = Path.cwd()
    data_dir = project_root / "data"
    try:
        sources = load_sources(data_dir / "raw")
    except FileNotFoundError as error:
        raise SystemExit("Run food-inflation-download to get the source CSVs.") from error

    monthly = monthly_indicators(*sources)
    output_path = save_monthly_indicators(monthly, data_dir / "interim")
    print(f"Saved {len(monthly)} months to {output_path.relative_to(project_root)}.")
