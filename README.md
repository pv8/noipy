<!-- 
SPDX-FileCopyrightText: 2013 Pablo V <noipy@pv8.dev>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# noipy: DDNS update tool

[![CI](https://github.com/pv8/noipy/actions/workflows/ci.yml/badge.svg)](https://github.com/pv8/noipy/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/noipy.svg)](https://pypi.python.org/pypi/noipy/)
[![Python versions](https://img.shields.io/pypi/pyversions/noipy.svg)](https://pypi.python.org/pypi/noipy)
[![codecov](https://codecov.io/gh/pv8/noipy/branch/main/graph/badge.svg)](https://codecov.io/gh/pv8/noipy)
[![Snap Status](https://snapcraft.io/noipy/badge.svg)](https://snapcraft.io/noipy)
[![Snap Trending](https://snapcraft.io/noipy/trending.svg?name=0)](https://snapcraft.io/noipy)

Command line tool to update DDNS hosts IP address via update API. Initially
the tool was designed to update IP address only on No-IP DDNS provider. But
now **noipy** has support for the following DDNS providers:

- [No-IP](http://www.noip.com/integrate/request)
- [DuckDNS](https://www.duckdns.org/install.jsp)
- [DynDNS](http://dyn.com/support/developers/api/perform-update/)

## Installation

Install with [pip](https://pip.pypa.io/en/stable/):

```bash
$ pip install noipy
```

Or with [Snappy](https://en.wikipedia.org/wiki/Snappy_(package_manager)) on [supported distros](https://docs.snapcraft.io/core/install#support-overview):

```bash
$ sudo snap install noipy
```

**Note**: **noipy** will also install the [Requests HTTP library](https://github.com/kennethreitz/requests).

## Usage

Basic usage of **noipy** command line tool:

```bash
$ noipy -u <your username> -p <your password> -n <your hostname on DDNS provider> \
        --provider {generic|noip|dyn|duck}
```

For [DuckDNS provider](https://www.duckdns.org), the command line would look like this:

```bash
$ noipy -u <your token> -n <your DuckDNS domain> --provider duck
```

Or you can just use `--hostname` (`-n`) and `--provider` arguments if you have
previously [stored your auth information](#storing-auth-information) with `--store` option.

```bash
$ noipy --hostname <your hostname on DDNS provider> --provider {generic|noip|dyn|duck}
```

You can also specify a custom DDNS URL (thanks to [@jayennis22](https://github.com/jayennis22)):

```bash
$ noipy --hostname <your hostname on DDNS provider> [--provider generic] \
        --url <custom DDNS URL>
```

It is also possible to inform an IP address other than the machine's current:

```bash
$ noipy --hostname <your hostname on DDNS provider> 127.0.0.1
```

If `--provider` option is not informed, **generic** will be used as provider.

For details:

```bash
$ noipy --help
```

## Storing auth information

With `--store` option it is possible to store login information. The
information is stored in `$HOME/.noipy/` directory:

```bash
$ noipy --store --username <your username> --password <your password> \
    --provider {generic|noip|dyn|duck}
```

Or simply:

```bash
$ noipy --store --provider {generic|noip|dyn|duck}
```

And type username and password when required.

**Note:** password is stored simply encoded with
[Base64](https://en.wikipedia.org/wiki/Base64) method and is not actually
*encrypted*!

### Running tests

#### Using uv (recommended)

```bash
# Install uv (if not already installed)
$ pipx install uv
# Or see https://docs.astral.sh/uv/getting-started/installation/

# Sync test dependencies
$ uv sync --extra tests

# Run tests with tox
$ uv run tox
```

#### Using pip

Install test dependencies and run tests:

```bash
$ pip install -e ".[tests]"
$ tox
```

### Linting

#### Using uv (recommended)

```bash
# Sync linting dependencies
$ uv sync --extra lint

# Run linting with tox
$ uv run tox -e lint
```

#### Using pip

Install linting dependencies and check code style:

```bash
$ pip install -e ".[lint]"
$ tox -e lint
```

### Type checking

**noipy** uses type hints to improve code quality and maintainability.

#### Using uv (recommended)

```bash
# Sync type checking dependencies
$ uv sync --extra typing

# Run type checking with mypy
$ uv run mypy noipy/
```

#### Using pip

Install type checking dependencies and run mypy:

```bash
$ pip install -e ".[typing]"
$ mypy noipy/
```

## License

[![License](https://img.shields.io/github/license/pv8/noipy.svg)](LICENSE)
