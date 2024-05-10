# @Author   : ChaoQiezi
# @Time     : 2023/7/18  21:54
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to check and get missing url;
"""

from datetime import datetime

from libs._GPM import find_missing

in_path = r'F:\ExtremePrecipitation\data\GSMap-MVK'
url_path = r'D:\PyProJect\ExtremePrecipitation\docs\links\MVK\MVK.txt'
start = datetime(2018, 3, 12)
end = datetime(2023, 6, 28)
missing_dates_hours = find_missing(in_path, start, end, url_path)
