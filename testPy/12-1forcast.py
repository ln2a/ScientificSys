from __future__ import annotations
import json
import pandas as pd

# import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.tsa.arima.model import ARIMA  # ARIMA模型


with open("./output_data/centrality.json", "r", encoding="utf-8") as f:
    jsonData = json.load(f)

current_index = [
    (1, 0),
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 0),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (3, 8),
    (4, 0),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (5, 0),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (6, 0),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),
    (6, 6),
    (6, 7),
    (6, 8),
    (7, 0),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
    (7, 6),
    (7, 7),
    (8, 0),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
    (8, 5),
    (8, 6),
    (8, 7),
    (9, 0),
    (9, 1),
    (9, 2),
    (9, 3),
    (9, 4),
    (9, 5),
    (9, 6),
    (9, 7),
    (9, 8),
    (10, 0),
    (10, 1),
    (10, 2),
    (10, 3),
    (10, 4),
    (10, 5),
    (10, 6),
]
current_index2 = [(1, 4), (1, 1)]


def func(current_type, current_cluster, current_topic):
    # 选择cluster
    need_data = []
    for i in jsonData[current_type]:
        if i["cluster"] == current_cluster:
            need_data.append((i["topic"], i["year"], i["value"]))

    print(need_data)
    # 选择topic
    x = [i[1] for i in need_data if i[0] == current_topic]
    y = [i[2] for i in need_data if i[0] == current_topic]
    print(x)
    print(y)
    data = {
        "time_data": pd.to_datetime(x, format="%Y"),
        "deal_data": y,
    }

    df = pd.DataFrame(data)

    df.set_index(["time_data"], inplace=True)  # 将时间戳设置为索引

    data = df
    print(data)
    # 用来正常显示中文标签
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
    # 绘图
    data.plot()
    # 图片展示
    # plt.show()

    # 绘制自相关图
    # plot_acf(data).show()
    # 绘制偏自相关图
    # plot_pacf(data).show()
    # 平稳性检测
    if len(set(y)) == 1:
        forecast = [y[0], 0]
    else:
        adf_result = ADF(data)
        print("原始序列的ADF检验结果为：", adf_result)
        count = 0  # 阶数
        # 第二个参数大于0.05说明数据不稳定
        # 如果p-value大于0.05，说明数据可能不是平稳的，需要差分
        data_diff = data
        if adf_result[1] > 0.05:
            print("数据不是平稳的，需要差分")
            count += 1
            # 差分化
            data_diff = data_diff.diff().dropna()
            # 再次进行平稳性检验
            adf_result_diff = ADF(data_diff)
            print(f"差分后 ADF p-value: {adf_result_diff}")
        print("阶数为：%s" % count)
        # 偏自相关图
        # plot_pacf(data_diff).show()
        # 自相关图
        # plot_acf(data_diff).show()
        # 选择pdq
        pmax = int(len(data_diff) / 2)
        qmax = int(len(data_diff) / 2)
        bic_matrix = []  # BIC矩阵
        # 差分阶数
        diff_num = count

        for p in range(pmax):
            tmp = []
            for q in range(qmax):
                try:
                    tmp.append(ARIMA(data_diff, order=(p, diff_num, q)).fit().bic)
                except Exception as e:
                    print(e)
                    tmp.append(None)
            bic_matrix.append(tmp)
        bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值
        p, q = (
            bic_matrix.stack().idxmin()
        )  # 先用stack展平，然后用idxmin找出最小值位置。
        print("BIC最小的p值和q值为：%s、%s" % (p, q))
        print("阶数为：%s" % diff_num)
        # 构建ARIMA模型
        model = ARIMA(data, order=(p, diff_num, q))
        model_fit = model.fit()

        # 进行预测，预测未来一年（2025年）
        forecast = model_fit.forecast(steps=1)  # 预测1步

    # 显示预测结果
    print(f"预测2025年: {forecast[0]}")
    # 新的数据加入excel中
    new_data = pd.read_excel("./output_data/forecast_data.xlsx", index_col=0)
    newrow = {
        "type": current_type,
        "cluster": current_cluster,
        "topic": current_topic,
        2025: forecast[0],
    }
    new_data.loc[len(new_data)] = newrow
    print(newrow)
    print("final:%s" % y[-1])
    new_data.to_excel("./output_data/forecast_data.xlsx")
    new_data = pd.read_excel("./output_data/forecast_data.xlsx", index_col=0)
    print(new_data.tail())


def pause():
    input("pause ")


def func_out():

    for i, j in current_index:
        current_type = "betweenness"
        current_cluster = i
        current_topic = j
        func(current_type, current_cluster, current_topic)
        pause()


func_out()
