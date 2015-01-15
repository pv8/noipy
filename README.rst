noipy: DDNS update tool
=======================

.. image:: https://pypip.in/version/noipy/badge.svg?style=flat
        :target: https://pypi.python.org/pypi/noipy/

.. image:: https://pypip.in/download/noipy/badge.svg?style=flat
        :target: https://pypi.python.org/pypi/noipy/

.. image:: https://travis-ci.org/povieira/noipy.svg?branch=master
        :target: https://travis-ci.org/povieira/noipy

.. image:: https://img.shields.io/coveralls/povieira/noipy.svg?style=flat&branch=master
        :target: https://coveralls.io/r/povieira/noipy?branch=master

.. image:: https://landscape.io/github/povieira/noipy/master/landscape.svg?style=flat
        :target: https://landscape.io/github/povieira/noipy/master
        :alt: Code Health

.. image:: https://zenodo.org/badge/doi/10.5281/zenodo.13320.png
        :target: http://dx.doi.org/10.5281/zenodo.13320

Command line tool to update DDNS hosts IP address via update API. Initially
the tool was designed to update IP address only on No-IP DDNS provider. But
now **noipy** has support for the following DDNS providers:

- `No-IP <http://www.noip.com/integrate/request>`_
- `DuckDNS <https://www.duckdns.org/install.jsp>`_
- `DynDNS <http://dyn.com/support/developers/api/perform-update/>`_


Installation
------------

To install **noipy**, simply:

.. code-block:: bash

    $ pip install noipy


Usage
-----

Basic usage of **noipy** command line tool:

.. code-block:: bash

    $ noipy -u <your username> -p <your password> -n <your hostname on DDNS provider>
            --provider {generic|noip|dyn|duck}


For `DuckDNS provider <https://www.duckdns.org>`_, the command line would look like this:

.. code-block:: bash

    $ noipy -u <your token> -n <your DuckDNS domain> --provider duck


Or you can just use ``--hostname`` (``-n``) and ``--provider`` arguments if you have
previously  stored login information with ``--store`` option.

.. code-block:: bash

    $ noipy --hostname <your hostname on DDNS provider> --provider {generic|noip|dyn| duck}


You can also specify a custom DDNS URL (thanks to `@jayennis22 <https://github.com/jayennis22>`_):

.. code-block:: bash

    $ noipy --hostname <your hostname on DDNS provider> [--provider  generic]
            --url <custom DDNS URL>


It is also possible to inform an IP address other than the machine's current:

.. code-block:: bash

    $ noipy --hostname <your hostname on DDNS provider> 127.0.0.1


If ``--provider`` option is not informed, **generic** will be used as provider.


For details:

.. code-block:: bash

    $ noipy --help


Storing auth information
------------------------

With ``--store`` option it is possible to store login information. The
information is sotred in ``$HOME/.noipy/`` directory:

.. code-block:: bash

    $ noipy --store --username <your username> --password <your password> \
        --provider {generic|noip|dyn| duck}

Or simply:

.. code-block:: bash

    $ noipy --store --provider {generic|noip|dyn| duck}

And type username and password when required.

**Note:** password is stored simply encoded with
`Base64 <https://en.wikipedia.org/wiki/Base64>`_ method and is not actually
*encrypted*!


Contributing
------------

Improvements & Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have any enhancement suggestions or find a bug, please:

#. Open an `issue <https://github.com/povieira/noipy/issues>`_
#. `Fork <https://github.com/povieira/noipy/fork>`_ the project
#. Do your magic (+ `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ + test)
#. Is everything working? Send a `pull request <https://github.com/povieira/noipy/pulls>`_

Running tests
~~~~~~~~~~~~~

.. code-block:: bash

    $ python setup.py test


Copyright & License
-------------------

.. image:: https://pypip.in/license/noipy/badge.svg?style=flat
        :target: https://pypi.python.org/pypi/noipy/
        :alt: License

Copyright (c) 2013 Pablo O Vieira (povieira).
