# @炒茄子  2023-07-05

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False		# 显示负号


# 准备工作
txt_dir = r'F:\ExtremePrecipitation\extreme_precipitation_py\plot'  # 存放txt文件的目录
units = {  # 单位设置, 键为txt文件名, 值为单位
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
dfs = list(map(lambda x: pd.read_csv(x, sep=r'\s+', header=None), txt_paths))  # '\s+'表示匹配任意空白字符

# 绘制图像
sns.set_style('darkgrid')  # 设置绘图的整体风格
fig, axes = plt.subplots(nrows=len(dfs), figsize=(20, 80/9 * len(dfs)), dpi=100)  # 设置子图的个数, 大小, 分辨率
for index, (ax, df) in enumerate(zip(axes, dfs)):
    df.columns = ["station", "value", "year"]

    # 箱线图的数据预处理
    box_df = df.copy()
    box_df['year'] += 1959
    box_df['decade'] = box_df['year'] // 10 * 10
    box_df['year'] = (box_df['year'] - 1960) / (2020 - 1960) * 6
    box_df['dispersion'] = box_df['value'] - box_df.groupby('decade')['value'].transform('mean')

    # 折线图的数据预处理
    df = df.groupby('year').mean().reset_index()  # 按年份求平均值
    df['rolling_mean'] = df['value'].rolling(5).mean()  # 五年移动平均值
    df['rolling_std'] = df['value'].rolling(5).std()  # 五年移动标准差
    df['year'] += 1959
    df['decade'] = df['year'] // 10 * 10  # 按十年分组
    decade_num = df['decade'].nunique()
    year_min, year_max = df['year'].min(), df['year'].max()
    df['year'] = (df['year'] - year_min) / (year_max - year_min) * (decade_num - 1)
    df['dispersion'] = df['value'] - df.groupby('decade')['value'].transform('mean')

    txt_name = txt_paths[index].split('\\')[-1].split('.')[0]
    txt_unit = units[txt_name]
    txt_describe = txt_name + ' (' + txt_unit + ')'
    ax2 = ax.twinx()
    # Creating line plots
    ax.plot(df['year'], df['value'], label='Original ' + txt_name, color='#4D85BD', marker='o', linestyle='-',
            linewidth=2)
    ax.plot(df['year'], df['rolling_mean'], color='#F7903D', label='5-year Moving Average ' + txt_name, linestyle='-',
            linewidth=8)
    ax.fill_between(df['year'], (df['rolling_mean'] - df['rolling_std']),
                    (df['rolling_mean'] + df['rolling_std']), color='#F7903D', alpha=0.3)

    # 绘制箱线图
    # box_df = df
    # box_df = box_df[box_df['decade'] < 2020]
    sns.boxplot(x='decade', y="dispersion", data=box_df, ax=ax2, width=0.5,
                showfliers=True,  # 设置是否显示异常值
                fliersize=10,  # 设置异常值显示的大小
                showmeans=True,  # 设置是否显示均值
                meanprops={'marker': 'D', 'markerfacecolor': 'red'},  # 均值点的属性设置
                flierprops={'marker': 'o',  # 异常值形状
                            'markerfacecolor': 'red',  # 形状填充色
                            'color': 'black',  # 形状外廓颜色
                            },
                notch=True,  # 是否显示缺口, 缺口所在位置是中位数
                medianprops={'linestyle': '--', 'color': 'gray'},  # 中位数线的属性设置
                palette='Set3',  # 设置调色板
                )

    # 折线图的轴(左)设置
    y_min, y_max = df['value'].min() * 0.25, df['value'].max()
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Decades', color='black', fontsize=30)  # ,
    ax.set_ylabel(txt_describe, color='black', fontsize=30)
    ax.tick_params(axis='y', labelsize=20)  # labelsize=25
    ax.tick_params(axis='x', labelsize=20)  # , labelsize=25
    ax.legend(loc='upper right', fontsize=25)

    # 箱线图的轴(右)设置
    y_min, y_max = box_df['dispersion'].min(), box_df['dispersion'].max() * 1.75
    ax2.set_ylim(y_min, y_max)
    ax2.tick_params(axis='y', labelsize=20)
    ax2.set_ylabel(txt_describe, color='black', fontsize=30)

    # # 设置x轴标签
    xticks = [i for i in range(decade_num)]
    xticklabels = [str(int(decade)) + 's' for decade in df['decade'].unique()]
    ax.set_xticks(xticks)  # 设置x轴刻度
    ax.set_xticklabels(xticklabels, fontsize=25)  # 设置x轴刻度标签
    # # # 每个子图都设置

    # ax.set_xticks(xticks)
    # ax.set_xticklabels(xticklabels, fontsize=25)
    # ax.set_xlim(-0.3, 7.3)  # 设置x轴的范围
    # ax.set_xticks([0, 1, 2, 3, 4, 5, 6])  # 设置x轴刻度
    # ax.set_xticklabels(['1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'], fontsize=25)  # 设置x轴刻度标签



fig.autofmt_xdate()
plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
plt.show()
