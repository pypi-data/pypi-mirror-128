# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jobsbundle', 'jobsbundle.job']

package_data = \
{'': ['*'], 'jobsbundle': ['_config/*']}

install_requires = \
['console-bundle>=0.5,<0.6',
 'databricks-cli>=0.16.0',
 'pyfony-bundles>=0.4.0,<0.5.0',
 'python-box>=3.4,<4.0']

entry_points = \
{'pyfony.bundle': ['create = jobsbundle.JobsBundle:JobsBundle']}

setup_kwargs = {
    'name': 'jobs-bundle',
    'version': '0.4.0.dev2',
    'description': 'Databricks jobs management bundle for the Daipe Framework',
    'long_description': '# Databricks jobs bundle\n\nCreate Databricks jobs from YAML templates.\n\nProvides console commands to automate jobs creation, deletion, ...\n\n## Installation\n\nInstall the bundle via Poetry:\n\n```\n$ poetry add jobs-bundle\n```\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/jobs-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
