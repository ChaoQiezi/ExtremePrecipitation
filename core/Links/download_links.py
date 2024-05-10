# @炒茄子  2023-07-06

from pydap.client import open_url
from pydap.cas.urs import setup_session

dataset_url = 'https://gpm1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi?FILENAME=%2Fdata%2FGPM_L3%2FGPM_3IMERGHHL.06%2F2023%2F001%2F3B-HHR-L.MS.MRG.3IMERG.20230101-S000000-E002959.0000.V06C.HDF5&VERSION=1.02&FORMAT=bmM0Lw&BBOX=3%2C73%2C54%2C136&SHORTNAME=GPM_3IMERGHHL&SERVICE=L34RS_GPM&LABEL=3B-HHR-L.MS.MRG.3IMERG.20230101-S000000-E002959.0000.V06C.HDF5.SUB.nc4&DATASET_VERSION=06'

username = 'Chaoqiezi'
password = 'QWEqwe510928!'

try:
    session = setup_session(username, password, check_url=dataset_url)
    dataset = open_url(dataset_url, session=session)
except AttributeError as e:
    print('Error:', e)
    print('Please verify that the dataset URL points to an OPeNDAP server, the OPeNDAP server is accessible, or that your username and password are correct.')