# Food inflation in Turkey

Can exchange rates and global food prices help predict monthly food inflation in Turkey?

The [data preparation notebook](notebooks/01_data_understanding_and_preparation.ipynb)
checks coverage and missing values, then aligns Turkish food CPI, daily USD/TRY
rates and FAO food price indices to one row per month.
The [exploration and regression notebook](notebooks/02_exploration_and_explanatory_regression.ipynb)
describes monthly changes through December 2023. It fits explanatory regressions
on historical months and reserves January 2024 onward for final forecast evaluation.
The [forecast evaluation notebook](notebooks/03_forecast_evaluation.ipynb)
runs a walk-forward backtest for 2021–2023. It compares three checkpoint
methods using revised snapshots and a fixed two-month availability rule.

## Run the project

From the repository root, with [uv](https://docs.astral.sh/uv/) installed:

```sh
uv sync --locked
uv run food-inflation-download
uv run food-inflation-prepare
uv run jupyter lab
```

In PyCharm, use the project's `.venv` as the Python interpreter and mark
`src/` as a Sources Root under **Settings → Project → Project Structure**.
Select the same interpreter for the notebook kernel.

The download command reuses the three CSVs in `data/raw/`. If either EVDS
file is missing, it needs an [EVDS API key](https://evds3.tcmb.gov.tr/).
Set `EVDS_API_KEY` in the environment, copy `.env.example` to `.env` and
fill it in, or enter the key when prompted in a terminal. The FAO download
is public. To refresh a source, move its CSV out of `data/raw/` and rerun
the download command.

The preparation command reads the local CSVs and saves
`data/interim/monthly_indicators.parquet`. The `date` index uses the first
day of each month. The table keeps the CPI calendar and averages the
published USD/TRY rates within each month. Missing daily rates are left
blank during aggregation. CPI and FAO columns contain index levels.

## Project layout

```text
data/
├── raw/         Source CSV snapshots
├── interim/     Reusable monthly indicators generated from the source CSVs
└── processed/   Datasets prepared for a specific analysis or forecast
notebooks/       Numbered notebooks for data checks and analysis
src/food_inflation/
├── datasets/
│   ├── food_cpi/            Turkish food CPI series
│   ├── exchange_rates/      Daily USD/TRY rates and monthly averages
│   ├── global_food_prices/  FAO food price indices
│   ├── evds_client.py       Shared authentication and yearly requests
│   └── csv_snapshots.py     Shared CSV parsing, validation and saving
├── monthly_dataset/        Aligns all three inputs and writes Parquet
├── forecasting/            Reserved for forecasting code
└── cli.py                   Download and preparation commands
tests/
├── monthly_dataset/     Monthly table checks
└── test_cli.py           Download and offline reuse checks
handout/         Course brief and template
reports/
├── proposal/    Written proposal, slides and speaking script
├── progress/    Mid-project progress report and presentation
└── final/       December report and final presentation
```

Git ignores the data files and tracks directories once they contain tracked
files. Create the forecasting and report milestone folders locally as needed.

## Reports and presentations

The proposal folder has the [written proposal](reports/proposal/food-inflation-project-proposal.pdf),
[slides](reports/proposal/food-inflation-proposal.pptx), and
[speaking script](reports/proposal/proposal-script.md). Keep the report, slides,
and any figures for each presentation in its milestone folder.

The [checkpoint presentation materials](reports/progress/checkpoint-presentation-materials.md)
collect the findings, slide figures, and proposed next experiments.

## Checks

```sh
uv run pytest
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_understanding_and_preparation.ipynb
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/02_exploration_and_explanatory_regression.ipynb
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/03_forecast_evaluation.ipynb
```
