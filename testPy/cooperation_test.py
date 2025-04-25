import pandas as pd

df = pd.read_excel("./output_data/nodes_10y_clean.xlsx")

auNodes = []
# 作者节点
auPairs = {}
# 作者组合次数
auCoop = {}
# 作者合作次数
instNodes = []
# 机构节点
instPairs = {}
# 机构组合次数
instCoop = {}
# 机构合作次数

for i in range(len(df)):
    info = df.loc[i]
    ls = eval(info["AF"])
    aus = []
    insts = []
    for auInst in ls:
        for k, v in auInst.items():
            aus.append(k)
            insts.append(v)
    aus = list(set(aus))
    insts = list(set(insts))
    # 加入节点
    auNodes += aus
    instNodes += insts
    # 合作次数
    for au in aus:
        auCoop[au] = len(aus) - 1 + auCoop.get(au, 0)
    for inst in insts:
        instCoop[inst] = len(insts) - 1 + instCoop.get(inst, 0)
    # 合作组合次数
    for i in range(len(aus)):
        for j in range(i + 1, len(aus)):
            auPairs[(aus[i], aus[j])] = auPairs.get((aus[i], aus[j]), 0) + 1
    for i in range(len(insts)):
        for j in range(i + 1, len(insts)):
            instPairs[(insts[i], insts[j])] = instPairs.get((insts[i], insts[j]), 0) + 1
