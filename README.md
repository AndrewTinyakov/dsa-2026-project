# Food inflation in Turkey

Can exchange rates and global food prices help predict monthly food inflation in Turkey?

The [data preparation notebook](notebooks/01_data_understanding_and_preparation.ipynb)
checks coverage and missing values, then aligns Turkish food CPI, daily USD/TRY
rates and FAO food price indices to one row per month.

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
├── raw/          Source CSV snapshots used by the original notebook
└── interim/     Reusable monthly indicators generated from the source CSVs
notebooks/       Numbered notebooks for data checks and analysis
src/food_inflation/
├── ingestion/
│   ├── evds.py           Turkish food CPI and daily USD/TRY from EVDS
│   ├── fao.py            Global food price indices from FAO
│   ├── csv_files.py      CSV validation and saving
│   └── pipeline.py       Downloads missing source CSVs
└── data_preparation/
    ├── source_tables.py  Parses and validates the source tables
    ├── monthly_table.py  Aligns the indicators to the CPI calendar
    └── pipeline.py       Saves the monthly Parquet file
tests/
├── ingestion/           Download and offline reuse checks
└── data_preparation/    Monthly table checks
handout/         Course brief and template
reports/
├── proposal/    Written proposal, slides and speaking script
├── progress/    Mid-project progress report and presentation
└── final/       December report and final presentation
```

Git ignores the data files. `data/processed/` can hold a dataset built for
a specific analysis or forecast.

## Reports and presentations

The proposal folder has the [written proposal](reports/proposal/food-inflation-project-proposal.pdf),
[slides](reports/proposal/food-inflation-proposal.pptx), and
[speaking script](reports/proposal/proposal-script.md). Keep the report, slides,
and any figures for each presentation in its milestone folder.

## Checks

```sh
uv run pytest
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_understanding_and_preparation.ipynb
```
