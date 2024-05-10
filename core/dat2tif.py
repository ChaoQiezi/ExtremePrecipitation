# @炒茄子  2023-07-02

"""
this script is used to preprocess the GSMao-MVK data, include format concert(.dat ==> .tiff), clip and mask, and

"""

import gzip
import os
import glob
import numpy as np
from datetime import datetime, timedelta
from osgeo import gdal
from pprint import pprint


# preparation
# in_path = r'F:\ExtremePrecipitation\data\GSMap-MVK'
# out_path = r'E:\DATA\GSMap_MVK'
# in_path = r'F:\ExtremePrecipitation\data\GSMap_Gauge'
# out_path = r'E:\DATA\GSMap_Gauge'
in_path = r'F:\ExtremePrecipitation\data\GSMap-NRT'
out_path = r'E:\DATA\GSMap_NRT'
shp_path = r'F:\ExtremePrecipitation\data\basic\研究区\Yangtze_rever_basin.shp'
print('DATASET: {}'.format(os.path.basename(in_path)))
start_year = datetime(2023, 1, 1)
end_year = datetime(2023, 6, 30)
print('start year: {}'.format(start_year))
print('end year: {}'.format(end_year))
days = (end_year - start_year).days + 1
# dataset basic information
rows = 1200
cols = 3600
lon_upper_left = 0
lat_upper_left = 60
lon_res = 0.1
lat_res = 0.1
_type = np.float32  # because 4-Bytes floats means 32 bits floats, 1 Byte = 8 bits

# generate the empty dataset(1200row, 3600col
dataset = np.zeros((rows, cols), dtype=_type)
for day in range(days):
    date = start_year + timedelta(days=day)
    date_str = date.strftime('%Y%m%d')
    for hour in range(24):
        file_name = '*{}.{:02d}00*.gz'.format(date_str, hour)
        paths = glob.glob(os.path.join(in_path, file_name))
        if len(paths) != 1:
            print()
            print('{} {} {}'.format('-' * 45, file_name, '-' * 50))
            print('the number of nc4 files is {}'.format(len(paths)))
            pprint(paths)
            print('{} {} {}'.format('-' * 45, file_name, '-' * 50))
            print()
            continue
        gz_path = paths[0]
        out_temp_path = os.path.join(out_path, '{}.tif'.format(os.path.basename(gz_path)[:-3]))
        # get data from .gz file
        with gzip.open(gz_path, 'rb') as f:
            data = f.read()
            data = np.frombuffer(data, dtype=_type)
            data = np.array(data).reshape(rows, cols)
            data[data < 0] = np.nan

        # write data to .tif file
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(out_temp_path, cols, rows, 1, gdal.GDT_Float32)  # 1 means one band
        out_ds.SetGeoTransform((lon_upper_left, lon_res, 0, lat_upper_left, 0, -lat_res))
        out_ds.SetProjection('WGS84')
        out_ds.GetRasterBand(1).WriteArray(data)
        out_ds.FlushCache()
        out_ds = None

        # clip and mask
        out_clip_path = os.path.join(out_path, '{}_clip.tif'.format(os.path.basename(gz_path)[:-3]))
        gdal.Warp(out_clip_path, out_temp_path, cutlineDSName=shp_path, cropToCutline=True, dstNodata=np.nan)

        # delete the original .tif file
        os.remove(out_temp_path)

