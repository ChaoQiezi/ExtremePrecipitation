# @炒茄子  2023-07-05

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

sns.set_style('darkgrid')
# 准备工作
txt_dir = r'F:\ExtremePrecipitation\extreme_precipitation_py\plot'
units = {
    'CWD': 'days',
    'R10mm': 'days',
    'R25mm': 'days',
    'PRCPTOT': 'mm',
    'SDII': 'mm/day',
    'R95T': 'mm',
    'R99T': 'mm',
    'RX1DAY': 'mm',
    'RX5DAY': 'mm',
}
# 读取数据
txt_paths = glob.glob(txt_dir + r'\*.txt')
dfs = list(map(lambda x: pd.read_csv(x, sep=r'\s+', header=None), txt_paths))

fig, axes = plt.subplots(nrows=len(dfs), figsize=(20, 80), dpi=100)
sns.set_style('darkgrid')
flag = 0
for ax, df in zip(axes, dfs):
    df.columns = ["station", "value", "year"]

    source_df = df.copy()
    source_df['year'] += 1959
    source_df['decade'] = source_df['year'] // 10 * 10
    source_df['year'] = (source_df['year'] - 1960) / (2020 - 1960) * 6
    source_df['dispersion'] = source_df['value'] - source_df.groupby('decade')['value'].transform('mean')

    df = df.groupby('year').mean().reset_index()
    df['rolling_mean'] = df['value'].rolling(5).mean()
    df['rolling_std'] = df['value'].rolling(5).std()
    df['year'] += 1959
    df['decade'] = df['year'] // 10 * 10
    df['year'] = (df['year'] - 1960) / (2020 - 1960) * 6
    df['dispersion'] = df['value'] - df.groupby('decade')['value'].transform('mean')

    txt_name = txt_paths[flag].split('\\')[-1].split('.')[0]
    txt_unit = units[txt_name]
    txt_describe = txt_name + ' (' + txt_unit + ')'
    ax2 = ax.twinx()
    # Creating line plots
    ax.plot(df['year'], df['value'], label='Original '+txt_name, color='#4D85BD', marker='o', linestyle='-', linewidth=2)
    ax.plot(df['year'], df['rolling_mean'], color='#F7903D', label='5-year Moving Average '+txt_name, linestyle='-', linewidth=8)
    ax.fill_between(df['year'], (df['rolling_mean'] - df['rolling_std']),
                 (df['rolling_mean'] + df['rolling_std']), color='#F7903D', alpha=0.3)
    # Creating box plots
    # 将df中decade大于2020年的所有行删除
    df = df[df['decade'] < 2020]
    sns.boxplot(x="decade", y="dispersion", data=source_df, ax=ax2, width=0.5, showfliers=True, showmeans=True)  # showfliers=False表示不显示异常值
    # sns.pointplot(x="decade", y="dispersion", data=df, ax=ax2)  # , ci=None
    # sns.swarmplot(x="decade", y="rolling_mean", data=df, ax=ax2, alpha=0.6, size=12)  # , size=12

    y_min, y_max = df['value'].min() * 0.8, df['value'].max()
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Decades', color='black')  # , fontsize=30
    ax.set_ylabel(txt_describe, color='black', fontsize=30)
    ax.tick_params(axis='y', labelsize=20)  # labelsize=25
    ax.tick_params(axis='x', labelsize=20)  # , labelsize=25
    ax.legend(loc='upper left', fontsize=25)

    y_min, y_max = source_df['dispersion'].min(), source_df['dispersion'].max() * 2
    ax2.set_ylim(y_min, y_max)
    ax2.tick_params(axis='y', labelsize=20)  # , labelsize=25
    ax2.set_ylabel(txt_describe, color='black', fontsize=30)

    # 设置x轴标签
    xticks = [0, 1, 2, 3, 4, 5, 6]
    xticklabels = ['1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
    # 每个子图都设置
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=25)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xticklabels, fontsize=25)
    flag += 1


fig.autofmt_xdate()
plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
plt.show()
