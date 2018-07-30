USGS Data Tools
======================================

A python package to assist with data management best practices.

USGS Digital Object Identifer Tool (internal tool)

This module supports a python wrapper ontop of the usgs doi tool. 

✅ User sessions

✅ Creating digital object identifiers

✅ Update digital object identifiers

✅ Query the tool

Datacite

Convienience function to query a DOI that's in DataCite to return attributes.

✅ Query DOI 

Metadata Parser

✅ Validate local files (XML)

=================
Quick Start
=================

:: 

    from usgs_datatools import doi

    doi_session = doi.DoiSession()
    doi_session.doi_authenticate("someperson@usgs.gov", "somepassword")

    # Get DOI
    my_doi = doi_session.get_doi("doi:10.5066/xxxx")

    # Create DOI
    doi_session.doi_create({'title': 'USGS Datatools Test Creation',
                            'datasource_id': '17501', 
                        'status': 'reserved'})  

``pip install -e git+https://github.com/bserna-usgs/usgs_datatools.git@latest``

Install python requirements

``pip install -r requirements.txt``

Install usgs_datatools (locally for now)

Clone or download this package and change directory into the top level

``pip install .``

=================
Examples
=================

Please see the examples/notebook directory for a sample of DOI Tool usage (querying, creating, modifying).

Datacite queries can be ran using the new ``doi.datacite_search(10.5066/xxxxx)`` method.

=================
Contributions
=================

All kinds of contributions are greatly appreciated, please see the CONTRIBUTING.rst file for more information link

=================
Testing
=================

Testing is setup using pytest and can be started using the command below.

``python -m pytest tests/``

=================
Development
=================

Update versions

``bumpversion  --current-version 0.2.0 minor --allow-dirty``

=================
Credits
=================

Python, Requests, BeautifulSoup, PyYaml, Cookiecutter: cookiecutter, audreyr/cookiecutter-pypackage, PyTest

=================
Disclaimer
=================

Provisional Software Disclaimer Under USGS Software Release Policy, the software codes here are considered preliminary, not released officially, and posted to this repo for informal sharing among colleagues.

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

=================
Contents:
=================

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   modules
   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
