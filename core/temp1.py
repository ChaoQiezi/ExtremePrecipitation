# @Author   : ChaoQiezi
# @Time     : 2023/7/24  23:55
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to ...
"""


import netCDF4 as nc


in_path = r'F:\ExtremePrecipitation\data\LWX\FY4A-_AGRI--_N_REGC_1047E_L2-_QPE-_MULT_NOM_20180316113000_20180316113416_4000M_V0001.NC'

with nc.Dataset(in_path) as ds:
    precip = ds.variables['Precipitation'][:]
    print(precip.shape)

# find the max
print(precip.max())
