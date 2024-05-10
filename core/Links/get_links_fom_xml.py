import os
import xml.etree.ElementTree as ET


def xml_to_ftp_links(xml_file):
    # 解析XML文件
    tree = ET.parse(xml_file)  # 这表示解析XML文件
    root = tree.getroot()  # 这表示获取XML文件的根节点

    ftp_links = []

    for file_node in root.iter('File'):  # 这表示获取XML文件中所有名为'File'的节点
        # 获取本地文件路径
        remote_file = file_node.find('RemoteFile').text

        # 把本地文件路径转换成FTP链接
        date = remote_file.split('.')[1]
        year, month, day = date[:4], date[4:6], date[6:8]
        ftp_link = f"ftp://rainmap@hokusai.eorc.jaxa.jp/standard/v7/hourly_G/{year}/{month}/{day}/{remote_file}"

        ftp_links.append(ftp_link)

    return ftp_links


# 使用XML文件生成FTP链接
os.chdir(r'D:\PyProJect\ExtremePrecipitation\docs\links\Gauge')
xml_paths = [path for path in os.listdir(os.getcwd()) if path.endswith('.xml')]
for xml_path in xml_paths:
    xml_file = os.path.join(os.getcwd(), xml_path)
    ftp_links = xml_to_ftp_links(xml_file)

    # 创建txt文件存储FTP链接
    with open(os.path.join(os.getcwd(), xml_path.split('.')[0] + '.txt'), 'w') as f:
        for link in ftp_links:
            f.write(link + '\n')
# xml_file = r'F:\ExtremePrecipitation\extreme_precipitation_py\2020_MVK.xml'  # 把这里的'your_xml_file.xml'替换成你实际的XML文件路径
# ftp_links = xml_to_ftp_links(xml_file)
# # 创建txt文件存储FTP链接
# with open(r'F:\ExtremePrecipitation\extreme_precipitation_py\ftp_links.txt', 'w') as f:
#     for link in ftp_links:
#         f.write(link + '\n')
