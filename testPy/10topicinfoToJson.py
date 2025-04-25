import pandas as pd
import json

df = pd.read_excel("./output_data/topic_info_API.xlsx")

topicInfo = {}
for i in range(len(df)):
    data = df.loc[i]
    cluster = int(data["clusterNum"])
    topic = int(data["topicNum"])
    des = data["describe"]
    if cluster not in topicInfo:
        topicInfo[cluster] = {}
    topicInfo[cluster][topic] = des

with open("./output_data/topicInfoJson.json", "w", encoding="utf-8") as f:
    json.dump(topicInfo, f, indent=4, ensure_ascii=False)
