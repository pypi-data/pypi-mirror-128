# API wrapper for the Source Aggregation Service (Python)

## Requirements

- Python 3.8+
- Make

## Setup for development

- Create a virtual env: `python -m virtualenv venv`
- Install development dependencies: `python -m pip install -e ".[dev]"`
- Run `make unit-test` to run unit tests or run `tox` to run unit tests for all support python versions.
- If you have an instance of the Source Aggregation Service available, you can run integration tests with `make integration-test`.

New PRs are opened against `develop`. We merge to `main` when we want to publish a new version.

## Publishing a new version

1. Bump version numbers in setup.py
2. Run `make publish` and authenticate with our PyPi credentials.
3. We only publish new versions from the `main` branch. We use git tags for new releases.

## About the SAS

The SAS, short for Source Aggregation Service, is a system developed by [Wepublic](https://wepublic.nl). It only has a private API available, that's not meant for public use.

### How to use

Take the following example. In this example we want to get a list of artifacts:

```python
from source_aggregation import ApiClient

ENDPOINT = 'https://sas.publicaffairs.dev'
TOKEN = 'jwt-token'
client = ApiClient(ENDPOINT, ENDPOINT)
artifacts = client.artifacts.list()
print(artifacts)
```

## Contact / maintainers

Jonathan (stakeholderintel@wepublic.nl) is the maintainer of this package.
