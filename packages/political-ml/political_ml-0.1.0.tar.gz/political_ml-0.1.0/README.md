# API wrapper for the Political ML API

## About Political ML

Political ML is a set of API that can perform multiple NLP related tasks. Currently two things are supported: extracting
entities and categorising texts. These currently only work for Dutch texts. Political ML is developed
by [Wepublic](https://wepublic.nl). It only has a private API available, that's not meant for public use.

### How to use

```python
from political_ml import ApiClient

client = ApiClient(token, endpoint)
texts = [
    {
        "id": 1,
        "text": "Mark Rutte eet wel bitterballen."
    },
    {
        "id": 2,
        "text": "Jesse Klaver eet geen bitterballen."
    }
]
entities = client.ner(texts)
print(entities)

"""
[
  {
    "entities": [
      {
        "end": 10,
        "entity": "Mark Rutte",
        "start": 0,
        "type": "PERSON"
      }
    ],
    "id": 1,
    "model": {
      "version": "v1"
    }
  },
  {
    "entities": [
      {
        "end": 12,
        "entity": "Jesse Klaver",
        "start": 0,
        "type": "PERSON"
      }
    ],
    "id": 2,
    "model": {
      "version": "v1"
    }
  }
]
"""
```

## For development

### Requirements

- Python 3.8+
- Make

### Setup for development

- Create a virtual env: `python -m virtualenv venv`
- Install development dependencies: `python -m pip install -e ".[dev]"`
- Run `make unit-test` to run unit tests or run `tox` to run unit tests for all support python versions.
- If you have an instance of the API's available, you can run integration tests with `make integration-test`.

New PRs are opened against `develop`.

### Publishing a new version

1. Bump version numbers in [__meta__.py](/src/source_aggregation/__meta__.py)
2. Update [CHANGELOG.md](/CHANGELOG.md).
3. Publish a [new release](https://github.com/wepublic-nl/sas-package/releases/new) and create a git tag equal to the version number set in step 1.

A Github Action workflow takes care of building and publishing to [PyPi](https://pypi.org/project/source-aggregation/#description).

## Contact / maintainers

Jonathan (stakeholderintel@wepublic.nl) is the maintainer of this package.
