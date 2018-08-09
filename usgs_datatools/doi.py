# -*- coding: utf-8 -*-

"""
usgs_datatools.doi
------------------

This python module provides a user session and additional functionality for
the USGS Digitial Object Identifier creation tool.
"""
import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore")  # avoid confusion for cert issues


class DoiSession:
    """A USGS DOI tool session.

    Basic Usage::
      >>> import usgs_datatools
      >>> s = usgs.datatools.doi.DoiSession()
      >>> s.doi_authenticate("user", "password")
    """

    def __init__(self, env="staging"):
        """Defines the tools environment for testing or production dois.

        The production environment creates live identifiers. The other
        environments represent the various releases of the tool for testing
        purposes.

        :param env: (optional) String, the default is staging where test
            dois can be created.
        """
        if env == "production":
            self._base_doi_url = "https://www1.usgs.gov/csas/dmapi/"
<<<<<<< HEAD
        elif env == "dev":
=======
        if env == "dev":
>>>>>>> 6c7d1fde15068be36c6376069af74bb278a4fb75
            self._base_doi_url = (
                "https://www1-dev.snafu.cr.usgs.gov/csas/dmapi/"
            )
        else:
            self._base_doi_url = (
                "https://www1-staging.snafu.cr.usgs.gov/csas/dmapi/"
            )

        self._session = requests.Session()

    def doi_authenticate(self, username, password):
        """User authentication updated for the new dmapi.

        :param username: String, current USGS username (Active Directory).
        :param password: String, current USGS user password (Acitve Directory).
        """
        response_status = self._session.post(
            self._base_doi_url + "login",
            json={"username": username, "password": password},
        )
        if response_status.status_code == 200:
            return self
        else:
            return {
                "error": response_status.status_code,
                "message": response_status.text,
            }


    def get_my_dois(self):
        """Current users dois"""
        response_status = self._session.get(
            self._base_doi_url + "doi/" + "all"
        )
        if response_status.status_code == 200:
            return response_status.json()
        else:
            return {
                "error": response_status.status_code,
                "message": response_status.text,
            }

    def get_doi(self, doi):
        """Get DOI attributes function that returns the doi fields as a dictionary.

        :parm doi: String, doi identifier.
            Example: ('doi:10.5066/F7SB43S8')

        :returns: Dictionary, DOI fields as a dictionary.

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
        response_status = self._session.get(
            self._base_doi_url + "doi/" + doi
        )
        if response_status == 200:
            return response_status.json()
        else:
            return {
                "error": response_status.status_code,
                "message": response_status.text,
            }


    def doi_update(self, doi):
        """ Updating an existing DOI.

        :param doi: DOI Attributes as a dictionary.

        :returns: post response status code
        """
        response_status = self._session.put(
            self._base_doi_url + "doi/" + doi["doi"], json=doi
        )
        if response_status.status_code == 200:
            return response_status.json()
        else:
            return {
                "error": response_status.status_code,
                "message": response_status.text,
            }


    def doi_create(self, doi):
        """ Reserving a DOI.

        :param doi: DOI Attributes as a dictionary.

        :returns: post response

        >>> doi_create(doi_dict)
        """
        response_status = self._session.post(
            self._base_doi_url + "doi/", json=doi
        )
        if response_status.status_code == 200:
            return response_status.text
        else:
            return {
                "error": response_status.status_code,
                "message": response_status.text,
            }


def datacite_search(doi):
    """Datacite API Querying.

    :param doi: published doi to query.
    :type: str
    """
    try:
        doi = doi.replace("doi:", "")  # If improper format strip.
        r = requests.get("https://api.datacite.org/works/" + str(doi))
        return r.json()
    except Exception as e:
        print(e)


def add_primary_doi_manager(doi_dict, username):
    """Utility function to add additional doi tool manager (primary)
    :param doi_dict: Dictionary that represents a doi
    :param username: String, active directory username
    """
    key = "usersAndTypes[" + username + "]"
    doi_dict[key] = "PRIMARY"


def add_backup_doi_manager(doi_dict, username):
    """Utility function to add additional doi tool manager (backup).

    :param doi_dict: Dictionary that represents a doi
    :param username: String active directory username
    """
    key = "usersAndTypes[" + username + "]"
    doi_dict[key] = "BACKUP"
