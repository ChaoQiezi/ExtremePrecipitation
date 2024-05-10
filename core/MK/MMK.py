# @Author   : ChaoQiezi
# @Time     : 2023/7/19  9:42
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to perform MMK trend analysis;
"""

import matplotlib.pyplot as plt
import pymannkendall as mk
import pandas as pd

# preparation
in_path = r'D:\PyProJect\ExtremePrecipitation\docs\stations\CWD.txt'

# prepcessing
ds = pd.read_csv(in_path, sep='\s+', header=None, names=['station', 'value', 'year'])
ds.year += 1959
ds = ds.groupby('year')['value'].mean()

# MK analysis
# yue_wang_modification_test
result1 = mk.yue_wang_modification_test(ds)
# TFPW-MK(trend_free_pre_whitening MK test)
result2 = mk.trend_free_pre_whitening_modification_test(ds)
# sen's slope
slope = mk.sens_slope(ds)

# output
print("""
trend: 这表示了序列的趋势。可能的结果有 "increasing"、"decreasing" 或 "no trend"。

h: 这表示了检验的结果，即在给定的显著性水平下是否可以拒绝原假设。如果 h 为 True，则表示拒绝原假设，也就是说存在趋势。

p: 这是 p 值，表示在原假设为真的情况下得到这样或更极端的结果的概率。在趋势检验中，原假设通常是不存在趋势。一个较小的 p 值（例如小于0.05）通常被用来拒绝原假设，从而得出存在趋势的结论。

z: 这是 Mann-Kendall Z统计量的值。一个正的 Z 值通常对应于上升趋势，一个负的 Z 值则对应于下降趋势。

Tau: 这是 Kendall's Tau，一个衡量序列中一致性对和不一致性对比例的统计量。

s: 这是 S统计量，即一致性对减去不一致性对的总数。

var_s: 这是 S统计量的方差。

slope: 这是 Sen's Slope，表示趋势的斜率。

intercept: 这是根据 Sen's Slope 估计的线性模型的截距。
""")
print('yue_wang_modification_test: ')
print('trend: {}'.format(result1.trend))
print('h: {}'.format(result1.h))
print('p: {}'.format(result1.p))
print('z: {}'.format(result1.z))
print('Tau: {}'.format(result1.Tau))
print('s: {}'.format(result1.s))
print('var_s: {}'.format(result1.var_s))
print('slope: {}'.format(result1.slope))
print('intercept: {}\n'.format(result1.intercept))
print('trend_free_pre_whitening_modification_test: ')
print('trend: {}'.format(result2.trend))
print('h: {}'.format(result2.h))
print('p: {}'.format(result2.p))
print('z: {}'.format(result2.z))
print('Tau: {}'.format(result2.Tau))
print('s: {}'.format(result2.s))
print('var_s: {}'.format(result2.var_s))
print('slope: {}'.format(result2.slope))
print('intercept: {}\n'.format(result2.intercept))
print("sen's slope: {}".format(slope.slope))
print("sen's intercept: {}".format(slope.intercept))


# plot
fig, ax = plt.subplots(figsize=(20, 10), dpi=300)
ax.plot(ds.index, ds.values, label='CWD')
ax.set_xlabel('Year', fontsize=25)
ax.set_ylabel('CWD', fontsize=25)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend(loc='best', fontsize=16)
plt.grid(True, axis='both', linestyle='--', linewidth=1)
plt.title('CWD Time Series and Trend Analysis', fontsize=30)
plt.show()
