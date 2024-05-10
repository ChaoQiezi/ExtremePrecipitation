# coding: UTF-8
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
# import logging
import glob
import os
import rasterio
from rasterio.transform import from_origin


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
start_time = datetime.datetime(2018, 9, 6)
end_time = datetime.datetime(2018, 9, 6)
days = (end_time - start_time).days + 1
precipitation_name = 'Precipitation'
lon_name = 'x'
lat_name = 'y'
paths = glob.glob(in_path + r'\*.nc')
# 需要插值的经纬度
new_lon, new_lat = utils.gen_lat_lon(70, 140, 60, 0, 0.036)

for path in paths:
    file_name = os.path.basename(path)
    sv_path = os.path.join(temp_path, file_name)
    # 得到数据块，并存储为nc
    fy4a.get_data_from_data_name(path, precipitation_name, new_lon, new_lat, sv_path=sv_path)
    # 数据对象
    # logging.debug(fy4a.read_FY4A(path))

for day in range(days):
    date = start_time + datetime.timedelta(days=day)
    date_str = date.strftime('%Y%m%d')
    for hour in range(16, 17):
        filename_wildcard = "*NOM_{}{:02d}*.NC".format(date_str, hour)
        paths = glob.glob(os.path.join(temp_path, filename_wildcard))
        # storage box
        dataset_hours = []
        lon = None
        lat = None
        for path in paths:
            with nc.Dataset(path) as ds:
                precip_data = np.array(ds.variables['var'][:])
                precip_data[(precip_data < 0.0) | (precip_data > 50.0)] = np.nan
                dataset_hours.append(precip_data)
                lon = ds['lon'][:]
                lat = ds['lat'][:]
        dataset_per_hour = np.nanmean(np.array(dataset_hours), axis=0)
        write_tiff(os.path.join(out_path, 'Precipitation_{}{:02d}.tif'.format(date_str, hour)),
                   dataset_per_hour, lon, lat)
