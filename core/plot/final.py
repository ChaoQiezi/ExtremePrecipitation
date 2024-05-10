# @炒茄子  2023-07-05
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv(r'F:\\ExtremePrecipitation\\extreme_precipitation_py\\plot\\PRCPTOT.txt', sep='\s+', header=None)
df.columns = ["station", "value", "year"]
# 计算年平均值(每年所有站点的平均值)
df = df.groupby('year').mean().reset_index()  # reset_index()用于重置索引
# 计算五年移动平均线以及标准差
df['rolling_mean'] = df['value'].rolling(5).mean()
df['rolling_std'] = df['value'].rolling(5).std()
# 整理数据
df['year'] += + 1959  # 将年份转换为实际年份
df['decade'] = df['year'] // 10 * 10
df['year'] = (df['year'] - 1960) / (2020 - 1960) * 6


# 图预备
plt.ion()  # 开启交互模式
sns.set_style('darkgrid')
fig, ax1 = plt.subplots(figsize=(20, 16), dpi=100)
ax2 = ax1.twinx()
# 创建折线图

ax1.plot(df['year'], df['value'], label='Original', color='#4D85BD', marker='o', linestyle='-', linewidth=2)
ax1.plot(df['year'], df['rolling_mean'], color='#F7903D', label='5-year Moving Average', linestyle='-', linewidth=8)
ax1.fill_between(df['year'], (df['rolling_mean'] - df['rolling_std']),
                 (df['rolling_mean'] + df['rolling_std']), color='#F7903D', alpha=0.3)
# 创建箱线图

sns.boxenplot(x="decade", y="rolling_mean", data=df, ax=ax2)
sns.swarmplot(x="decade", y="rolling_mean", data=df, ax=ax2, alpha=0.6, size=12)

# ax1设置
ax1.set_ylim(3.5, 9)  # 设置y轴刻度范围
ax1.set_xlabel('Decades', color='black', fontsize=30)
ax1.set_ylabel('Precipitation', color='black', fontsize=30)
ax1.tick_params(axis='y', labelsize=25)  # 设置x轴刻度值的字体大小
ax1.tick_params(axis='x', labelsize=25)  # 设置y轴刻度值的字体大小
ax1.legend(loc='upper right', fontsize=25)  # 设置图例位置和大小

# ax2设置
ax2.set_ylim(6.5, 10)  # 设置y轴刻度范围
ax2.tick_params(axis='y', labelsize=25)  # 设置y轴刻度值的字体大小
ax2.set_ylabel('Precipitation', color='black', fontsize=30)

# 共同设置
fig.autofmt_xdate()
plt.title('Precipitation Time Series and Boxplot', fontsize=30)
plt.show()


"""
"""

def precess(dfs):
    # # 重命名列名
    # dfs = list(map(lambda x: x.rename(columns={0: 'station', 1: 'value', 2: 'year'}), dfs))
    # # 计算年平均值(每年所有站点的平均值)
    # dfs = list(map(lambda x: x.groupby('year').mean().reset_index(), dfs))
    # # 计算五年移动平均线以及标准差
    # dfs = list(map(lambda x: x.assign(rolling_mean=x['value'].rolling(5).mean()), dfs))
    # dfs = list(map(lambda x: x.assign(rolling_std=x['value'].rolling(5).std()), dfs))
    # # 整理数据
    # dfs = list(map(lambda x: x.assign(year=(x['year'] - 1) / (2020 - 1960) * 6), dfs))
    # dfs = list(map(lambda x: x.assign(decade=x['year'] // 10 * 10), dfs))

    # 创建一个长度一致的列表
    new_dfs = []
    for df in dfs:
        df.columns = ["station", "value", "year"]
        # 计算年平均值(每年所有站点的平均值)
        df = df.groupby('year').mean().reset_index()  # reset_index()用于重置索引
        # 计算五年移动平均线以及标准差
        df['rolling_mean'] = df['value'].rolling(5).mean()
        df['rolling_std'] = df['value'].rolling(5).std()
        # 整理数据
        df['year'] += + 1959  # 将年份转换为实际年份
        df['decade'] = df['year'] // 10 * 10
        df['year'] = (df['year'] - 1960) / (2020 - 1960) * 6
        new_dfs.append(df)
    return new_dfs

import glob
# 准备工作
txt_dir = r'F:\ExtremePrecipitation\extreme_precipitation_py\plot'
# 读取数据
txt_paths = glob.glob(txt_dir + r'\*.txt')
dfs = list(map(lambda x: pd.read_csv(x, sep=r'\s+', header=None), txt_paths[:2]))
# 预处理数据
dfs = precess(dfs)
df = dfs[0]
plt.ion()
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 16), dpi=100)
axes = axes.flatten()
ax1 = axes[0]

