""" Example python script to authenticate into the DOI Tool
Replace either yaml file with USGS AD username/password
The function will print a sucess message, the doi_session object
can be reused along with the returned cookie_jar.
"""
import usgs_datatools.doi as doi
import yaml
import requests
import os

credentials = yaml.load(open(os.path.expanduser('~') + '/cred.yaml').read())
doi_session = requests.Session()

doi_session, cookie_jar = doi.doi_authenticate(doi_session, 's', credentials['application_credentials']['username'], credentials['application_credentials']['password'])
