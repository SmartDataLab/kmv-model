#%%
import pandas as pd
import os

raw_files = [x for x in os.listdir("data") if "kmv_raw" in x]

#%%
print(raw_files)
cpi_df = pd.read_excel("data/CPI.xlsx", index_col="var")
for i, file_ in enumerate(raw_files):
    df = pd.read_csv("data/%s" % file_, index_col="date")
    for year in cpi_df.columns:
        cpi_df.loc["EDF%s" % (i + 1), year] = df.loc[
            [x for x in df.index if x[:4] == str(year)], "roe_dt"
        ].mean()
cpi_df.to_csv("data/cpi_roe.csv")
# %%
cpi_df = pd.read_excel("data/CPI.xlsx", index_col="var")
for i, file_ in enumerate(raw_files):
    df = pd.read_csv("data/%s" % file_, index_col="date")
    for year in cpi_df.columns:
        cpi_df.loc["EDF%s" % (i + 1), year] = df.loc[
            [x for x in df.index if x[:4] == str(year)], "EDF"
        ].mean()
cpi_df.to_csv("data/cpi_extra.csv")
