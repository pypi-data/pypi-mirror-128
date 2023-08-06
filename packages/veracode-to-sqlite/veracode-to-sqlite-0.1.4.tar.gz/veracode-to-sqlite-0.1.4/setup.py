# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['veracode_to_sqlite']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['veracode-to-sqlite = veracode_to_sqlite.__main__:main']}

setup_kwargs = {
    'name': 'veracode-to-sqlite',
    'version': '0.1.4',
    'description': 'Create a SQLite database from a Veracode results file.',
    'long_description': "# veracode-to-sqlite\n\nThis is a command-line tool that creates a SQLite database from the JSON results\nfile of a Veracode scan.\n\nVeracode scans can produce dozens or hundreds of issues that need to be\nreviewed. In some settings there's good UI for triaging these issues. In other\ncases (such as when running a [pipeline scan]) the results are presented as a\nraw JSON file, and must be triaged by hand.\n\n[pipeline scan]: https://docs.veracode.com/r/t_run_pipeline_scan\n\nThis tool converts the results from JSON into a SQLite database, which can then\nbe consumed by a tool like [datasette] for further analysis.\n\n[datasette]: https://datasette.io/\n",
    'author': 'Nathaniel Knight',
    'author_email': 'nathaniel.ep@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
