import pandas as pd
from pandas.testing import assert_frame_equal

from food_inflation.monthly_dataset.build import monthly_indicators


def test_monthly_indicators_use_cpi_calendar_and_published_daily_rates():
    cpi = pd.DataFrame(
        {"food_cpi": [200.0, 230.0]},
        index=pd.DatetimeIndex(["2025-01-01", "2025-03-01"], name="date"),
    )
    usd_try = pd.DataFrame(
        {"usd_try": [30.0, None, 34.0, 36.0]},
        index=pd.DatetimeIndex(["2025-01-03", "2025-01-04", "2025-01-06", "2025-02-03"], name="date"),
    )
    fao = pd.DataFrame(
        {"food_price_index": [110.0, 111.0]},
        index=pd.DatetimeIndex(["2024-12-01", "2025-02-01"], name="date"),
    )

    result = monthly_indicators(cpi, usd_try, fao)

    expected = pd.DataFrame(
        {
            "food_cpi": [200.0, None, 230.0],
            "usd_try": [32.0, 36.0, None],
            "fao_food_price_index": [None, 111.0, None],
        },
        index=pd.date_range("2025-01-01", periods=3, freq="MS", name="date"),
    )
    assert_frame_equal(result, expected)
