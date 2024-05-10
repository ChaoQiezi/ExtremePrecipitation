# @Author   : ChaoQiezi
# @Time     : 2023/7/18  21:48
# @Email    : chaoqiezi.one@qq.com

"""
This script is used to ...
"""

import os
import glob

in_path = r'D:\PyProJect\ExtremePrecipitation\docs\links\NRT'
txt_paths = glob.iglob(os.path.join(in_path, '*.txt'))
content = []
for txt_path in txt_paths:
    with open(txt_path, 'r') as f:
        content.extend(f.readlines())

with open(os.path.join(in_path, 'NRT.txt'), 'w') as f:
    f.writelines(content)