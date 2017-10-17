# -*- coding: utf-8 -*-
"""USGS DOI Tool module."""
import yaml
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")  # avoid confusion for cert issues


class DoiSession():
    """ DoiSession enables actions to be taken on the USGS DOI Tool"""
    def __init__(self, env='staging'):
        """init

        :param env: optional default is "staging"
        """
        if env == 'production':
            self._base_doi_url = 'https://www1.usgs.gov/csas/doi/'
        else:
            print('Using Staging Environment\n')
            self._base_doi_url = 'https://www1-staging.snafu.cr.usgs.gov/csas/doi/'

        self._session = requests.Session()


    def doi_authenticate(self, username, password):
        """ Authentication function for the usgs doi tool.

        :param username: Current USGS username (Active Directory).
        :param password: Current USGS user password (Acitve Directory).
        """
        # Fetch application cookie for follow requests.
        cookie_getter = self._session.get(self._base_doi_url, verify=False)

        self._csrf = str(cookie_getter.content).split('name="_csrf" value="')[1].split('"')[0]
        self._username = username  # Save username

        response = self._session.post(self._base_doi_url + 'j_spring_security_check', data = {'j_username': self._username, 'j_password': password, '_csrf': self._csrf}, verify = False) # , verify = False

        if 'crowd.token_key' not in self._session.cookies:
            raise Exception('Login failed')
        self._crowdToken = self._session.cookies['crowd.token_key']
        return self


    def get_doi(self, doi):
        """ Get DOI attributes function that returns the doi fields as a dictionary.

        :parm doi: DOI string ('doi:10.5066/F7SB43S8')

        :returns: dict (DOI fields as a dictionary)

        >>> doi.get_doi('doi:10.5072/FK2J38SV7D')
        {'_csrf': 'cd...',
         'abstractTypeDesc': 'test',
         'addNewCreatorAuthor': None,
         'addNewCreatorAuthorOrcid': None,
         'authorValidity': 'valid',
         'authors[0].authorName': 'Wright, Justin',
         'authors[0].orcId': '',
         'authors[0].position': '0',
         'datasource_id': '17501',
         'date': '',
         'dateType': '[Not Set]',
         'identifier': 'doi:10.5072/FK2J38SV7D',
         'projectDate': '',
         'projectDatePresent': None,
         'projectEndDate': '',
         'projectEndYear': '',
         'projectStartDate': '',
         'projectStartYear': '',
         'projectYear': '',
         'projectYearPresent': None,
         'pubYear': '',
         'publisher': 'U.S. Geological Survey',
         'resourceType': 'Dataset',
         'resourceURL': 'https://usgs.gov/14340938409',
         'save': 'Submit',
         'status': 'public',
         'subject': '2012',
         'title': 'SERVICE TEST ITEM2017-09-25 14:32',
         'usersAndTypes[bserna@usgs.gov]': 'PRIMARY',
         'usersAndTypes[justinwright@usgs.gov]': 'PRIMARY',
         'usersAndTypes[myTest]': 'PRIMARY'}
        """
        fields = {}
        fetch = self._session.get(self._base_doi_url + 'form.htm?doi=' + doi, verify=False)
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
        return fields


    def doi_update(self, doi):
        """ Updating an existing DOI.

        :param doi: DOI Attributes as a dictionary.

        :returns: post response status code
        """
        response_update = self._session.post(self._base_doi_url + 'result.htm', data=doi, verify=False)
        print("Updated DOI: " + str(doi['identifier']))
        return response_update.status_code


    def doi_create(self, doi):
        """ Reserving a DOI.

        :param doi: DOI Attributes as a dictionary.

        :returns: post response
        """
        response_create = self._session.post(self._base_doi_url + 'result.htm', data=doi, verify=False)

        # Retrieve DOI
        doi_number = response_create.text.split('Your DOI has been saved: ')[1].split('</div>')[0].replace(" ","").replace("\n","")
        print("Created DOI: " + str(doi_number))
        return doi_number


def datacite_search(doi):
    """ Datacite API Querying

    :param doi: published doi to query.
    :type: str
    """
    try:
        doi = doi.replace('doi:','')  # If improper format strip.
        r = requests.get('https://api.datacite.org/works/' + str(doi))
        return r.json()
    except Exception as e:
        print(e)


def add_primary_doi_manager(doi_dict, username):
    """ Utility function to add additional doi tool manager (primary)
    :param doi_dict: dictionary that represents a doi
    :param username: AD username
    """
    key = 'usersAndTypes[' + username + ']'
    doi_dict[key] = 'PRIMARY'


def add_backup_doi_manager(doi_dict, username):
    """ Utility function to add additional doi tool manager (backup)
    :param doi_dict: dictionary that represents a doi
    :param username: AD username
    """
    key = 'usersAndTypes[' + username + ']'
    doi_dict[key] = 'BACKUP'
