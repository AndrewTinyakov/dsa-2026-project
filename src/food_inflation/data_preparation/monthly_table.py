import pandas as pd


def monthly_indicators(
    cpi: pd.DataFrame, usd_try: pd.DataFrame, fao: pd.DataFrame
) -> pd.DataFrame:
    """Align source indicators to the monthly CPI calendar."""
    usd_try_monthly = usd_try.resample("MS").mean()
    monthly = cpi.asfreq("MS").join(usd_try_monthly, how="left", validate="1:1")
    return monthly.join(fao.add_prefix("fao_"), how="left", validate="1:1")
