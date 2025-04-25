import json
import networkx as nx
from networkx.algorithms.community import louvain_communities

# 读取 JSON 文件
with open("output_data/sourceJsonTest.json", "r", encoding="utf-8") as f:
    jsonData = json.load(f)  # 解析 JSON 文件

nodes = [i["id"] for i in jsonData["nodes"]]
# print(nodes[0])
# print(len(nodes))

links = [(i["source"], i["target"]) for i in jsonData["links"]]
# print(links[0])
# print(len(links))


G = nx.Graph()

# 添加节点（可选，NetworkX 会自动添加边中的节点）
G.add_nodes_from(nodes)

# 添加边（你自己的数据）
G.add_edges_from(links)

print(len(G.nodes()))

# 运行 Louvain 算法
communities = louvain_communities(G)
# count = 0
# for comm in communities:
#     count += len(comm)
# print(count)


# 将社区划分到最精确
res = 1  # 分辨率默认为1
commNum = len(communities)
preCommNum = -1
print(commNum)
minComm = commNum
i = 0.5
while i < 2:
    communities = louvain_communities(G, resolution=i)
    if minComm > len(communities):
        minComm = len(communities)
    i += 0.1

print(minComm)

# while preCommNum < commNum:
#     preCommNum = commNum
#     res = res + 0.1
#     communities = louvain_communities(G, resolution=res)
#     commNum = len(communities)
# print(commNum)

# def merge_small_communities(G, communities, max_communities):
#     """合并较小的社区，直到满足最大社区数量要求"""
#     while len(communities) > max_communities:
#         # 计算每个社区的大小
#         communities = sorted(communities, key=len)
#         smallest = communities.pop(0)  # 弹出最小的社区
#         # 找到它的邻居社区
#         neighbor_counts = {}
#         # 取出最小社区的节点——找到该节点直连节点
#         # 找到直连节点所在社区号，计算为最小社区到该社区一次
#         for node in smallest:
#             for neighbor in G.neighbors(node):
#                 for idx, comm in enumerate(communities):
#                     if neighbor in comm:
#                         neighbor_counts[idx] = neighbor_counts.get(idx, 0) + 1
#         # 合并到最近的邻居社区
#         if neighbor_counts:
#             best_match = max(neighbor_counts, key=neighbor_counts.get)
#             communities[best_match] = communities[best_match].union(smallest)

#     return communities


# max_communities = 6  # 期望的最大社区数
# merged_communities = merge_small_communities(G, communities, max_communities)
# print(f"合并后社区数: {len(merged_communities)}")

# # print("社区总数：", len(communities))

# # print(edges)
# jsonNodes = jsonData["nodes"]
# print(len(jsonNodes))
# jsonLinks = jsonData["links"]

# nodeDc = {}
# for idx, comm in enumerate(merged_communities):
#     for node in comm:
#         nodeDc[node] = idx + 1

# # 节点数据中加入cluster号
# for i in range(len(jsonNodes)):
#     id = jsonNodes[i]["id"]
#     if id in nodeDc:
#         jsonNodes[i]["cluster"] = nodeDc[id]
#     else:
#         jsonNodes[i]["cluster"] = 0

# # 同一个cluster的边权值增加
# for k in range(len(jsonLinks)):
#     i = jsonLinks[k]["source"]
#     j = jsonLinks[k]["target"]
#     if i in nodeDc and j in nodeDc and nodeDc[i] == nodeDc[j]:
#         jsonLinks[k]["value"] = 10


# jsonData["nodes"] = jsonNodes
# jsonData["links"] = jsonLinks
# with open("./output_data/sourceJsonTest_cluster.json", "w", encoding="utf-8") as f:
#     json.dump(jsonData, f, indent=4, ensure_ascii=False)
