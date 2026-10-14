# Data check for the project proposal

Checked the three downloaded CSVs on 14 October 2026. The check read the saved files without changing them or running the notebook's download cell.

| Source file | Rows × columns | Period | One row represents |
| --- | --- | --- | --- |
| Turkish food CPI | 261 × 7 | January 2005 to September 2026 | One month with the overall food CPI and four food-group indices |
| USD/TRY | 7,943 × 3 | 1 January 2005 to 30 September 2026 | One calendar date with a rate when EVDS publishes an observation |
| FAO food indices | 441 × 7 | January 1990 to September 2026 | One month with the overall food index and five commodity-group indices |

Column counts include dates and source metadata. CPI contains five numeric index series, USD/TRY contains one rate series, and FAO contains six numeric index series. `UNIXTIME` is metadata in the two EVDS files.

All dates parse, follow chronological order, and have no duplicates or missing dates within each file's calendar span. All populated numeric values parse, are finite, and are positive. All CPI and FAO index observations are present.

USD/TRY contains 5,473 populated rates and 2,470 blank observations. Earlier checks identified 2,270 blanks on weekends and 200 on weekdays. Every month has published rates. Monthly averages use available rates only, without filling blanks. TCMB's FAQ describes a previous-business-day rate convention for EVDS, which matches the source spot checks. Keep the original EVDS dates.

## First look used in the slides

Monthly Turkish food inflation is calculated from adjacent monthly index levels:

`100 × (CPI this month / CPI previous month − 1)`

There are 260 calculated changes from February 2005 to September 2026. The median is 1.37%. The largest is 15.98% in December 2021. These figures come from the downloaded index levels, whose stored precision can affect calculated changes.

The three sources overlap for 261 complete months of levels. Computing monthly changes leaves 260 overlapping observations. This is a coverage check. Publication delays and lagged predictors still need to be handled before defining the final forecasting sample.

The first-look chart describes historical variation. It does not establish that exchange rates or global food prices improve forecasts, or that either causes Turkish inflation. The Turkish and FAO food baskets also differ, including the Turkish dairy/eggs group and FAO's dairy group.

## Sources and reuse

- [TÜİK CPI release and tables](https://veriportali.tuik.gov.tr/tr/press/58289), downloaded through [TCMB EVDS](https://evds3.tcmb.gov.tr/).
- [EVDS terms](https://evds3.tcmb.gov.tr/igmevdsms-dis/documents/showDocument?docId=18) permit use and publication with source attribution. Simplified English labels in this project are the team's labels.
- [FAO Food Price Index](https://www.fao.org/worldfoodsituation/foodpricesindex/en/). The [FAO statistical database terms](https://www.fao.org/contact-us/terms/db-terms-of-use/en/) specify CC BY 4.0 unless stated otherwise for a dataset, with additional provider terms.
- [TCMB FAQ on EVDS exchange-rate dates](https://www.tcmb.gov.tr/wps/wcm/connect/bab69efb-d66c-45b5-91c6-1533886acd6e/GenelAg-SSS.pdf?MOD=AJPERES). The indexed FAQ describes previous-business-day rates. Its direct PDF link was unavailable during the latest check; fresh CSV/JSON and official daily XML comparisons support the observed convention in the sampled dates.
