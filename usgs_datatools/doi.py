# -*- coding: utf-8 -*-
"""USGS DOI Tool module."""
import yaml
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")  # avoid confusion for cert issues


def service_picker(doi_configuration_url):
    """Choses which doi service to use"""
    if doi_configuration_url != 'p' or 'P':
        return 'https://www1-staging.snafu.cr.usgs.gov/csas/doi/'
    else:
        return 'https://www1.usgs.gov/csas/doi/'


def doi_authenticate(r, url, username, password):
    """ Authentication function for the usgs doi tool
    Returns a tuple of session and cookie jar. """
    url = service_picker(url)

    req = r.get(url, verify=False)
    form_csrf = str(req.content).split('name="_csrf" value="')[1].split('"')[0]

    cred = {'j_username': username, 'j_password': password, '_csrf': form_csrf}

    response = r.post(url + 'j_spring_security_check', cookies = req.cookies, data = cred, verify = False) # , verify = False
    cookie_jar = response.cookies

    # Test login success (no change)
    profile_url = url + 'profile.htm'
    profile_test = r.get(profile_url, cookies = cookie_jar, verify = False)
    if profile_test.status_code == 200 and profile_test.url == profile_url:
        print("Successful authentication to DOI TOOL \n")
        return r, cookie_jar
    else:
        print("Error logging the user in, verify correct credentials entered \n")


def get_doi(r, url, doi, cookie_jar):
    """ Get DOI attributes function that returns the doi fields as a dictionary"""
    url = service_picker(url)
    fields = {}
    fetch = r.get(url + 'form.htm?doi=' + doi, cookies=cookie_jar, verify=False)
    soup = BeautifulSoup(fetch.text)

    for inp in soup.find_all('input', ):
        fields[inp.get('name')] = inp.get('value')
    for ta in soup.find_all('textarea',):
        fields[ta.get('name')] = ta.text
    for i in soup.find_all('select'):
        o = i.find_all('option')
        for ii in o:
            if ii.get('selected'):
                fields[i.get('name')] = ii.get('value')
    try:
        del fields[None]
    except:
        pass
    return r, fields


def doi_update(r, url, doi, cookie_jar, cur_time):
    """ Updating an existing DOI
    Expecting a session, environment specification, doi (dict), cookie jar"""
    url = service_picker(url)
    try:
        post_url = url + 'result.htm'
        update_doi = r.post(post_url, cookies =cookie_jar, data=doi, verify=False)

        print("Updated DOI: " + str(doi))
        return update_doi
    except Exception as e:
        print(e)


def doi_create(r, url, doi, cookie_jar):
    url = service_picker(url)
    try:
        post_url = url + 'result.htm'
        update_doi = r.post('https://www1-staging.snafu.cr.usgs.gov/csas/doi/result.htm', cookies =cookie_jar, data=doi, verify=False)

        print("Updated DOI: " + str(doi))
        return update_doi
    except Exception as e:
        print(e)
        return False
