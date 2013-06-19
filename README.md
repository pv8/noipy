# noipy - README

[![Build Status](https://travis-ci.org/povieira/noipy.png?branch=master)](https://travis-ci.org/povieira/noipy)

Command line tool to update DDNS hosts IP address via update API. Initially, the tool was designed to update IP address only on No-IP DDNS provider. But now **noipy** has support for the two most popular DDNS providers: [No-IP](http://www.noip.com/integrate/request) and [DynDNS](http://dyn.com/support/developers/api/perform-update/).

## Installation
Installation can be done via `setup.py`:
```sh
$ python setup.py install
```

## Usage

Basic usage of **noipy** command line tool:
```sh
$ noipy --username <your username> --password <your password> --hostname <your hostname on DDNS provider> --provider {noip|dyn}
```
Or you can just use `--hostname` and `--provider` arguments if you have previously stored login information with `--store` option.
```sh
$ noipy --hostname <your hostname on DDNS provider> --provider {noip|dyn}
```

If `--provider` option is not informed, `noip` will be used as provider.

It is also possible to inform an IP address other than the machine's current:
```sh
$ noipy --hostname <your hostname on DDNS provider> 127.0.0.1
```

For details:
```sh
$ noipy --help
```

## Storing auth information
With `--store` option it is possible to store login information. The information is sotred in `$HOME/.noipy/` directory:
```sh
$ noipy --store --username <your username> --password <your password> --provider
```
Or simply:
```sh
$ noipy --store
```
And type username and password when required.

**Note:** password is stored simply encoded with [Base64](https://en.wikipedia.org/wiki/Base64) method and is not actually *encrypted*!

## Improvements & Troubleshooting

If you have suggestions or find any bug, please feel free to report them using this project's [issue tracker](https://github.com/povieira/noipy/issues).

## Copyright & License

Copyright (c) 2013 Pablo O Vieira (povieira).  
This software is licensed under the [Eclipse Public License (EPL) - v1.0](LICENSE.md).

