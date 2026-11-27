# Checkpoint presentation materials

## Opening

Our project asks whether exchange rates and global food prices improve monthly forecasts of Turkish food inflation. At the checkpoint, we found that USD/TRY and FAO changes improve the fit to historical data. In the forecast backtest, adding them slightly reduced RMSE and increased MAE. Both regressions tended to predict too low. [Historical analysis](../../notebooks/02_exploration_and_explanatory_regression.ipynb) · [Forecast evaluation](../../notebooks/03_forecast_evaluation.ipynb)

## Suggested presentation order

1. **Data preparation.** Define the target and explain how daily exchange rates became monthly averages.
2. **Exploration.** Show the rise in inflation after 2020 and the pattern by calendar month.
3. **Historical models.** Show the regression comparison with calendar-month controls.
4. **Forecast test.** Show actual versus predicted inflation, then explain what RMSE and MAE say about the two regressions.
5. **Next experiment.** Use the averages by year to motivate testing shorter training windows. Explain when we would add a new source.

## Data and cleaning

- The target is the month-over-month percentage change in Turkey’s food and non-alcoholic beverages CPI. The sources are TÜİK food CPI through TCMB EVDS, daily TCMB USD/TRY rates, and FAO global food-price indices.
- The joined snapshot contains **261 months and 12 numeric series**, from January 2005 through September 2026, with no missing monthly values. The historical analysis ends in December 2023.
- The daily USD/TRY series has **2,470 missing rates**. Of these, 2,270 fall on weekends and 200 on weekdays. Seven recurring calendar dates account for 91 of the weekday gaps. Individual closures remain unverified. Each monthly average through December 2023 uses at least 17 published rates.
- Early food CPI levels are small on the current index base. Rounding makes the earliest monthly changes coarse, with nine recorded zero changes in 2005–2014.

[Data preparation](../../notebooks/01_data_understanding_and_preparation.ipynb) · [Data quality checks](../../notebooks/02_exploration_and_explanatory_regression.ipynb)

## What we found in the historical data

| Finding | Evidence |
|---|---|
| Food inflation shifted after 2020 | Average monthly food inflation rose from **0.91%** in 2005–2020 to **4.26%** in 2021–2023. USD/TRY’s average monthly increase rose from **0.99%** to **3.92%**. FAO’s mean monthly change stayed near **0.30%**. |
| Calendar month matters | In 2005–2020, the median change was **+3.45% in January** and **+2.85% in October**. June had the lowest median, **−1.68%**. |
| USD/TRY had the strongest lagged association | The correlation with food inflation one month later was **0.39** overall, **0.19** in 2005–2020, and **0.58** in 2021–2023. The FAO lag-one correlation was **0.11**. Large changes have a strong influence on these comparisons. |
| The category results varied | With FAO lagged one month, the matched oils and fats series had a correlation of **0.25** and cereals **0.12**. Meat and dairy were near zero. |
| Large changes were a weak signal on their own | In 2021–2023, food inflation exceeded its pre-2021 upper-quartile threshold in **24 of 36 months**. It did so in **10 of 14** months after a large depreciation and **14 of 22** other months. It also did so in **5 of 10** months after a large FAO rise and **19 of 26** other months. The small group sizes limit these comparisons. |

On the same **226 months**, the food-only regression had adjusted R² of **0.179**. Adding USD/TRY raised it to **0.250**, adding FAO alone to **0.189**, and adding both to **0.285**. With calendar-month controls, adding both indicators raised adjusted R² from **0.297 to 0.416**. The 2005–2020 refit had lower adjusted R², **0.044** for food only and **0.075** with both indicators. These are associations measured on the historical sample. [Exploration and regression notebook](../../notebooks/02_exploration_and_explanatory_regression.ipynb)

## What happened when we forecast

The development backtest made one forecast before each month from **January 2021 through December 2023**. Both regressions used the same expanding training history. The models and carry-forward benchmark used the conservative **two-month availability rule**. The data come from revised snapshots, so original published values may differ. [Forecast design and release timing](../../notebooks/03_forecast_evaluation.ipynb)

| Method | RMSE | MAE | Mean error |
|---|---:|---:|---:|
| Carry forward the latest available food inflation | 4.65 | 3.54 | −0.03 |
| Regression using past food inflation | 4.56 | **2.98** | −2.72 |
| Regression adding USD/TRY and FAO | **4.49** | 3.06 | −2.69 |

Errors are in percentage points. MAE is the average size of a miss. RMSE gives large misses more weight. Mean error is forecast minus actual, so a negative value means the model forecast too low on average. Adding both indicators improved RMSE by about **0.07 points** and increased MAE by about **0.08 points**. [Forecast scores](../../notebooks/03_forecast_evaluation.ipynb)

### Why the errors were large

- **A different inflation level.** Each regression forecast too low in **28 of the 36 months**. At the last forecast, **189 of 223 training months** were from 2005–2020. The lower inflation in those years may explain part of the bias. A shorter training window will test that.
- **A few large shocks.** In December 2021, actual food inflation was **15.98%**. The food-only and expanded regressions predicted **0.94%** and **1.24%**. That month accounts for about **30% of the total squared error** of each regression.
- **The age of the inputs.** Each forecast used changes from two months earlier. A model can still miss sudden increases if the available inputs give little warning. A one-month USD/TRY lag may be feasible once the month-end data availability is verified.

[Forecast table and interpretation](../../notebooks/03_forecast_evaluation.ipynb) · [Average forecasts by year](figures/average-forecast-by-year.png)

## Next experiment

1. **Vary the training history.** Compare all available history with rolling windows of the most recent five and ten years. Use the same 36 development months, timing rule, and forecast methods. Compare RMSE, MAE, and mean error. Shorter windows emphasize recent conditions and give the models fewer observations.
2. **If errors remain large, test new signals one at a time.** Start with Turkish agricultural producer prices (**Tarım-ÜFE**), then consider agricultural input costs (**Tarım-GFE**). Check historical coverage and publication timing first. Compare each addition against the same baseline on the same months. Calendar-month controls are also available from the current data. Brent in lira and Ramadan or holiday features are further options if the first tests justify them.
3. **Reserve the final evaluation.** Settle the training window and inputs using development results. Then evaluate January 2024 through September 2026 and report whether the forecast improvement holds up.

## Figures for slides

| Figure | Use it to show |
|---|---|
| [Monthly indicator changes](figures/monthly-indicator-changes.png) | The inflation shift after 2020 and when food CPI, USD/TRY, and FAO moved together or apart. |
| [Food inflation by calendar month](figures/food-inflation-seasonality.png) | The months that typically rise or fall. |
| [Lagged indicator relationships](figures/lagged-indicator-relationships.png) | The USD/TRY and FAO relationships at different lags. |
| [Historical fit with seasonality](figures/historical-fit-with-seasonality.png) | How the historical model fit changes after adding the two indicators, with and without month controls. |
| [Actual and forecast food inflation](figures/actual-and-forecast-food-inflation.png) | The timing and size of the biggest misses. |
| [Average forecasts by year](figures/average-forecast-by-year.png) | Why we want to test whether training on more recent data reduces underprediction. |
