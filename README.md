# noipy - README

A simple command line tool to update No-IP.com hosts IP via [No-IP DDNS Update API](http://www.noip.com/integrate/request).
This script also prints the response massege based on [No-IP DDNS Update API Response Codes](http://www.noip.com/integrate/response/).

## Installation

```sh
$ python setup.py install
```

## Usage

Basic usage of **noipy** command line tool:
```sh
$ noipy --file <properties file path>
```

For details:
```sh
$ noipy --help
```

## Properties File Configuration
Put the auth information and hostname in a `properties` file:

	username=<your username>
	password=<your password>
	hostname=<your hostname on no-ip.com>

Check out the [noipy.properties](noipy.properties) sample file if there is still any doubts.

## Troubleshooting

If you find any errors, please feel free to report them using this project's [issue tracker](https://github.com/povieira/noipy/issues).

## License & Copyright

Copyright (c) 2013 Pablo O Vieira (povieira).  
This software is licensed under the [Eclipse Public License (EPL)](LICENSE.md).


