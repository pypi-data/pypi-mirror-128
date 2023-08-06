# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_pahrametahrize']
install_requires = \
['pytest>=6.0,<7.0']

entry_points = \
{'pytest11': ['pytest-pahrametahrize = pytest_pahrametahrize']}

setup_kwargs = {
    'name': 'pytest-pahrametahrize',
    'version': '1.0.0',
    'description': 'Parametrize your tests with a Boston accent.',
    'long_description': '# pytest-pahrametahrize\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/pytest-pahrametahrize/main.svg)](https://results.pre-commit.ci/latest/github/sco1/pytest-pahrametahrize/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/sco1/pytest-pahrametahrize)\n\nParametrize your tests with a Boston accent!\n\n### Examples\n```py\nimport pytest\n\nTRUTHINESS_TEST_CASES = [\n    (None, False),\n    (False, False),\n]\n\n\n@pytest.mark.parametrize(("in_val", "truth_out"), TRUTHINESS_TEST_CASES)\ndef test_pahrametahrize(in_val, truth_out):\n    assert bool(in_val) == truth_out\n```\n\n\nbecomes: \n```py\nimport pytest\n\nTRUTHINESS_TEST_CASES = [\n    (None, False),\n    (False, False),\n]\n\n\n@pytest.pahrametahrize(("in_val", "truth_out"), TRUTHINESS_TEST_CASES)\ndef test_pahrametahrize(in_val, truth_out):\n    assert bool(in_val) == truth_out\n```\n\nWicked pissah.\n',
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sco1/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
