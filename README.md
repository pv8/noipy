# noipy - README

[![Build Status](https://travis-ci.org/povieira/noipy.png?branch=master)](https://travis-ci.org/povieira/noipy)

A simple command line tool to update No-IP.com hosts IP via [No-IP DDNS Update API](http://www.noip.com/integrate/request).
This script also prints the response massege based on [No-IP DDNS Update API Response Codes](http://www.noip.com/integrate/response/).

## Installation

```sh
$ python setup.py install
```

## Usage

Basic usage of **noipy** command line tool:
```sh
$ noipy --username <your username> --password <your password> --hostname <your hostname on no-ip.com>
```
Or you can just call **noipy** if you have previously stored login information and hostname with `--store` [option](#store).
```sh
$ noipy
```

For details:
```sh
$ noipy --help
```

## Settings File Configuration
The settings file is a simple key/value pair file containing login information and hostname:

	username=<your username>
	password=<your password>
	hostname=<your hostname on no-ip.com>

With `--store` option it is possible to store login and hostname information in `HOME` directory (`~/.noipy`):
```sh
$ noipy --store
```
**Note:** password will be stored in settings file as plain text.

Check out the [noipy.properties](noipy.properties) sample file if there is still any doubts.

## Troubleshooting

If you find any errors, please feel free to report them using this project's [issue tracker](https://github.com/povieira/noipy/issues).

## Copyright & License

Copyright (c) 2013 Pablo O Vieira (povieira).  
This software is licensed under the [Eclipse Public License (EPL) - v1.0](LICENSE.md).

