import requests
from . import xml_utils
try:
    import pandas as pd
except ImportError:
    pd = None

_BASE_URL = "https://sipp.cr.usgs.gov/SIPPService/"
_USGS_CENTERS_URL = "Centers.ashx"
_USGS_CUSTOMERS_URL = "CustomerDetail.ashx"
_CENTER_MASTER_LIST_URL = "ProjectTaskMaster.ashx?CostCenter={}"
_PROJECT_OVERVIEW_URL = "ProjectXML.ashx?ProjectNumber={}"


def usgs_centers(return_format='df', **kwargs):

    centers_url = _BASE_URL + _USGS_CENTERS_URL
    r = requests.get(centers_url)
    centers = xml_utils.XMLNode(r.text)

    if return_format == 'df' and pd is not None:
        df = _xml2df(centers)
        for key, value in kwargs.items():
            try:
                df = df[df[key].str.match(value)]
            except KeyError:
                print('!'*79)
                print("Field {} not found in result".format(key))
                print('!'*79)
        return df
    else:
        return centers


def center_master_list(cost_center, return_format='df', **kwargs):
    url = _BASE_URL + _CENTER_MASTER_LIST_URL.format(cost_center)
    r = requests.get(url)
    master_list = xml_utils.XMLNode(r.text)

    if return_format == 'df' and pd is not None:
        df = _xml2df(master_list)
        for key, value in kwargs.items():
            try:
                df = df[df[key].str.match(value)]
            except KeyError:
                print('!'*79)
                print("Field {} not found in result".format(key))
                print('!'*79)
        return df
    else:
        return master_list


def _xml2df(xml_node):
    all_records = []
    for child in xml_node.children:
        record = {}
        for subchild in child.children:
            record[subchild.tag] = subchild.text
        all_records.append(record)
    return pd.DataFrame(all_records)