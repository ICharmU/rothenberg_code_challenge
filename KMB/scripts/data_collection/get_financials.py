# TODO - clean up into descriptive functions
from pathlib import Path
import os

KMB_CIK = "0000055785"
kmb_fp = Path("data") / f"CIK{KMB_CIK}.json"

import json

with open(kmb_fp) as f:
    raw_data = json.load(f)

from collections import defaultdict
outstanding_shares = raw_data["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"]
parsed = defaultdict(list)

for event in outstanding_shares:
    parsed["date"].append(event["end"])
    parsed["outstanding_shares"].append(event["val"])
    parsed["form"].append(event["form"])

diff_format = list()
simple_data = list()
for feat in raw_data["facts"]["us-gaap"].keys():
    try:
        feat_data = raw_data["facts"]["us-gaap"][feat]["units"]
        for unit in feat_data:
            parsed = defaultdict(list)

            for event in feat_data[unit]:
                parsed["period_end"].append(event["end"])
                parsed[feat].append(event["val"])
                parsed["form"].append(event["form"])
                parsed["filing_date"].append(event["filed"])

            simple_data.append(parsed)
    except Exception as e:
        # print(e)
        diff_format.append(feat)

if diff_format:
    print("Different format detected. Come check it out!")
    raise Exception

for feat in raw_data["facts"]["dei"].keys():
    try:
        feat_data = raw_data["facts"]["dei"][feat]["units"]
        for unit in feat_data:
            parsed = defaultdict(list)

            for event in feat_data[unit]:
                parsed["period_end"].append(event["end"])
                parsed[feat].append(event["val"])
                parsed["form"].append(event["form"])
                parsed["filing_date"].append(event["filed"])

            simple_data.append(parsed)
    except:
        diff_format.append(feat)

import pandas as pd
simple_data = [pd.DataFrame(d) for d in simple_data]

processed_dfs = []
for df in simple_data:
    # Identify the 'unique feature' column (the one that isn't a key)
    keys = {'period_end', 'filing_date', 'form'}
    unique_col = [c for c in df.columns if c not in keys][0]
    
    # Melt or rename so we can stack them consistently
    # It's often easier to just melt it into a 'value' and 'feature_name' column
    temp_df = df.melt(id_vars=['period_end', 'filing_date', 'form'], 
                      var_name='feat', 
                      value_name='value')
    processed_dfs.append(temp_df)

# 2. Concatenate vertically (Extremely fast)
long_df = pd.concat(processed_dfs, ignore_index=True)

# 3. Pivot to wide format (The "Join" equivalent)
final_df = long_df.pivot_table(
    index=['period_end', 'filing_date', 'form'],
    columns='feat',
    values='value'
).reset_index()

cleaned_fp = Path("cleaned")
if not os.path.exists(cleaned_fp):
    os.makedirs(cleaned_fp)
final_df.to_csv(cleaned_fp / "KMB.csv", index=False)