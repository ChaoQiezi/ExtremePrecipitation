1# coding: UTF-8
"""
@Project: codes
@FileName: main.py
@author: shi yao  <aiwei169@sina.com>
@create date: 2021/9/28 14:45
@Software: PyCharm
python version: python 3.6.13
"""

import datetime
import netCDF4 as nc
from FY.fy4a import FY4A
from FY import utils, components
import numpy as np
import glob
import os
import rasterio
from rasterio.transform import from_origin
from osgeo import gdal


def write_tiff(out_path, dataset, lon, lat, nodata_value=np.nan):
    """
    this function is used to write tiff file
    :param dataset: band of tiff file
    :param lon: longitude
    :param lat: latitude
    :return: None
    """

    # get the basic info of the precipitation
    rows = len(lat)
    cols = len(lon)
    lon_res = (max(lon) - min(lon)) / cols
    lat_res = (max(lat) - min(lat)) / rows
    lon_upper_left = min(lon) - lon_res / 2.0
    lat_upper_left = max(lat) + lat_res / 2.0
    """
    lon_res = lon[1] - lon[0]  # assume the lon and lat are equally spaced
    lat_res = lat[1] - lat[0]
    """

    # write the precipitation data into a tif file
    with rasterio.open(out_path, 'w', driver='GTiff',
                       height=rows, width=cols,
                       count=1, dtype=dataset.dtype,
                       crs='+proj=latlong',  # the coordinate acrually is WGS84
                       nodata=nodata_value,  # (x_res, x_skew, x_ul, y_skew, y_res, y_ul) = dst.transform
                       transform=from_origin(lon_upper_left, lat_upper_left, lon_res, lat_res)) as dst:
        dst.write(dataset, 1)  # write the precipitation dataset into the first band of the tif file


arg = components.Arg()
arg_parsed = arg.arg_parse('-d'.split())  # 代码输入参数
# arg_parsed = arg.arg_parse()  # 命令行输入参数
fy4a = FY4A(arg_parsed)

# preparation
in_path = r'G:\Objects\ExtremePrecipitation\Datasets\FY4A'
temp_path = r'F:\ExtremePrecipitation\data\TEMP\Output'
out_path = r'F:\ExtremePrecipitation\data\TEMP\Output'
shp_path = r'F:\ExtremePrecipitation\data\basic\研究区\长江流域.shp'
start_time = datetime.datetime(2018, 9, 6)
end_time = datetime.datetime(2018, 9, 6)
print('start time: {}'.format(start_time))
print('end time: {}'.format(end_time))
days = (end_time - start_time).days + 1
precipitation_name = 'Precipitation'
lon_name = 'x'
lat_name = 'y'
# paths = glob.glob(in_path + r'\*.nc')
# 需要插值的经纬度
new_lon, new_lat = utils.gen_lat_lon(-170, 170, 80, -80, 0.036)

# for path in paths:
#     file_name = os.path.basename(path)
#     sv_path = os.path.join(temp_path, file_name)
#     # 得到数据块，并存储为nc
#     fy4a.get_data_from_data_name(path, precipitation_name, new_lon, new_lat, sv_path=sv_path)
#     # 数据对象
#     # logging.debug(fy4a.read_FY4A(path))

for day in range(days):
    date = start_time + datetime.timedelta(days=day)
    date_str = date.strftime('%Y%m%d')
    for hour in range(0, 1):
        filename_wildcard = "*QPE*.nc".format(date_str, hour)
        paths = glob.glob(os.path.join(in_path, filename_wildcard))
        if len(paths) == 0:
            print('Time: {}{:02d} is not exist'.format(date_str, hour))
            continue
        # storage box
        dataset_hours = []
        lon = None
        lat = None

        for path in paths:
            file_name = os.path.basename(path)
            sv_path = os.path.join(temp_path, file_name)
            # 得到数据块，并存储为nc
            try:
                fy4a.get_data_from_data_name(path, precipitation_name, new_lon, new_lat, sv_path=sv_path)
            except:
                print('Time: {}{:02d} can not open'.format(date_str, hour))
                continue

        paths = glob.glob(os.path.join(temp_path, filename_wildcard))
        for path in paths:
            with nc.Dataset(path) as ds:
                precip_data = np.array(ds.variables['var'][:])
                precip_data[(precip_data < 0.0) | (precip_data > 50.0)] = np.nan
                dataset_hours.append(precip_data)
                lon = ds['lon'][:]
                lat = ds['lat'][:]
            os.remove(path)
        dataset_per_hour = np.nanmean(np.array(dataset_hours), axis=0)
        write_tiff(os.path.join(out_path, 'Precipitation_{}{:02d}.tif'.format(date_str, hour)),
                   dataset_per_hour, lon, lat)
        # clip and mask
        # dataset = gdal.Open(os.path.join(out_path, 'Precipitation_{}{:02d}.tif'.format(date_str, hour)))  # open the tiff file

        # gdal.Warp(os.path.join(out_path, 'Clip_Precipitation_{}{:02d}.tif'.format(date_str, hour)), dataset,
        #           cutlineDSName=shp_path, cropToCutline=True)
        # close
        # dataset = None
        # delete temp file
        # os.remove(os.path.join(out_path, 'Precipitation_{}{:02d}.tif'.format(date_str, hour)))


# # 按掩膜提取
#
# import numpy as np
# import netCDF4 as nc
# from osgeo import gdal, osr, ogr
# import os
# import glob
#
# shp = r"D:\DATA\TIFF\mask\poly.shp"  # 圈选范围的路径
# Input_folder = r"D:\DATA\nc\REA\2016\2016"  # 要裁剪的tif文件所在的文件夹
# data_list = glob.glob(Input_folder + '/*.tif')  # 读取文件
# for i in range(len(data_list)):
#     data = data_list[i]
#     inputImage = data  # 遥感影像的路径
#     dataset = gdal.Open(inputImage)  # 打开遥感影像
#     num = i + 1  # 为了方便写入文件的名字
#     outputImage = r"D:\DATA\nc\REA\mask\2016-" + str(num) + ".tif"  # 按照圈选范围提取出的影像所存放的路径
#     gdal.Warp(outputImage, dataset, cutlineDSName=shp, cropToCutline=True)  # 按掩膜提取
#
# print(data + '-----转tif成功')

