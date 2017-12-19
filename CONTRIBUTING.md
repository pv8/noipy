# Contributing

First of all, thanks for contributing! :tada:

If you have any enhancement suggestions or find a bug, please:

1. Open an [issue](https://github.com/pv8/noipy/issues) so we can discuss it first

2. [Fork](https://github.com/pv8/noipy/fork) the project ([GitHub tutorial on Forking Projects ](https://guides.github.com/activities/forking/))

3. Do your magic

4. Please, [PEP8](https://www.python.org/dev/peps/pep-0008/) and [test your](#running-tests) code

5. All good? Make a [pull request](https://github.com/pv8/noipy/pulls)

## Running tests

Install tests dependencies:

```bash
$ pip install -r requirements-dev.txt
```

Test the code against all supported Python versions and check it against **PEP8** with ``tox``:

```bash
$ tox
```

Check **PEP8** only:

```bash
$ tox -e pep8
```
