# -*- coding: utf-8 -*-
""" Metadata Parser module."""

import requests


def validate(local_file):
    """
    :param local_file: Requires a valid XML filepath from your PC.

    :returns: json response

    >>> from usgs_datatools import mp


    >>> mp.validate('~/Documents/BlueRidgeParkway.xml')
    """
    URL_target = 'https://mrdata.usgs.gov/validation/service.php'
    f = {'input_file': open(local_file, 'rb')}

    payload = {
        "a":"mp",
        "upgrade":"yes",
        "indent":"yes",
        "lang":"en",
        "input_type":'file'
    }

    return requests.post(URL_target, data=payload, files = f).json()
