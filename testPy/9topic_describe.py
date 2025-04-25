import pandas as pd

from openai import OpenAI

api_key = "sk-b8a53c99684947b98570308ca2a3aebd"
api_url = "https://api.deepseek.com"
api_model = "deepseek-chat"
# api_model = "deepseek-reasoner"


def generate_cluster_description(keywords, representative_texts):
    """用 GPT 生成类别的描述"""
    prompt = f"""以下是一个研究类别的信息：
    
    关键词: {keywords}
    
    代表论文摘要:
    {"\n\n".join(representative_texts)}
    
    请根据这些信息，请生成该研究类别主题的简要描述，并分别用一句话描述主要的研究内容和研究方法，生成内容不要有“*”。
    比如：
    该集合的研究主题主要是...。
    研究内容主要有：
    1、...，
    2、...，
    3、...
    研究方法主要有：
    1、...，
    2、...，
    3、...
    """
    print("正在请求中...")
    client = OpenAI(api_key=api_key, base_url=api_url)

    response = client.chat.completions.create(
        model=api_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    print("请求成功。")
    return response.choices[0].message.content


df = pd.read_excel("./output_data/kmeans_Info.xlsx")
dfOut = pd.DataFrame(columns=("clusterNum", "topicNum", "describe"))
for idx in range(len(df)):
    row = df.loc[idx]
    keywords = eval(row["topicWords"])
    texts = eval(row["topicAB"])
    describe = generate_cluster_description(keywords, texts)
    n = len(dfOut)
    dfOut.loc[n] = [row["clusterNum"], row["topicNum"], describe]
    print(row["clusterNum"], row["topicNum"])
    # if idx == 3:
    #     break

dfOut.to_excel("./output_data/topic_Info_API.xlsx")
