from pathlib import Path
import json
import pandas as pd
import os

# non-vectorized operation used
import warnings
from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=PerformanceWarning)



with open(Path("data") / "CIK0000055785_submissions.json") as f:
    data = json.load(f)

filing_dt = pd.to_datetime(pd.Series(data["filings"]["recent"]["acceptanceDateTime"]))

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

def get_market_reception_day(utc_series):
    # 1. Setup the NYSE Business Calendar (excludes weekends & holidays)
    us_bus = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    
    # 2. Localize to UTC and Convert to New York (handles EST/EDT automatically)
    ny_time = pd.to_datetime(utc_series).dt.tz_convert('America/New_York')
    
    # 3. Logic: If filed after 4:00 PM, it belongs to the NEXT business day
    # Note: SEC acceptance times are precision timestamps. 
    is_after_hours = ny_time.dt.hour >= 16
    
    # 4. Create the final date. 
    # Use .normalize() to strip the time and keep just the date
    reception_date = ny_time.dt.normalize()
    
    # Shift only the after-hours filings to the next business day
    reception_date.loc[is_after_hours] += us_bus # performance warning for non-vectorized operations
    
    # 5. Final Check: Ensure even "on-time" filings aren't on weekends/holidays
    # This rolls a Saturday 10:00 AM filing forward to Monday
    is_weekend_or_holiday = ~reception_date.isin(pd.bdate_range(reception_date.min(), reception_date.max(), freq=us_bus))
    reception_date.loc[is_weekend_or_holiday] += us_bus
    
    return reception_date.dt.tz_localize(None) # Strip TZ for cleaner dataframes

filing_dt = get_market_reception_day(filing_dt)

dates = list(zip(filing_dt.to_numpy(), data["filings"]["recent"]["reportDate"]))
df = pd.DataFrame(dates)
df.columns = ["filing_date", "report_date"]

df["filing_date"] = pd.to_datetime(df["filing_date"])
df["report_date"] = pd.to_datetime(df["report_date"])

df = df.dropna() # can't convert with missing dates

download_dir = Path("preprocessed")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
df.to_csv(download_dir / "KMB_dates.csv", index=False)