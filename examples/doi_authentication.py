""" Example python script to authenticate into the DOI Tool.
The function will print a sucess message, the doi_session object
can be reused along with the returned cookie_jar.
"""
from __future__ import print_function
from usgs_datatools import doi
import getpass
import requests
import os

if hasattr(__builtins__, 'raw_input'):
    input = raw_input

doi_session = doi.DoiSession(env='staging')
username = input('AD Username: ')
password = getpass.getpass('AD Password')

doi_session.doi_authenticate(username, password)
