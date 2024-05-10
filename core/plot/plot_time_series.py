# @炒茄子  2023-07-05
"""
这个脚本用于绘制时间序列箱线图
"""
import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv(r'F:\ExtremePrecipitation\extreme_precipitation_py\plot\CWD.txt', sep='\s+', header=None)
df.columns = ["station", "value", "year"]
df['year'] += 1959  # 将年份转换为实际年份

# 计算年平均值(每年所有站点的平均值)
df = df.groupby('year').mean().reset_index()  # reset_index()用于重置索引
# 计算五年移动平均线以及标准差
df['rolling_mean'] = df['value'].rolling(5).mean()
df['rolling_std'] = df['value'].rolling(5).std()

# 绘制时间序列图
fig, ax1 = plt.subplots(figsize=(20, 10))
# sns.set_style('darkgrid')  # style主要有darkgrid, whitegrid, dark, white, ticks,
ax1.plot(df['year'], df['value'], label='Original', color='black', marker='o', linestyle='-', linewidth=2)
ax1.plot(df['year'], df['rolling_mean'], color='red', label='5-year Moving Average', linestyle='-',
         linewidth=8)
ax1.fill_between(df['year'], (df['rolling_mean'] - df['rolling_std']),
                 (df['rolling_mean'] + df['rolling_std']), color='blue', alpha=0.3)
ax1.set_ylabel('Precipitation', color='black', fontsize=25)
ax1.set_xlabel('Year', color='black', fontsize=25)
ax1.legend(loc='best', fontsize=16)

# 箱线图的绘制
ax2 = ax1.twinx()
# 首先根据年份分组，计算每十年的降水量
decade_df = df.groupby(df['year'] // 10)['value'].apply(list)
# 绘制箱线图
ax2.boxplot(decade_df.values, positions=decade_df.index * 10 + 5, widths=4, patch_artist=True,
            boxprops=dict(facecolor='blue', color='blue')) # 箱体属性
ax2.set_ylabel('Precipitation - Boxplot', color='black', fontsize=25)
# 设置坐标轴刻度
ax1.tick_params(axis='x', labelsize=20)
ax1.tick_params(axis='y', labelsize=20)
ax1.set_xlim(1960, 2021)  # 设置x轴刻度范围
ax1.set_ylim(3.5, 9)  # 设置y轴刻度范围
ax2.tick_params(axis='y', labelsize=20)
ax2.set_ylim(5.5, 12)  # 设置y轴刻度范围
# 自动调整日期显示方式
fig.autofmt_xdate()
plt.grid(True, axis='both', linestyle='--', linewidth=1)
plt.title('Precipitation Time Series and Boxplot', fontsize=30)
plt.show()

