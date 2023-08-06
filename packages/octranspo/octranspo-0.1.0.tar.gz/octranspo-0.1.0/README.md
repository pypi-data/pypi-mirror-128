# OC Transpo API Wrapper [![Build Badge]](https://gitlab.com/MysteryBlokHed/oc-transpo-api/-/pipelines) [![Docs Badge]](https://octranspo.readthedocs.io/en/latest/) [![License Badge]](#license)

A Python wrapper around the OC Transpo API.

## Getting Started

Help to get started is available in [the docs](https://octranspo.readthedocs.io/en/latest/getting_started.html).

## Installation

To install, clone the repository and run:

```sh
python setup.py install
```

<!---------- Uncomment this when package is added to PyPI ---------->
<!--
The best way to install is with pip:

```sh
  pip install octranspo
  # or
  python -m pip install octranspo
```
-->

## Building Docs

To build docs, install the requirements:

```sh
pip install -r docs/requirements.txt
```

Then move to the docs directory and run the build script:

```sh
cd docs

# windows
make.bat html
# *nix
make html
```

## License

This project is licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
  <http://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or
  <http://opensource.org/licenses/MIT>)

at your option.

[build badge]: https://img.shields.io/gitlab/pipeline-status/MysteryBlokHed/oc-transpo-api
[docs badge]: https://img.shields.io/readthedocs/octranspo
[python version badge]: https://img.shields.io/pypi/pyversions/octranspo
[license badge]: https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-green
