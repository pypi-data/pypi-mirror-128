OARepo DOI Generator
====================
[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Instalation
----------
```bash
    pip install oarepo-doi-generator
```

Usage
----------
OARepo module for DataCite DOI registration. 

Functions
---------
###### doi_request(record)
 Creates a new identifier in record metadata with empty ```value```, ```scheme``` as ```doi``` and with ```status``` set as ```requested```.
###### doi_approved(record, pid_type)
 For DOI registration. A new DOI is registered on DataCite and attached to record metadata as a new identifier.
If test_mode sets on True, the registration is performed only on DataCite testing server.

Configuration
-------------
#### must be present in config:
###### DOI_DATACITE_USERNAME
 Repository account credentials for DataCite in the format "xxx.yyy"
###### DOI_DATACITE_PASSWORD
 Password for DataCite
###### DOI_DATACITE_PREFIX
 Registered DOI prefix
###### DOI_TEST_MODE
 If true, dois will be generated only on test server


#### optional:
###### DOI_DATACITE_PUBLISHER
 For metadata that are generated for record and associated with registered DOI.
  If publisher is specified in record metadata, this variable is not used.
  Default value: CESNET
###### DOI_DATACITE_TEST_URL
 Only for test purposes.
  URL that is allowed in the domains settings of the test repository.

 [image]: https://img.shields.io/travis/oarepo/oarepo-doi-genrator.svg
  [1]: https://travis-ci.com/github/oarepo/oarepo-doi-genrator
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-doi-genrator.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-doi-genrator
  [4]: https://img.shields.io/github/license/oarepo/oarepo-doi-genrator.svg
  [5]: https://github.com/oarepo/oarepo-doi-genrator/blob/master/LICENSE
  [6]: https://img.shields.io/pypi/v/oarepo-doi-genrator.svg
  [7]: https://pypi.org/pypi/oarepo-doi-generator