# @Author   : ChaoQiezi
# @Time     : 2023/7/17  22:19
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to ...
"""

import os
import glob
import netCDF4 as nc
import numpy as np
from libs.func import write_tiff, glt_warp, fy4a_calibration, get_lon_lat, clip, read_geo, row_col_2_lon_lat

def read_var(nc_file_path, var_name):
    """
    读取nc文件中的数据
    :param nc_file_path: nc文件路径
    :param var_name: 变量名
    :return: 变量值
    """
    nc_file = nc.Dataset(nc_file_path)
    var = nc_file[var_name][:]
    nc_file.close()

    return var

# 准备工作
in_path = r'F:\ExtremePrecipitation\data\TEMP\REGC'
out_path = r'F:\ExtremePrecipitation\data\TEMP\Output\temp'
row_name = 'LineNumber'  # 像元行号矩阵, 来自*GEO*.hdf(上geo_path)
col_name = 'ColumnNumber'  # 像元列号矩阵, 同上
out_res = 0.036  # 0.036为输出的分辨率(°/度), 约为4km


paths = glob.glob(in_path + r'\*.nc')

for path in paths:
    df = nc.Dataset(path)
    # get the bias of row and column
    l_bias = df['geospatial_lat_lon_extent'].begin_line_number
    c_bias = df['geospatial_lat_lon_extent'].begin_pixel_number
    rows = read_var(path, 'x')  # dimension: 1124
    cols = read_var(path, 'y')  # dimension: 2748
    # deal with lon and lat base on the bias
    rows += l_bias
    cols += c_bias
    col_mesh, row_mesh = np.meshgrid(cols, rows)
    col_mesh, row_mesh = np.array(col_mesh), np.array(row_mesh)
    # get the lon and lat
    # lon, lat = row_col_2_lon_lat(cols, rows)
    # col_mesh, row_mesh = np.meshgrid(cols, rows)
    # col_mesh, row_mesh = np.array(col_mesh), np.array(row_mesh)
    # lon, lat = lon.T, lat.T
    band = read_var(path, 'Precipitation')  # dimension: 1124*2748
    hh, ww = band.shape
    l = np.repeat(np.array([np.arange(hh)]).T, ww, axis=1) + l_bias
    c = np.repeat(np.array([np.arange(ww)]), hh, axis=0) + c_bias
    lon, lat = row_col_2_lon_lat(row_mesh, col_mesh)
    band[(band < 0) | (band > 50)] = np.nan
    # q = read_var(in_path, 'geospatial_lat_lon_extent')
    # a, b = np.meshgrid(lat, lon)  # dimension: 2748*1124
    # 裁剪
    reform_band, reform_lon, reform_lat = clip(band, lon, lat, (70, 140, 0, 60))
    # 校正
    interp_band = glt_warp(reform_band, reform_lon, reform_lat, out_res, method='linear')  # 0.036°大约是4km
    # 仿射变换参数
    transform = (
        np.nanmin(reform_lon),  # 左上角经度
        out_res,  # x方向分辨率
        0,  # 旋转角度
        np.nanmax(reform_lat),  # 左上角纬度
        0,  # 旋转角度
        -out_res,  # y方向分辨率, 由于自左上角开始(纬度往下逐渐减小), 因此为负;
    )
    # 输出
    print('Writing tiff file ...')
    out_ = out_path + '\\' + os.path.basename(path).split('.')[0] + '.tif'
    write_tiff(out_, [interp_band], transform)

