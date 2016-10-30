.. :changelog:

Changelog
=========

1.5.0 (2016-10-30)
------------------

- Automatic deploy to `PyPI <https://pypi.python.org/pypi>`_ via `Travis CI <https://docs.travis-ci.com/user/deployment/pypi/>`_
- Minor refactorings
- **Dropped support for Python 3.2**

1.4.4 (2016-04-11)
------------------

- Bugfix

1.4.3 (2015-10-15)
------------------

- Included ``User-Agent`` in request Header
- Improvements on plugins test cases
- Changed code coverage service from `Coveralls <https://coveralls.io>`_ to `Codecov <https://codecov.io>`_

1.4.2 (2015-08-22)
------------------

- **Bugfix**: storing auth credentials properly from ``stdin``
- Test case for ``--store`` option getting username/password from ``stdin``

1.4.0 (2015-04-25)
------------------

- Using the awesome `Requests HTTP library <https://github.com/kennethreitz/requests>`_
- Using `tox <http://tox.readthedocs.org/en/latest/>`_ in order to ease test against multiple Python versions

1.3.1 (2014-12-19)
------------------

- Send update to DDNS only if IP address has changed

1.3.0 (2014-12-16)
------------------

- Support for custom DDNS URL via ``--url`` parameter

1.2.3 (2014-10-10)
------------------

- Unit tests improvements and ``PluginsTest`` bug fixes
- Custom config directory feature bug fix (``--config`` argument)

1.2.2 (2014-07-03)
------------------

- PEP8'd code (Closes #5)
- Switched to `Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_
- Unit test improvement
- Minor feature: custom config directory via ``-c`` or ``--config`` argument.

1.2.1 (2014-06-30)
------------------

- Bug fix (execution via command line. issue #5)

1.2.0 (2014-04-21)
------------------

- Support for `DuckDNS domains update <https://www.duckdns.org/install.jsp>`_

1.1.4 (2013-08-29)
------------------

- Test case improvements
- `Coveralls.io <http://coveralls.io/>`_ support

1.1.3 (2013-07-24)
------------------

- Python 3.3 compatibility

1.1.0 (2013-05-15)
------------------

- Support for `DynDNS Update API <http://dyn.com/support/developers/api/>`_ 
- DDNS auth info storage changed

1.0.1 (2013-05-10)
------------------

- Added flexibility to DNS updater with ``abc.ABCMeta``
- Code organization
- Manual settings file removed (auth info can be stored via command line)

0.1.0 (2013-03-22)
------------------

- Conception
