
[![Travis CI status](https://travis-ci.org/davidread/ckanext-hierarchy.svg?branch=master)](https://travis-ci.org/davidread/ckanext-hierarchy)

[![Latest version on pypi](https://img.shields.io/pypi/v/ckanext-hierarchy.svg)](https://pypi.org/project/ckanext-hierarchy/)

[![License](https://img.shields.io/pypi/l/ckanext-hierarchy.svg)](https://pypi.org/project/ckanext-hierarchy/)


# ckanext-hierarchy - Organization hierarchy for CKAN

Organizations can be arranged into a tree hierarchy.

This new hierarchical arrangement of organizations is displayed
using templates in this extension, instead of the usual list:
![Screenshot of organizations page](screenshots/orgs_page.png)

Provides a new field on the organization edit form to select a parent
organization:
![Screenshot of organization edit page](screenshots/org_edit.png)

When viewing an organization you see its context within the tree in the side bar. In addition you can widen search of the organization's datasets to include datasets in sub-organizations too:
![Screenshot of organization page](screenshots/org_page.png)

## Technical details

Templates:
* /organization - now shows the organization hierarchy instead of list
* /organization/about/{id} - now also shows the relevant part of the hierarchy

Snippets (used by hierarchy and ckanext-scheming):
* /scheming/form_snippets/org_hierarchy.html

In order to make hierarchy work with ckanext-scheming you need to enable
hierarchy and then use corresponding form_snippet in your org_schema.
For example, you may add next field:
```
{
    "field_name": "not_used",
    "label": "Parent organization",
    "display_snippet": null,
    "form_snippet": "org_hierarchy.html",
    "validators": "ignore_missing"
}
```

Optionally one could also specify a full name and leave the field 'title' for
the short name or acronym (more convenient for  display).
```
{
    "field_name": "longname",
    "label": "Full Name",
    "validators": "ignore_missing unicode",
    "form_snippet": "large_text.html",
    "form_attrs": {"data-module": "slug-preview-target"},
    "form_placeholder": "My Organization full name",
    "display_snippet": null
}
```

TODO:
* make the trees prettier with JSTree

## Requirements

This extension requires CKAN v2.8 or later.

## Installation

To install ckanext-hierarchy:

1. Activate your CKAN virtual environment, for example:

       . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-hierarchy Python package into your virtual environment:

       cd /usr/lib/ckan/default/src
       pip install -e "git+https://github.com/davidread/ckanext-hierarchy.git#egg=ckanext-hierarchy"
       pip install -r ckanext-hierarchy/requirements.txt

3. Add ``hierarchy`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

        sudo service apache2 reload

## Config settings

None at present

## Tests

To run the tests, do::

    pytest --ckan-ini=test.ini ckanext/hierarchy/tests

## Licence and copyright

This module is openly licensed with AGPLv3 - see LICENSE file.

Copyright belongs to commit authors. Commits 2013-2017 by @davidread are Crown Copyright.
