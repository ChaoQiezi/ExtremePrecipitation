# @Author   : ChaoQiezi
# @Time     : 2023/7/22  22:28
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to find missing data in the solved FY4A data
"""

import glob
import os
import datetime as dt

in_path = r'F:\ExtremePrecipitation\data\TEMP\Output'
start_time = dt.datetime(2018, 3, 12)
end_time = dt.datetime(2023, 7, 8)

days = (end_time - start_time).days + 1

for day in range(days):
    date = start_time + dt.timedelta(days=day)
    date_str = date.strftime('%Y%m%d')
    for hour in range(0, 24):
        filename_wildcard = "Clip_Precipitation_{}{:02d}.tif".format(date_str, hour)
        paths = glob.glob(os.path.join(in_path, filename_wildcard))
        if len(paths) == 0:
            print('Time: {}{:02d} is not exist'.format(date_str, hour))