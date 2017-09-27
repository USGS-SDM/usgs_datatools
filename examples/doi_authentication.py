""" Example python script to authenticate into the DOI Tool.
The function will print a sucess message, the doi_session object
can be reused along with the returned cookie_jar.
"""
from __future__ import print_function
import usgs_datatools.doi as doi
import getpass
import requests
import os

if hasattr(__builtins__, 'raw_input'):
    input = raw_input

doi_session = requests.Session()
username = input('AD Username: ')
password = getpass.getpass('AD Password')

doi_session, cookie_jar = doi.doi_authenticate(doi_session, 's', username, password)
