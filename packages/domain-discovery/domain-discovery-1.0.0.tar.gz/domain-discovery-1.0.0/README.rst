.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: domain-discovery-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/domain-discovery.svg
    :alt: domain-discovery-py release
    :target: https://pypi.org/project/domain-discovery

.. image:: https://github.com/whois-api-llc/domain-discovery-py/workflows/Build/badge.svg
    :alt: domain-discovery-py build
    :target: https://github.com/whois-api-llc/domain-discovery-py/actions

========
Overview
========

The client library for
`Domains & Subdomains Discovery API <https://domains-subdomains-discovery.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============

.. code-block:: shell

    pip install domain-discovery

Examples
========

Full API documentation available `here <https://domains-subdomains-discovery.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

.. code-block:: python

    from domaindiscovery import *

    client = Client('Your API key')

Domains
-------------------

.. code-block:: python

    terms = {
        'include': ['example.*']
    }

    # Get the list of domains (up to 10,000)
    result = client.get(domains=terms)

    # Total count
    print(result.domains_count)

Subdomains
-------------------

.. code-block:: python

    domain_terms = {
        'include': ['blog.*'],
        'exclude': ['*.com']
    }
    subdomain_terms = {
        'include': ['*news*']
    }

    # Search for subdomains
    result = client.get(subdomains=subdomain_terms)

    # Search in subdomains of the required domain names
    result = client.get(
        domains=domain_terms,
        subdomains=subdomain_terms)

Extras
-------------------

.. code-block:: python

    import datetime

    terms = {
        'include': ['blog.*'],
        'exclude': ['*.com']
    }
    since_date = datetime.date(2021, 8, 12)

    # Get raw response in XML and filter by date
    raw_result = client.get_raw(
        domains=terms,
        output_format=Client.XML_FORMAT,
        since_date=since_date)

Response model overview
-----------------------

.. code-block:: python

    Response:
        - domains_count: int
        - domains_list: [str]

