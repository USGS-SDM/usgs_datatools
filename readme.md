# USGS Data Tools

An in-progress python package to assist with data management best practices. This package is more tailored for internal functionality however it would be great to include more capabilities for general data management processes. 

##### USGS Digital Object Identifer Tool (internal)

✅ Create DOI

✅ Get a DOI

✅ Update a DOI

##### Datacite 

✅ Query DOI 

##### Metadata Parser 

✅ Validate local XML file

### Quick Start

Install python requirements

```
pip install -r requirements.txt
```

Git Install 

```
pip install -e git+https://github.com/bserna-usgs/usgs_datatools.git@c4cae0459ba61dc7a9a606827e781fdbde8abf1a#egg=usgs_datatools
```

Or install usgs_datatools (locally)

```
# Clone or download this packagage and change directory into the top level
pip install .
```

### Examples

Please see the examples/notebook directory for a sample of DOI Tool usage (querying, creating, modifying).

Datacite queries can be ran using the new ```doi.datacite_search(10.5066/xxxxx)``` method.

### Contributions

All kinds of contibutions are greatly appreicated, please see the ```CONTRIBUTING.rst``` file for more information [link](https://github.com/bserna-usgs/usgs_datatools/blob/master/CONTRIBUTING.rst)


### Testing

Testing is setup using pytest and can be started using the command below.

```sh
python -m pytest tests/
```

### Development

Update versions

```sh
# preferred and w/o commit 
bumpversion minor

# old
bumpversion  --current-version 0.2.0 minor --allow-dirty
```


### Credits

Python, Requests, BeautifulSoup, PyYaml, Cookiecutter: [cookiecutter](https://github.com/audreyr/cookiecutter), audreyr/cookiecutter-pypackage: [link](https://github.com/audreyr/cookiecutter-pypackage), PyTest

<hr>

### Provisional Software Disclaimer Under USGS Software Release Policy, the software codes here are considered preliminary, not released officially, and posted to this repo for informal sharing among colleagues.

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.
