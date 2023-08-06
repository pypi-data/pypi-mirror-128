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

## Package layout

There's one public class available: `ApiClient`. The ApiClient is a factory that automatically registers various subclasses through a hook using the `__init_subclass__` method.

New subclasses can be added by inheriting `_BaseClient` and adding a resource name. This resource name cannot be similar to resource names used by other subclasses. The resource name dictates how the subclass is available in the public API of ApiClient.

### Example

Take the following example. The class `_Artifact` inherits _BaseClient. The resource_name of the class is 'artifacts', making the methods of the `_Artifact` class publicly available.

```python
class ApiClient:
    resources = {}

    def __init__(self, endpoint, token):
        ...

    def __getattr__(self, name):
        return self.__class__.resources[name](self._endpoint, self._token)

class _BaseClient:
    def __init__(self, endpoint, token):
        ...

    def __init_subclass__(cls, /, resource_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        ApiClient.resources[resource_name] = cls

class _Artifact(_BaseClient, resource_name='artifacts'):
    def example_method(self):
        ...

# we can now call methods of _Artifact like this:

client = ApiClient(credentials)
client.artifacts.example_method()
```



## Contact / maintainers

Jonathan Seib (jonathan.seib@wepublic.nl) is the maintainer of this package.
