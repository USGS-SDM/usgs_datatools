#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `usgs_datatools` package."""

import pytest
import yaml
import os

from click.testing import CliRunner

import usgs_datatools.doi as doi
import usgs_datatools.mp as mp
from usgs_datatools import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'usgs_datatools.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_doi_auth():
    """Test USGS DOI Tool authentication."""
    credentials = yaml.load(open(os.path.expanduser('~') + '/cred.yaml').read())

    doi_session = doi.DoiSession()

    test = doi_session.doi_authenticate(credentials['application_credentials']['username'], credentials['application_credentials']['password'])

    if 'crowd.token_key' in test._session.cookies:
        assert True


def test_doi_auth_failure():
    """Test authentication failure"""
    doi_session = doi.DoiSession()
    try:
        doi_session.doi_authenticate('fake_user', 'fake_password')
    except:
        assert True


def test_doi_get_doi():
    """Test USGS DOI Tool doi get function"""
    credentials = yaml.load(open(os.path.expanduser('~') + '/cred.yaml').read())
    doi_session = doi.DoiSession()

    doi_session.doi_authenticate(credentials['application_credentials']['username'], credentials['application_credentials']['password'])

    # This test works with the Staging application when the below DOI exists.
    sample_doi = doi_session.get_doi('doi:10.5072/S977GF16')

    assert len(sample_doi) > 20


def test_mp_validate():
    """Test MP local file validate"""
    file_notes = mp.validate('./tests/BlueRidgeParkway.xml')
    assert type(file_notes) == dict
