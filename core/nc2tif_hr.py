# @炒茄子  2023-07-02
"""
this script is used to convert the nc4 file to tif file and convert the precipitation half hourly data to
hourly data
"""

import os
import numpy as np
import glob
import datetime
import netCDF4 as nc
import rasterio
import h5py
from pprint import pprint
from rasterio.transform import from_origin


def write_tiff(out_path, dataset, lon, lat, nodata_value):
    """
    this function is used to write the dataset into a tiff file
    :param out_path: path of the output tif file
    :param dataset: the precipitation dataset or other dataset
    :param lon: lon dataset based on the dataset(e.g. precipitation)
    :param lat: lat dataset based on the dataset(e.g. precipitation)
    :param nodata_value: the nodata value of the dataset
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


# preparation
in_path = r'F:\ExtremePrecipitation\data\GPM_IMERG_Late\2018'
out_path = r'E:\DATA\GPM_IMERG_Late_hourly'
start_year = datetime.datetime(2018, 3, 12)
end_year = datetime.datetime(2018, 3, 12)
days = (end_year - start_year).days + 1
precipitation_name = 'precipitationCal'  # all this info by Panoply software
lon_name = 'lon'
lat_name = 'lat'
_fill_value_name = '_FillValue'

# get the path of all the nc4 files
for day in range(days):
    date = start_year + datetime.timedelta(days=day)
    date_str = date.strftime('%Y%m%d')
    for hour in range(24):
        # judge whether two nc4 files exist(two nc4 files for one hour)
        filename_wildcards = '*{}-S{:02d}*.hdf5'.format(date_str, hour)
        paths_nc4 = glob.glob(os.path.join(in_path, filename_wildcards))  # get the generator of the nc4 files
        if len(paths_nc4) != 2:  # this info should be written into the log file(txt), i think
            print()
            print('{} {} {}'.format('-' * 45, filename_wildcards, '-' * 50))
            print('the numberof nc4 files is {}'.format(len(paths_nc4)))
            pprint(paths_nc4)
            print('{} {} {}'.format('-' * 45, filename_wildcards, '-' * 50))
            print()
            continue
        # read the precipitation, lon, lat dataset and some attributes
        with nc.Dataset(paths_nc4[0]) as dataset:
            precipitation0 = dataset.variables[precipitation_name][0, :, :]
            nodata_value = dataset.variables[precipitation_name].getncattr(_fill_value_name)
            lon = dataset.variables[lon_name][:]
            lat = dataset.variables[lat_name][:]
        with nc.Dataset(paths_nc4[1]) as dataset:
            precipitation1 = dataset.variables[precipitation_name][0, :, :]
        precipitation0[precipitation0 == nodata_value] = np.nan
        precipitation1[precipitation1 == nodata_value] = np.nan
        precipitation = (precipitation0 + precipitation1) / 2.0
        precipitation = np.transpose(precipitation)  # because the precipitation is (cols, rows) but the tif is (rows, cols)
        precipitation = np.flipud(precipitation)  # because the precipitation is upside down(probaly the ascending)
        write_tiff(os.path.join(out_path, '{}_{:02d}.tif'.format(date_str, hour)),
                   precipitation, lon, lat, np.nan)
print('done!')

# with rasterio.open(r'F:\ExtremePrecipitation\data\GPM_IMERG_Early_hourly\20180312_00.tif') as dst:
#     print(dst.transform)
#     print(dst.crs)
#     a = dst.read(1)
#
# # 将precipitation0输出为没有坐标系的tif影像文件
# import matplotlib.pyplot as plt
# import numpy as np
#
# precipitation_1 = np.transpose(precipitation0)
# # 将precipitation0的进行转换，x=x, y=-y的形式转换，因为上下颠倒了
# precipitation_2 = np.flipud(precipitation_1)
#
# # 使用matplotlib来显示并保存图像， cmap使用彩色
# plt.imshow(precipitation_2, cmap=plt.cm.jet)
# plt.savefig(r'F:\ExtremePrecipitation\data\GPM_IMERG_Early_hourly\image.png')

