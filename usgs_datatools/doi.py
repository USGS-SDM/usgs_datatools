# -*- coding: utf-8 -*-

"""
usgs_datatools.doi
------------------

This python module provides a user session and additional functionality for
the USGS Digitial Object Identifier creation tool.
"""
import requests
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

        :param env: (optional) string, the default is staging where test
            dois can be created.
        """
        if env == "production":
            self._base_doi_url = "https://www1.usgs.gov/csas/dmapi/"
        elif env == "dev":
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

        :param username: string
            current USGS username (Active Directory).
        :param password: string
            current USGS user password (Acitve Directory).
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

        :param doi: string
            Digital object identifier.
            Example: ('doi:10.5066/F7SB43S8')

        :returns: dictionary
            DOI fields as a dictionary.

        >>> doi.get_doi('doi:10.5072/S977GF16')
            {'doi': 'doi:10.5072/S977GF16',
            'title': '2018-09-26T14:36:08.806Z: Update / Public / Clear Optional Fields',
            'pubDate': '2001',
            'url':'https://data.usgs.gov/datacatalog/doi-messages/permanent.html',
            'resourceType': 'Documentation',
            'date': '',
            'dateType': '',
            'description': '',
            'subject': '',
            'username': 'newman@usgs.gov',
            'status': 'public',
            'noDataReleaseAvailableReason': None,
            'noPublicationIdAvailable': False,
            'dataSourceId': 17260,
            'dataSourceName': 'Midwest Region',
            'linkCheckingStatus': None,
            'formatTypes': [],
            'authors': [{'authorName': 'Wright, Justin J.', 'orcId': '1111-1111-1111-111X', 'nameType': 'Personal', 'position': 1}, {'authorName': 'U.S. Forest Service', 'orcId': None, 'nameType': 'Organizational', 'position': 0}],
            'users': ['newman@usgs.gov', 'sciencebase@ornl.gov', 'ome_service_account@usgs.gov'],
            'relatedIdentifiers': [{'relatedIdentifier': 'https://doi.org/10.5072/N91WBCT8', 'dataciteRelationType': 'IS_CITED_BY','usgsRelationSubType': 'PUBLICATION'}, {'relatedIdentifier': 'https://doi.org/10.5072/N76DHdgdgd', 'dataciteRelationType': 'IS_SUPPLEMENT_TO', 'usgsRelationSubType': None}], 
            'ipdsNumbers': [{'ipdsNumber': '12345', 'ipdsType': 'DATA_RELEASE'}, {'ipdsNumber': '12345678', 'ipdsType': 'PUBLICATION'}],
            'created': '2018-09-26',
            'modified': '2018-09-26'}
        """
        response_status = self._session.get(
            self._base_doi_url + "doi/" + doi
        )

        if response_status.status_code == 200:
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
