from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from ..datasets.exchange_rates import usd_try
from ..datasets.food_cpi import source as food_cpi
from ..datasets.global_food_prices import fao


def load_sources(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load typed CPI, daily USD/TRY and FAO tables, in that order."""
    return food_cpi.load(raw_dir), usd_try.load(raw_dir), fao.load(raw_dir)


def monthly_indicators(
    cpi: pd.DataFrame, daily_rates: pd.DataFrame, global_prices: pd.DataFrame
) -> pd.DataFrame:
    """Align source indicators to the monthly CPI calendar."""
    usd_try_monthly = usd_try.monthly_average(daily_rates)
    monthly = cpi.asfreq("MS").join(usd_try_monthly, how="left", validate="1:1")
    return monthly.join(global_prices.add_prefix("fao_"), how="left", validate="1:1")


def save_monthly_indicators(monthly: pd.DataFrame, interim_dir: Path) -> Path:
    output_path = interim_dir / "monthly_indicators.parquet"
    interim_dir.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=interim_dir) as directory:
        temporary = Path(directory) / output_path.name
        monthly.to_parquet(temporary)
        temporary.replace(output_path)
    return output_path
