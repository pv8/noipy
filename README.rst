noipy: DDNS update tool
=======================


.. image:: https://img.shields.io/pypi/v/noipy.svg
        :target: https://pypi.python.org/pypi/noipy/

.. image:: https://img.shields.io/pypi/pyversions/noipy.svg
        :target: https://pypi.python.org/pypi/noipy

.. image:: https://build.snapcraft.io/badge/pv8/noipy.svg
        :target: https://build.snapcraft.io/user/pv8/noipy
        :alt: Snap Status

.. image:: https://api.travis-ci.org/pv8/noipy.svg?branch=master
        :target: https://travis-ci.org/pv8/noipy

.. image:: https://codecov.io/gh/pv8/noipy/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/pv8/noipy

.. image:: https://landscape.io/github/pv8/noipy/master/landscape.svg
        :target: https://landscape.io/github/pv8/noipy/master
        :alt: Code Health

.. image:: https://api.codeclimate.com/v1/badges/1f700be0ea796c8a49e9/maintainability
        :target: https://codeclimate.com/github/pv8/noipy/maintainability
        :alt: Maintainability

.. image:: https://zenodo.org/badge/doi/10.5281/zenodo.29017.svg?style=flat-square
        :target: http://dx.doi.org/10.5281/zenodo.29017

Command line tool to update DDNS hosts IP address via update API. Initially
the tool was designed to update IP address only on No-IP DDNS provider. But
now **noipy** has support for the following DDNS providers:

- `No-IP <http://www.noip.com/integrate/request>`_
- `DuckDNS <https://www.duckdns.org/install.jsp>`_
- `DynDNS <http://dyn.com/support/developers/api/perform-update/>`_


Installation
------------

Install with `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: bash

    $ pip install noipy

Or with `Snappy <https://en.wikipedia.org/wiki/Snappy_(package_manager)>`_ on `supported distros <https://docs.snapcraft.io/core/install#support-overview>`_:

.. code-block:: bash

    $ sudo snap install noipy

**Note**: **noipy** will also install the `Requests HTTP library <https://github.com/kennethreitz/requests>`_.


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
previously `stored your auth information <#storing-auth-information>`_ with ``--store`` option.

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

Running tests
~~~~~~~~~~~~~

Install tests dependencies (`tox <http://tox.readthedocs.org/en/latest/>`_
and `flake8 <https://flake8.readthedocs.org/>`_):

.. code-block:: bash

    $ pip install -r requirements_dev.txt


Test the code against all supported Python versions and check it against **PEP8** with ``tox``:

.. code-block:: bash

    $ tox

Check **PEP8** only:

.. code-block:: bash

    $ tox -e pep8


Copyright & License
-------------------

.. image:: https://img.shields.io/github/license/pv8/noipy.svg?style=flat-square
        :target: LICENSE
        :alt: License

Copyright (c) 2013 Pablo Vieira (pv8).
