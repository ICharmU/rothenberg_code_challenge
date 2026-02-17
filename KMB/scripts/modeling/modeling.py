# TODO - clean up into descriptive functions
from pathlib import Path
import pandas as pd

prices = pd.read_csv(Path("preprocessed") / "KMB_prices_dates.csv")
financials = pd.read_csv(Path("preprocessed") / "KMB_financials.csv")

prices["target"] = prices["Close"] - prices["Open"]
prices = prices[["Date", "target"]] # backward looking
priced = prices.sort_values(by="Date")

dates = pd.read_csv(Path("preprocessed") / "KMB_dates.csv")

merged = prices.merge(financials, left_on="Date", right_on="period_end").sort_values(by="period_end")
merged = merged.merge(dates, left_on="Date", right_on="report_date", suffixes=("", "_drop"))
merged = merged.drop(columns=["Date", "filing_date_drop", "report_date"])
financial_cols = list(set(merged.columns) - {'0', '1', '2', '3', 'filing_date', 'form'})
binarized_form_cols = ['0', '1', '2', '3']
grouped = merged.groupby('period_end')

agg_logic = {col: 'first' for col in financial_cols}
form_logic = {col: 'max' for col in binarized_form_cols}

df_consolidated = grouped.agg({**agg_logic, **form_logic})

full_calendar = pd.date_range(start=df_consolidated["period_end"].index.min(), end=df_consolidated["period_end"].index.max(), freq='B')
daily = df_consolidated.reindex(full_calendar)
daily = daily.ffill()
daily = daily.drop(columns=["target"]) # construct targets for each day later in the program

y = pd.read_csv(Path("preprocessed") / "KMB_prices_dates.csv").set_index("Date")
y = y.set_index(pd.to_datetime(y.index))
y_stock_returns = (y["Close"] - y["Open"])
y_stock_returns = y_stock_returns.loc[daily.index.min():daily.index.max()]

y_stock_returns = y_stock_returns.asfreq("B")
daily = daily.loc[y_stock_returns.index]

holidays = y_stock_returns.isna()

daily = daily.loc[~holidays].astype(float)
y_stock_returns = y_stock_returns.loc[~holidays].astype(float)

X_train, X_test = daily.iloc[:-180], daily.iloc[-180:]
y_train, y_test = y_stock_returns.iloc[:-180], y_stock_returns.iloc[-180:] # keep test set untrained for future modeling


# INCLUDE HERE: reliable model

# model.train()
# model.predict()
# predictions.to_csv()