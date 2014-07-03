noipy: DDNS update tool
=======================

.. image:: https://badge.fury.io/py/noipy.png
        :target: http://badge.fury.io/py/noipy

.. image:: https://travis-ci.org/povieira/noipy.png?branch=master
        :target: https://travis-ci.org/povieira/noipy

.. image:: https://pypip.in/d/noipy/badge.png
        :target: https://crate.io/packages/noipy

.. image:: https://coveralls.io/repos/povieira/noipy/badge.png?branch=master
        :target: https://coveralls.io/r/povieira/noipy?branch=master

.. image:: https://badge.waffle.io/povieira/noipy.png?label=ready
        :target: http://waffle.io/povieira/noipy

.. image:: https://zenodo.org/badge/4128/povieira/noipy.png
        :target: https://zenodo.org/record/10747

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
            --provider {noip|dyn|duck}


For `DuckDNS provider <https://www.duckdns.org>`_, the command line would look like this:

.. code-block:: bash

    $ noipy -u <your token> -n <your DuckDNS domain> --provider duck


Or you can just use ``--hostname`` (``-n``) and ``--provider`` arguments if you have
previously  stored login information with ``--store`` option.

.. code-block:: bash

    $ noipy --hostname <your hostname on DDNS provider> --provider {noip|dyn| duck}

If ``--provider`` option is not informed, **noip** will be used as provider.

It is also possible to inform an IP address other than the machine's current:

.. code-block:: bash

    $ noipy --hostname <your hostname on DDNS provider> 127.0.0.1


For details:

.. code-block:: bash

    $ noipy --help


Storing auth information
------------------------

With ``--store`` option it is possible to store login information. The
information is sotred in ``$HOME/.noipy/`` directory:

.. code-block:: bash

    $ noipy --store --username <your username> --password <your password> \
        --provider {noip|dyn| duck}

Or simply:

.. code-block:: bash

    $ noipy --store --provider {noip|dyn| duck}

And type username and password when required.

**Note:** password is stored simply encoded with
`Base64 <https://en.wikipedia.org/wiki/Base64>`_ method and is not actually
*encrypted*!


Contributing
------------

Source code
~~~~~~~~~~~

**noipy** source code can be found at GitHub repo: https://github.com/povieira/noipy/

Running tests
~~~~~~~~~~~~~

.. code-block:: bash

    $ python setup.py test


Improvements & Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have suggestions or find any bug, please feel free to report them using this
project's `issue tracker <https://github.com/povieira/noipy/issues>`_.


Copyright & License
-------------------

Copyright (c) 2013 Pablo O Vieira (povieira).
This software is licensed under the
`Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.
