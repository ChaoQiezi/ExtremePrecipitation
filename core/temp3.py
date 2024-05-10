import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import glob

# 准备工作
txt_dir = r'F:\ExtremePrecipitation\extreme_precipitation_py\plot'
# 读取数据
txt_paths = glob.glob(txt_dir + r'\*.txt')
dfs = list(map(lambda x: pd.read_csv(x, sep=r'\s+', header=None), txt_paths[:2]))

# 图预备
sns.set_style('darkgrid')

# 创建一个1x2的网格布局
fig, axes = plt.subplots(2, len(dfs), figsize=(20, 16), dpi=100)

# 对每个数据框，创建一个子图
for i, df in enumerate(dfs):
    df.columns = ["station", "value", "year"]
    df = df.groupby('year').mean().reset_index()
    df['rolling_mean'] = df['value'].rolling(5).mean()
    df['rolling_std'] = df['value'].rolling(5).std()
    df['year'] += 1959
    df['decade'] = df['year'] // 10 * 10
    df['year'] = (df['year'] - 1960) / (2020 - 1960) * 6

    # 在第一个轴上绘制折线图
    ax1 = axes[0, i]
    ax1.plot(df['year'], df['value'], label='Original', color='#4D85BD', marker='o', linestyle='-', linewidth=2)
    ax1.plot(df['year'], df['rolling_mean'], color='#F7903D', label='5-year Moving Average', linestyle='-', linewidth=8)
    ax1.fill_between(df['year'], (df['rolling_mean'] - df['rolling_std']), (df['rolling_mean'] + df['rolling_std']), color='#F7903D', alpha=0.3)

    y_min, y_max = df['value'].min(), df['value'].max()
    ax1.set_ylim(y_min, y_max)
    ax1.set_xlabel('Decades', color='black', fontsize=30)
    ax1.set_ylabel('Precipitation', color='black', fontsize=30)
    ax1.tick_params(axis='y', labelsize=25)
    ax1.tick_params(axis='x', labelsize=25)
    ax1.legend(loc='upper right', fontsize=25)

    # 在第二个轴上绘制箱线图
    ax2 = axes[1, i]
    sns.boxenplot(x="decade", y="rolling_mean", data=df, ax=ax2)
    sns.swarmplot(x="decade", y="rolling_mean", data=df, ax=ax2, alpha=0.6, size=12)
    y_min, y_max = df['value'].min(), df['value'].max()
    ax2.set_ylim(y_min, y_max)
    ax2.tick_params(axis='y', labelsize=25)
    ax2.set_ylabel('Precipitation', color='black', fontsize=30)

fig.tight_layout()
plt.show()
