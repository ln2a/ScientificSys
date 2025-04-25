import pandas as pd
import json

df = pd.read_excel("output_data/nodes_10y_clean.xlsx")

n = int(len(df) / 4)
# n = 500

papersLs = {}
nodesLs = []
linksLs = []
# 获取最有影响力的作者和机构
auRank = {}
instRank = {}
for i in range(n):
    # 用字典存一行
    dc = {}
    dc = df.loc[i]
    ls = eval(dc["AF"])
    for j in ls:
        for k, v in j.items():
            auRank[k] = auRank.setdefault(k, 0) + 1
            instRank[v] = instRank.setdefault(v, 0) + 1

# 取出现次数大于5
auRankls = [(k, v) for k, v in auRank.items()]
auRankls.sort(key=lambda x: x[1], reverse=True)
auLs = [i[0] for i in auRankls[:100]]
for i in auLs:
    nodesLs.append({"id": i, "group": 2})

instRankls = [(k, v) for k, v in instRank.items()]
instRankls.sort(key=lambda x: x[1], reverse=True)
instLs = [i[0] for i in instRankls[:100]]
for i in instLs:
    nodesLs.append({"id": i, "group": 3})

print(len(instLs))
print(len(auLs))

for i in range(n):
    # 用字典存一行
    dc = {}
    dc = df.loc[i]
    # 添加文章名
    papersLs[dc.loc["DI"]] = dc.loc["TI"]
    nodesLs.append({"id": dc["TI"], "group": 1})
    # 添加作者和机构
    try:
        ls = eval(dc["AF"])
        aus = []
        insts = []
        for j in ls:
            for k, v in j.items():
                aus.append(k)
                insts.append(v)
        # 去重复
        aus = list(set(aus))
        insts = list(set(insts))
        for k in aus:
            if k in auLs:
                # nodesLs.append({"id": k, "group": 2})
                linksLs.append({"source": dc["TI"], "target": k, "value": 1})
        for v in insts:
            if v in instLs:
                # nodesLs.append({"id": v, "group": 3})
                linksLs.append({"source": dc["TI"], "target": v, "value": 1})
    except Exception:
        print(i)
        print(df.loc[i]["TI"])

print(len(nodesLs))
print(len(linksLs))

# 添加论文合作节点
count = 0
papers = [name for name in papersLs.keys()]
for i in range(n):
    # 用列表存引文列表
    try:
        ls = eval(df.loc[i, "CR"])
        for j in range(len(ls)):
            if ls[j] in papers:
                count += 1
                dc = {"source": df.loc[i, "TI"], "target": papersLs[ls[j]], "value": 1}
                linksLs.append(dc)
    except Exception:
        print(i)
        print(df.loc[i, "TI"])

print(count)

jsonData = {"nodes": nodesLs, "links": linksLs}
print(len(nodesLs))
print(len(linksLs))


# 导出为 JSON 文件
# with open("./output_data/sourceJsonTest.json", "w", encoding="utf-8") as f:
#     json.dump(jsonData, f, indent=4, ensure_ascii=False)
with open("./output_data/sourceJson.json", "w", encoding="utf-8") as f:
    json.dump(jsonData, f, indent=4, ensure_ascii=False)
