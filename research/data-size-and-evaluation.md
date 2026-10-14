# Dataset size and evaluation for monthly food inflation

Checked on 14 October 2026. Source files and public metadata were inspected separately. The working notebook has not been executed. Authenticated EVDS observations and the final merged forecasting sample remain unverified.

## Actual source files inspected

| Source | Actual observations | Coverage | Findings |
| --- | ---: | --- | --- |
| FAO monthly nominal CSV | 441 months for each of six indices | January 1990 to September 2026 | Overall food, meat, dairy, cereals, vegetable oils and sugar; no duplicate months or missing index values |
| FAO restricted to January 2005 onward | 261 months per index | January 2005 to September 2026 | The actual CSV supplies this count; it is not the final merged sample |
| TÜİK expenditure-class CPI workbook | 259 months per inspected category | January 2005 to July 2026 | Cereals, meat, dairy/eggs and oils/fats are complete in the inspected workbook |
| TCMB daily USD/TRY | Two single-day XML files checked | 2 January 2014 and 13 October 2026 | Both contain USD buying and selling rates; a complete FX series has not been downloaded |

The [FAO source page](https://www.fao.org/worldfoodsituation/foodpricesindex/en/) links the [CSV inspected](https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/food_price_indices_data.csv?download=true&sfvrsn=523ebd2a_84). The file is 48,110 bytes. It has two title rows above its actual header, a blank row, and 66 CSV fields per record, of which only the first seven are named and populated. The meaningful table is one date column plus six numeric series. The page and the CSV both identify September 2026 as the latest month.

The 891,288-byte TÜİK workbook was downloaded from the “Harcama gruplarına göre endeks sonuçları” link on the [official CPI release page](https://veriportali.tuik.gov.tr/tr/press/58289). The workbook has sheets `Düzey 2`, `Düzey 3`, `Düzey 4` and `Düzey 5`. On `Düzey 4`, year and month identify the monthly rows; columns E, F, H and I hold codes 0111, 0112, 0114 and 0115. Its index base is 2025=100 and classification is COICOP 2018. The count and last month above describe this actual file, not a promise that another endpoint has the same latest observation. Direct Python requests to this TÜİK download returned HTTP 403, while the browser download succeeded.

The inspection copies and metadata are under `/tmp/dsa-food-size-fao/` and `/tmp/dsa-food-size-tuik/`. Raw inspection files were not committed or inserted into notebook outputs.

## Current EVDS access verified

The current [official EVDS web-service guide](https://evds3.tcmb.gov.tr/igmevdsms-dis/documents/showDocument?docId=16) downloaded successfully as PDF. It confirms the base `https://evds3.tcmb.gov.tr/igmevdsms-dis/`, path-style `series=...&startDate=...&endDate=...&type=json` requests, and the `key` HTTP header. The guide documents a maximum of 1,000 observations per request. The notebook therefore requests one calendar year at a time rather than assuming one request can return decades of daily rates.

Public catalogue endpoints returned actual JSON containing these codes:

| Series | Verified current code |
| --- | --- |
| Food and non-alcoholic beverages | `TP.TUKFIY2025.01` |
| Cereals and cereal products | `TP.TUKFIY2025.0111` |
| Meat group | `TP.TUKFIY2025.0112` |
| Milk, other milk products and eggs | `TP.TUKFIY2025.0114` |
| Liquid and solid fats | `TP.TUKFIY2025.0115` |
| USD foreign-exchange buying rate | `TP.DK.USD.A.YTL` |

The actual metadata URLs are [CPI catalogue JSON](https://evds3.tcmb.gov.tr/igmevdsms-dis/serieList/fe/type=json&code=bie_tukfiy2025) and [FX catalogue JSON](https://evds3.tcmb.gov.tr/igmevdsms-dis/serieList/fe/type=json&code=bie_dkdovytl). They returned 349 and 110 catalogue records respectively. They verify identities and frequencies, not the complete observation history. The standard authenticated metadata route returned 403 when no `key` header was supplied. No personal key was used.

The CPI and FX acquisition cells use the documented EVDS observation API with a user-supplied key. They have not been tested with authenticated responses. The notebook validates expected response fields, dates and numeric values rather than accepting malformed downloads silently.

## What these counts imply

The inspected CPI and FAO files overlap for 259 calendar months before FX coverage is checked. That is an upper bound from these two files, not a measured three-source forecasting sample. Calculating a first monthly percentage change removes the first month when no preceding index value is available. Lagged inputs and publication delays further affect usable rows.

An 80/20 split of 259 rows is 207 older rows and 52 later rows. For comparison, restricting the inspected CPI file to January 2015 onward gives 139 level observations. The counts are per category; adding more categories does not create more independent months.

These sizes make a small regression with a few predictors worth investigating. They do not guarantee reliable forecasts or justify many lagged features or a large neural network. We will decide the exact sample and split after the notebook is run and source coverage is aligned.

## Evaluation recommendation

The forecasting textbook describes about 20% held out as typical, while explicitly making the test length depend on the available sample and forecast horizon. [Forecasting Principles and Practice, training and test sets](https://otexts.com/fpp2/accuracy.html).

Use chronological dates and one-month-ahead evaluation. Choose model settings on earlier observations using a few expanding-window validation periods, then evaluate the chosen setup on one untouched final block. A final block of 24–36 months is an alternative worth considering alongside 20%; choose it deliberately once the usable dataset is known. Do not tune on that final block or treat all test months as separate random rows. [Forecasting Principles and Practice, time-series cross-validation](https://otexts.com/fpp3/tscv.html).

Forecast inputs must reflect what was published before each target month. Today's revised historical files do not by themselves reproduce historical data vintages, so a first-semester backtest will need an explicit revision-data limitation even after publication delays are handled.
