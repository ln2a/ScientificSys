import pandas as pd
import json

df = pd.read_excel("output_data/nodes_10y_clean.xlsx")

n = len(df)
# n = 500

papersLs = {}
nodesLs = []
nodesLs_all = []
linksLs = []
linksLs_all = []
# 获取最有影响力的作者和机构
auRank = {}
instRank = {}
auInst = {}
for i in range(n):
    # 用字典存一行
    dc = {}
    dc = df.loc[i]
    ls = eval(dc["AF"])
    for j in ls:
        for k, v in j.items():
            # auRank[(k, v)] = auRank.setdefault((k, v), 0) + 1
            auRank[k] = auRank.setdefault(k, 0) + 1
            instRank[v] = instRank.setdefault(v, 0) + 1
            auInst[k] = v

# 取发文数量前100的作者和机构
auRankls = [(k, v) for k, v in auRank.items()]
auRankls.sort(key=lambda x: x[1], reverse=True)
auLsMax = [i[0] for i in auRankls[:100]]  # 前100作者
for index, author in enumerate(auRankls):
    if index < 100:
        nodesLs.append(
            {
                "id": author[0],
                "group": 2,
                "paperCount": author[1],
                "inst": auInst[author[0]],
            }
        )
    nodesLs_all.append(
        {
            "id": author[0],
            "group": 2,
            "paperCount": author[1],
            "inst": auInst[author[0]],
        }
    )

instRankls = [(k, v) for k, v in instRank.items()]
instRankls.sort(key=lambda x: x[1], reverse=True)
instLsMax = [i[0] for i in instRankls[:100]]  # 前100机构
for index, inst in enumerate(instRankls):
    if index < 100:
        nodesLs.append({"id": inst[0], "group": 3, "paperCount": inst[1]})
    nodesLs_all.append({"id": inst[0], "group": 3, "paperCount": inst[1]})

# print(len(instLs))
# print(len(auLs))

# 添加paper节点
for i in range(n):
    # 存一行
    dc = df.loc[i]
    # doi和标题的对应关系
    papersLs[dc["DI"]] = dc["TI"]
    # 添加paper节点
    paperInfo = {
        "id": dc["TI"],
        "group": 1,
        "doi": dc["DI"],
        "ab": dc["AB"],
        "keywords": ",".join(eval(dc["DE"])),
        "year": str(dc["PY"]),
    }
    auInst = eval(dc["AF"])
    auInstInfo = []
    aus = []  # 存这篇paper的所有 作者-机构
    insts = []  # 存这篇paper的所有机构
    for item in auInst:
        for k, v in item.items():
            auInstInfo.append(k + "-" + v)
            aus.append(k)
            insts.append(v)
    paperInfo["auInst"] = ";".join(auInstInfo)

    nodesLs.append(paperInfo)
    nodesLs_all.append(paperInfo)

    # 去重复
    aus = list(set(aus))
    insts = list(set(insts))
    # 存储P-A;P-I
    for k in aus:
        linksLs_all.append({"source": dc["TI"], "target": k, "value": 1})
        if k in auLsMax:
            linksLs.append({"source": dc["TI"], "target": k, "value": 1})
    for v in insts:
        linksLs_all.append({"source": dc["TI"], "target": v, "value": 1})
        if v in instLsMax:
            linksLs.append({"source": dc["TI"], "target": v, "value": 1})

    # try:
    #     ls = eval(dc["AF"])
    #     aus = []
    #     insts = []
    #     for j in ls:
    #         for k, v in j.items():
    #             aus.append(k)
    #             insts.append(v)
    #     # 去重复
    #     aus = list(set(aus))
    #     insts = list(set(insts))
    #     for k in aus:
    #         if k in auLs:
    #             # nodesLs.append({"id": k, "group": 2})
    #             linksLs.append({"source": dc["TI"], "target": k, "value": 1})
    #     for v in insts:
    #         if v in instLs:
    #             # nodesLs.append({"id": v, "group": 3})
    #             linksLs.append({"source": dc["TI"], "target": v, "value": 1})
    # except Exception:
    #     print(i)
    #     print(df.loc[i]["TI"])

print(len(nodesLs))
print(len(nodesLs_all))
print(len(linksLs))
print(len(linksLs_all))

# 添加论文合作连边
count = 0
papers = [name for name in papersLs.keys()]
papers = list(set(papers))
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
