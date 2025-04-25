import pandas as pd

df = pd.read_excel("output_data/nodes_10y_0.xlsx")
# df1 = pd(columns=("DI", "TI", "AF", "DE", "AB", "PY", "CR"))
# count = 0
# for i in range(len(df)):
#     ls = eval(df.loc[i, "DE"])
#     count += 1
# print(count)

for i in range(len(df)):
    # 用字典存一行
    dc = {}
    dc = df.loc[i]
    if pd.isnull(dc["AF"]):
        df.drop(index=i, inplace=True)
    else:
        # 去除TI中的i标签
        s = dc["TI"].replace("<i>", "").replace("</i>", "")
        df.loc[i, "TI"] = s
        # 给CR和DE加上[]
        if pd.isnull(dc["CR"]):
            df.loc[i, "CR"] = "[]"
        if pd.isnull(dc["DE"]):
            df.loc[i, "DE"] = "[]"
# 重置索引
df = df.reset_index(drop=True)
# print(df.loc[20])
# print(df.loc[528])
# print(df.loc[993])
df.to_excel("./output_data/nodes_10y_clean.xlsx")
