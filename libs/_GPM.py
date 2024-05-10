# @Author   : ChaoQiezi
# @Time     : 2023/7/18  12:07
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to ...
"""

import glob
import os
from pprint import pprint
from datetime import timedelta


def get_links(txt_path, name_wildcard):
    """

    :param in_path:
    :param name_wildcard:
    :return:
    """

    links = []
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if name_wildcard in line:
                links.append(line.strip())

    return links


def find_missing(in_path, start_time, end_time, url_path):
    """

    :param in_path:
    :param start_time:
    :param end_time:
    :return:
    """

    days = (end_time - start_time).days + 1

    for day in range(days):
        date = start_time + timedelta(days=day)
        date_str = date.strftime('%Y%m%d')
        for hour in range(24):
            file_name = '*mvk.{}.{:02d}00*.gz'.format(date_str, hour)
            paths = glob.glob(os.path.join(in_path, file_name))
            if len(paths) != 1:
                # print()
                # print('{} {} {}'.format('-' * 45, file_name, '-' * 50))
                # print('the numberof nc4 files is {}'.format(len(paths)))
                # pprint(paths)
                print('{}.{:02d}'.format(date_str, hour))
                pprint(get_links(url_path, '{}.{:02d}'.format(date_str, hour)))
                # print('{} {} {}'.format('-' * 45, file_name, '-' * 50))
                # print()
                continue