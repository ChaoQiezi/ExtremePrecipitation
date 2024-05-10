# @Author   : ChaoQiezi
# @Time     : 2023/7/23  9:43
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to ...
"""

import os
import numpy as np
import glob
import datetime
import rasterio
import h5py
from pprint import pprint
from rasterio.transform import from_origin
from osgeo import gdal


def write_tiff(out_path, dataset, transform, nodata_value=np.nan):
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
                       transform=transform) as dst:
        dst.write(dataset, 1)  # write the precipitation dataset into the first band of the tif file


def write_tiff2(out_path, dataset, transform, nodata_value=np.nan):
    """
    this function is used to write the dataset into a tiff file
    :param out_path:
    :param dataset:
    :param transform:
    :param nodata_value:
    :return:
    """

    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(out_path, cols, rows, 1, gdal.GDT_Float32)

    ds.SetGeoTransform(transform)
    ds.SetProjection('WGS84')  # +proj=latlong
    ds.GetRasterBand(1).WriteArray(dataset)
    ds.GetRasterBand(1).SetNoDataValue(nodata_value)
    ds.FlushCache()
    ds = None


# preparation
in_path = r'F:\ExtremePrecipitation\data\GPM_IMERG_Late\2018'
shp_path = r'F:\ExtremePrecipitation\data\basic\研究区\Yangtze_rever_basin.shp'
out_path = r'D:\ChaoQiezi\Pictures'
start_year = datetime.datetime(2018, 3, 12)
end_year = datetime.datetime(2018, 3, 12)
days = (end_year - start_year).days + 1
precipitation_name = 'precipitationCal'  # all this info by Panoply software
lon_name = 'lon'
lat_name = 'lat'
_fill_value_name = '_FillValue'
# rows = 1800
# cols = 3600
# transform = (-179.9999830585056, 0.09997222052680121, 0, 89.99996916876898, 0, -0.09994444105360244)

# get the path of all the nc4 files
for day in range(days):
    date = start_year + datetime.timedelta(days=day)
    date_str = date.strftime('%Y%m%d')
    for hour in range(1):
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
        with h5py.File(paths_nc4[0], 'r') as f:
            lon = f['Grid'][lon_name][:]
            lat = f['Grid'][lat_name][:]
            precipitation0 = f['Grid'][precipitation_name][0, :, :]
            nodata_value = f['Grid'][precipitation_name].attrs[_fill_value_name]
        with h5py.File(paths_nc4[1], 'r') as f:
            precipitation1 = f['Grid'][precipitation_name][0, :, :]
        precipitation0[precipitation0 == nodata_value] = np.nan
        precipitation1[precipitation1 == nodata_value] = np.nan
        # mean the two precipitation dataset
        precipitation = np.nanmean(np.stack([precipitation0, precipitation1]), axis=0)
        # precipitation = np.transpose(precipitation)  # because the precipitation is (cols, rows) but the tif is (rows, cols)
        # precipitation = np.flipud(precipitation)  # because the precipitation is upside down(probaly the ascending)
        precipitation = np.rot90(precipitation)

        # write the precipitation into a tif file
        rows = len(lat)
        cols = len(lon)
        lon_res = (max(lon) - min(lon)) / cols
        lat_res = (max(lat) - min(lat)) / rows
        transform = (min(lon), lon_res, 0, max(lat), 0, -lat_res)
        out_temp_path = os.path.join(out_path, '{}_{:02d}.tif'.format(date_str, hour))
        write_tiff2(out_temp_path, precipitation, transform)

        # clip and mask
        out_clip_path = os.path.join(out_path, 'clip_{}_{:02d}.tif'.format(date_str, hour))
        gdal.Warp(out_clip_path, out_temp_path, cutlineDSName=shp_path, cropToCutline=True, dstNodata=np.nan)
        os.remove(out_temp_path)

print('done!')