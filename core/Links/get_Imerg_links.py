# @Author   : ChaoQiezi
# @Time     : 2023/7/23  8:35
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to ...
"""

import os
import glob
import datetime as dt
from pprint import pprint


# preparation
# in_path = r'F:\ExtremePrecipitation\data\GPM_IMERG_Late'
in_path = r'F:\ExtremePrecipitation\data\GPM_IMERG_Late\2023'
start_time = dt.datetime(2023, 1, 1)
end_time = dt.datetime(2023, 6, 30)
days = (end_time - start_time).days + 1
print('start_time: {}'.format(start_time))
print('end_time: {}'.format(end_time))
print('dataset: {}'.format(os.path.basename(in_path)))

for day in range(days):
    date = start_time + dt.timedelta(days=day)
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
