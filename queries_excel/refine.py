import os
import pandas as pd

filename = "excel_query_1_results.csv"


file_path = os.path.join("../Query_CSVs", filename)

df = pd.read_csv(file_path, delimiter=",", index_col=0, dtype=object)

for col in df.columns:
    for ind in df.index:
        # print(df.loc[ind][col], len(df.loc[ind][col]))
        if df.loc[ind][col] == "[]":
            df.loc[ind][col] = 0
        else:
            df.loc[ind][col] = df.loc[ind][col].count(r",") + 1
    # break

print(df)
