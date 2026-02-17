import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

ticker = "KMB"
end_date = datetime.now()
start_date = end_date - timedelta(days = 25*365)

df = yf.download(ticker, start=start_date, end=end_date)
df.columns = [c[0] for c in df.columns]
df = df.reset_index()

# date formated dates
df.to_csv(Path("preprocessed") / "KMB_prices_dates.csv", index=False)

# float approximated dates
df["Date"] = df["Date"].dt.year + df["Date"].apply(lambda x: x.timetuple().tm_yday) / 366 # leap year
df.to_csv(Path("preprocessed") / "KMB_prices_floats.csv", index=False)