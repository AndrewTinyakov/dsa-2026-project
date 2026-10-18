# Food inflation proposal speaking script

Five slides. Target speaking time is about five minutes. Daanish introduces the question and models. Andrei presents the sources and code on slides 2 and 3. Rio explains testing and the plan on slides 4 and 5. The times are rehearsal targets.

## Slide 1 Daanish

The question and proposed models. About 1 minute 20 seconds.

Hello, we are Daanish, Andrei and Rio. Our project asks: can exchange rates and global food prices help us predict food inflation in Turkey?

Food prices matter for household budgets. We want to predict how much they change from one month to the next.

To measure this, we use the food part of the Consumer Price Index, or CPI. It includes food and non-alcoholic drinks bought by households.

We plan to use linear regression with lagged inputs. These are values from earlier months. The baseline uses past food inflation. The second model also uses earlier exchange-rate changes and global food-price changes.

We will compare their prediction errors on later months. If the extra data do not reduce those errors, our answer will be no.

Andrei wrote our download code. He will explain the sources and the checks we have completed.

## Slide 2 Andrei

The dataset. About 1 minute.

Thanks, Daanish. We use three sources: TurkStat's food CPI, the central bank's dollar-lira exchange rate, and the FAO Food Price Index. We download the Turkish data through the EVDS service.

FAO is the Food and Agriculture Organization of the United Nations. Its index tracks prices of food traded internationally. The exchange rate tells us how many lira one US dollar costs.

I wrote code to download these files and load them in pandas. I kept the source dates and gave the columns clear names. CPI and FAO are monthly. The exchange-rate file has one row per calendar day. The table shows the loaded file sizes.

## Slide 3 Andrei

What we checked in the data. About 1 minute.

We found 2,470 blank daily exchange rates. Of these, 2,270 are weekend dates. The other 200 are weekdays and still need a calendar check. TCMB does not set rates on weekends or public holidays.

We calculate each monthly average from the available daily rates. Then we add CPI and FAO data for the same month.

The result has 261 monthly rows, from January 2005 to September 2026, with no missing numeric values.

We still need monthly changes and publication-date checks before modeling. Rio will explain our test.

## Slide 4 Rio

How we will check our predictions. About 50 seconds.

Thanks, Andrei. The main risk is using data that were published after a prediction. To predict June before it starts, we must use only data published before June.

We will test both regression models on the same months, using expanding-window validation.

We train on earlier months and predict the next month. We compare the prediction with the actual value. Once that value is available, we can add it to the training data and repeat.

## Slide 5 Rio

The plan and roles. About 50 seconds.

For this proposal, Andrei worked on the data, Daanish on the script, and I on the presentation.

For the next stage, Andrei will finish the dataset and help build the regression models. Daanish will explore the data and create charts. I will run forecast evaluation and review errors.

By the checkpoint on 23 November, we plan to have a documented monthly dataset, first charts, and an initial baseline comparison. We will all review results and prepare the report and presentations.

## Notes for rehearsal and questions

### What exactly are we predicting?

The percentage change in food CPI from one month to the next. CPI itself is an index level. We will calculate monthly inflation from changes in that index. We are not predicting individual shop prices or annual inflation.

### Why choose exchange rates and global food prices?

We chose them as possible signals of import costs and international food-price changes. Our question is whether they add useful information beyond earlier food inflation. Even if they improve forecasts, that would not establish a causal effect.

### What have we completed so far?

The notebook downloads and loads the sources, renames columns, checks dates and missing values, averages available daily exchange rates by month, and joins the sources. Next we need monthly changes, lagged inputs and publication-date checks. We have not fitted models or tested the research question.

### How can daily rates be missing but the monthly table be complete?

Each month has published rates, so we can average those available values. We do not replace blank daily values with zero or invent rates. Of the 2,470 blanks, 2,270 fall on weekends and 200 on weekdays. The weekday blanks still need a holiday-calendar check.

### Are all 261 months ready for modeling?

They form a complete table of monthly index levels and exchange rates. Calculating changes and lags will remove some starting rows. Publication timing may require further adjustments. The final training and test samples will therefore contain fewer observations. The extra food categories are available for optional later work.

### What does the baseline model do?

Both proposed models use linear regression. The baseline learns from earlier food inflation. The second model also uses earlier USD/TRY changes and FAO index changes. A lag means a value from an earlier month. We will choose the number of lags using training data.

### Is the test an 80/20 train-test split?

That could set the starting point, but the proposed method is expanding-window validation, also called walk-forward testing. We train on earlier months and predict the next month. Once its actual value is available, we add it to training and repeat through the later period. We keep months in date order. The exact starting split is still undecided.

### How will we avoid using future information?

We will define when each forecast is made and check which releases were available then. A value for the previous month may still be unpublished. Simply shifting every column by one month may not be enough. Historical data revisions are another limitation we need to check.

### What would count as a useful improvement?

Lower RMSE for the model with extra indicators on the same later months. RMSE means root mean squared error and gives more weight to large errors. For monthly inflation, its unit is percentage points. We will keep the test period separate from model choices. If the extra indicators do not help, that is still a valid answer.

## Proposal requirements

Both the written brief and the separate proposal template allow at most five slides. This version follows the five-slide outline in the brief: question, dataset, first look, main risk, then plan and roles. The first look is the missing-rate count, with its meaning and limits.

The written brief also requires a separate one-page proposal PDF by 18 October at 23:59. The presentation is on 19 October. The 23 November presentation is the checkpoint. Final findings come later. Keep the course AI-use log.

## Source notes

Data sizes, coverage and null counts come from the executed Proposal data check section in [food_inflation.ipynb](../food_inflation.ipynb).

CPI source and metadata: https://veriportali.tuik.gov.tr/en/press/58289. FAO definition: https://www.fao.org/worldfoodsituation/foodpricesindex/en/. Proposal requirements: handout/DSA101_Project_Proposal_Brief_2026Fall.pdf.

TCMB publication calendar: https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB%2BEN/Main%2BMenu/Core%2BFunctions/Exchange%2BRate%2BPolicy/Foreign%2BExchange%2Band%2BBanknotes%2BMarkets/Indicative%2BExchange%2BRates .
