# Contributing

## Testing

Tests are run using tox and/or pytest.

    tox -e py39

or directly:

    pytest


## Code Style

Code conforms to the `black` and PEP8 style guides. Before checking in code, please run the linters:

    black .
    flake8
    mypy diamond_art

These are tested by the 'lint' tox environment:

    tox -e lint


## Making a release

### Setup

- Set up GPG key (for signing the tag)
- `pip install twine`
- Generate API token at TestPyPI and PyPI and add to .pypirc:

    [distutils]
        index-servers=
            pypi
            testpypi
    [pypi]
        username = __token__
        password = pypi-...
    [testpypi]
        repository: https://test.pypi.org/legacy/
        username = __token__
        password = pypi-...

- `chmod 600 ~/.pypirc`


### Release

1. Bump to release version v0.1.0

2. Test

        tox

3. Build

        python setup.py sdist bdist_wheel

4. Run checks

        twine check dist/*
        git verify-tag v0.1.0

5. Push to testing

        twine upload --repository testpypi -s --identity 780796DF dist/*

6. Tag

        git tag -s -a v0.1.0

7. Push!

        git push
        git push --tags
        twine upload -s --identity 780796DF dist/*

8. Bump version number in __init__.py to .dev0

9. Make release on github