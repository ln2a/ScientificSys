from pandas import DataFrame
import re

df = DataFrame(columns=("DI", "TI", "AF", "DE", "AB", "PY", "CR"))
count = -1
with open("./data/test1-1000.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
with open("./data/test1001-2000.txt", "r", encoding="utf-8") as file:
    lines += file.readlines()
with open("./data/test2001-3000.txt", "r", encoding="utf-8") as file:
    lines += file.readlines()
with open("./data/test3001-3079.txt", "r", encoding="utf-8") as file:
    lines += file.readlines()

for i in range(len(lines)):
    try:
        if lines[i][:2] == "PT":
            count += 1
        # 添加标题
        if lines[i][:2] == "TI":
            title = lines[i][3:].rstrip("\n")
            i += 1
            while lines[i][:2] == "  ":
                title += " "
                title += lines[i].rstrip("\n").strip()
                i += 1
            df.loc[count, "TI"] = title
        # 添加作者
        if lines[i][:2] == "C1":
            df.loc[count, "AF"] = []
            while lines[i][:2] == "C1" or lines[i][:2] == "  ":
                k = lines[i].index("[")
                j = lines[i].index("]")
                names = lines[i][k + 1 : j].split(";")
                match = re.search(r"](.*?),", lines[i])
                uni = match.group(1)
                namesLs = [{name.strip(): uni.strip()} for name in names]
                df.loc[count, "AF"] += namesLs
                i += 1
        # 添加关键词
        if lines[i][:2] == "DE":
            keyWords = lines[i][3:].rstrip("\n")
            i += 1
            while lines[i][:2] == "  ":
                keyWords += lines[i].rstrip("\n")
                i += 1
            wordsLs = keyWords.split(";")
            df.loc[count, "DE"] = [word.strip() for word in wordsLs]
        # 添加摘要
        if lines[i][:2] == "AB":
            df.loc[count, "AB"] = lines[i][3:].rstrip("\n")
            i += 1
        # 添加引文
        if lines[i][:2] == "CR":
            df.loc[count, "CR"] = []
            while lines[i][:2] == "CR" or lines[i][:2] == "  ":
                if lines[i][:2] == "CR":
                    citeInfo = lines[i][3:].rstrip("\n")
                else:
                    citeInfo = lines[i].rstrip("\n")
                citeLs = [word.strip() for word in citeInfo.split(",")]
                for word in citeLs:
                    if word[:3] == "DOI":
                        doi = word[4:]
                if (
                    len(citeLs) >= 3
                    and citeLs[2] == "IEEE T VIS COMPUT GR"
                    and int(citeLs[1]) >= 2016
                    and int(citeLs[1]) <= 2025
                ):
                    df.loc[count, "CR"].append(doi)
                i += 1
        # 发布时间
        if lines[i][:2] == "PY":
            df.loc[count, "PY"] = lines[i][3:].rstrip("\n")
            i += 1
        # DOI
        if lines[i][:2] == "DI":
            df.loc[count, "DI"] = lines[i][3:].rstrip("\n")
            i += 1
    except Exception:
        print(i)
        print(lines[i])
print(len(df))
df.to_excel("./output_data/nodes_10y_0.xlsx")
