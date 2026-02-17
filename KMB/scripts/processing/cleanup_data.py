from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

df = pd.read_csv(Path("cleaned") / "KMB.csv")
df["period_end"] = pd.to_datetime(df["period_end"])
df["filing_date"] = pd.to_datetime(df["filing_date"])

# see KMB/preprocessing/preprocessed/1_eda.ipynb for general guidance on these features being picked.
# not including periodic trends that don't span into present day (i.e. missing data)
possibly_periodic = [
	3, 5, 6, 9, 10, 11, 15, 16, 
	20, 21, 23, 24, 26, 27, 28,
	29, 30, 35, 41, 42, 43, 44, 45,
	46, 51, 52, 53, 54, 55, 56,
	57, 58, 59, 60, 61, 62, 
	63, 64, 65, 66, 67, 71,
	72, 73, 74, 75, 76, 77,
	79, 82, 85, 87, 89, 90,
	93, 95, 97, 98, 99, 101,
	102, 103, 110, 111, 127,
	128, 129, 130, 142, 143,
	146, 153, 157, 158, 159,
	160, 180, 181, 182, 183, 185, 
	186, 187, 188, 189, 194, 
	195, 196, 198, 203, 205,
	206, 217, 236, 238, 239, 
	242, 243, 244, 245, 246,
	247, 258, 262, 263, 264,
	268, 269, 273, 274, 276,
	277, 278, 279, 280, 281,
	282, 283, 284, 287, 288,
	289, 302, 304, 305, 307,
	308, 309, 310, 311, 314,
	318, 319, 320, 322, 323,
	324, 325, 326, 327, 328,
	329, 332, 334, 335, 336, 
	338, 339, 340, 341, 343,
	344, 345, 357, 358, 359,
	361, 362, 363, 364, 365,
	377, 378, 381, 383, 385,
	387, 388, 401, 402, 405, 
	407, 408, 416, 417, 418,
	419, 421, 429, 437, 441,
	442, 444, 445, 451, 455, 
	457, 459, 461, 462, 463, 
	464, 465, 466, 467, 468, 
	469, 472, 474, 475, 477, 
	478, 482, 487, 489, 492,
	494, 496, 497, 499, 500,
	501, 505, 507, 514, 516,
	517, 521, 523, 524, 526,
	528, 529, 530, 554, 558,
	559, 560, 562, 567, 574,
	575, 577, 578, 579, 580,
	581, 582, 583, 585, 586,
	589, 590, 591, 592, 593,
	595, 601, 602, 603, 604,
]

full_feats = [0,1,2] # keep period end, filing date and form type
full_feats.extend(possibly_periodic)

df = df.iloc[:,full_feats]

# this is an estimate since points are not necessarily sequential
# looking for 2 full periods + 1 full period for validation (1) and test sets (3)
df = df.loc[:,df.notna().sum() >= 12] # need at least two full periods for valid nyquist frequency. 

binarizer = MultiLabelBinarizer(sparse_output=False)
binarized = binarizer.fit_transform(df["form"].to_numpy().reshape(-1,1))
df = pd.concat([df, pd.DataFrame(binarized)], axis=1)

df.to_csv(Path("preprocessed") / "KMB_financials.csv", index=False)