[![Run Test][gh-run-t-shield]][gh-run-t-url]
[![Package Test][gh-pkg-t-shield]][gh-pkg-t-url]
[![Code Quality][lgtm-shield]][lgtm-url]
[![PyPI Downloads][pypi-shield]][pypi-url]
[![GitHub tag][tag-shield]][tag-url]

[gh-run-t-shield]: https://img.shields.io/github/workflow/status/vrelease/vrelease-py/run-test?label=run%20test&logo=github&style=flat-square
[gh-run-t-url]: https://github.com/vrelease/vrelease-py/actions/workflows/run-test.yml

[gh-pkg-t-shield]: https://img.shields.io/github/workflow/status/vrelease/vrelease-py/pkg-test?label=package%20test&logo=github&style=flat-square
[gh-pkg-t-url]: https://github.com/vrelease/vrelease-py/actions/workflows/pkg-test.yml

[lgtm-shield]: https://img.shields.io/lgtm/grade/python/g/vrelease/vrelease-py.svg?logo=lgtm&style=flat-square
[lgtm-url]: https://lgtm.com/projects/g/vrelease/vrelease-py/context:python

[pypi-shield]: https://img.shields.io/pypi/dm/vrelease-bin?logo=python&logoColor=fff&style=flat-square
[pypi-url]: https://pypi.org/project/vrelease-bin

[tag-shield]: https://img.shields.io/github/tag/vrelease/vrelease-py.svg?logo=git&logoColor=FFF&style=flat-square
[tag-url]: https://github.com/vrelease/vrelease-py/releases


# `vrelease-py-wrapper`

<img src="icon.svg" height="240px" align="right"/>

Python wrapper for [`vrelease`][vrelease]. Install with pipenv:

```sh
pipenv install --dev vrelease-bin
```

Or pip:

```sh
pip install vrelease-bin
```

[vrelease]: https://github.com/vrelease/vrelease


## How can I use it?

For instructions on how to use `vrelease`, [see this](https://github.com/vrelease/vrelease#how-can-i-use-it).

### Global install

```sh
pip install vrelease-bin
```

Sudo privileges might be needed. After that, `vrelease` will be available at
`PATH`. Simply:

```sh
vrelease -h
```

### Per project basis

When installing on a single project, add a script to your `Pipfile`:

```toml
[scripts]
"vrelease:help" = "vrelease -h"
```

And run like any pipenv script:

```sh
pipenv run vrelease:help
```


## License

To the extent possible under law, [Caian Ertl][me] has waived __all copyright
and related or neighboring rights to this work__. In the spirit of _freedom of
information_, I encourage you to fork, modify, change, share, or do whatever
you like with this project! `^C ^V`

[![License][cc-shield]][cc-url]

[me]: https://github.com/upsetbit
[cc-shield]: https://forthebadge.com/images/badges/cc-0.svg
[cc-url]: http://creativecommons.org/publicdomain/zero/1.0
