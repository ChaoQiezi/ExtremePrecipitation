# @炒茄子  2023-07-11
import os
import pandas as pd
import numpy as np
import glob


def cal_hurst(ts):
    """
    改进的计算方法
    :param ts: 时间序列数据(np.array)
    :return: 返回Hurst指数
    """

    # 划分时间序列的间隔--步长
    step = 3
    # 不同步长下的时间子序列长度
    x_res = []
    # 不同步长下的R/S值
    y_res = []
    for interval_len in range(step, len(ts), step):
        x_res.append(np.log(interval_len))
        # 按照子区间长度interval_len划分时间间隔
        sub_ts1 = np.array([ts[i:i + interval_len] for i in range(0, len(ts), interval_len) if i + interval_len <= len(ts)])
        start = len(ts) % interval_len
        sub_ts2 = np.array([ts[i:i + interval_len] for i in range(start, len(ts), interval_len)])
        sub_ts = np.concatenate((sub_ts1, sub_ts2), axis=1)
        # 每个子区间的均值
        sub_mean = np.mean(sub_ts, axis=1)
        # 对每个子区间进行累计离差
        sub_cumulative_deviation = np.cumsum(sub_ts - sub_mean.reshape(-1, 1), axis=1)
        # 计算每个子区间的极差
        sub_R = np.max(sub_cumulative_deviation, axis=1) - np.min(sub_cumulative_deviation, axis=1)
        # 计算每个子区间的重标极差值(标准差)
        sub_S = np.std(sub_ts, axis=1)
        # 计算每个子区间的R/S值
        sub_RS = sub_R / sub_S
        # 计算每个子区间的R/S值的均值
        RS = np.mean(sub_RS)
        y_res.append(np.log(RS))

    # 拟合
    h, b = np.polyfit(x=x_res, y=y_res, deg=1)  # h为hurst指数

    return h


# 准备
in_path = r'F:\ExtremePrecipitation\data\precip_stations'

# 读取数据
paths = glob.glob(in_path + r'\*.txt')
names = [os.path.basename(path).split('.')[0] for path in paths]
hurst_D = pd.DataFrame(columns=['name', 'hurst', 'D'])
for index, path in enumerate(paths):
    ts = pd.read_csv(path, sep='\s+', header=None,
                     names=['station', 'prcptot', 'year'])
    # 求取每年所有站点的平均值
    ts = ts.groupby('year').mean()
    # 计算Hurst指数和分形维数(D)
    h = cal_hurst(ts['prcptot'].values)
    D = 2 - h
    hurst_D.loc[index] = [names[index], h, D]
print(hurst_D)
