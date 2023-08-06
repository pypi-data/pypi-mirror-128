# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafana_dashboard_manager']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'pylint>=2.12.1,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.14.0,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['grafana-dashboard-manager = '
                     'grafana_dashboard_manager.__main__:app']}

setup_kwargs = {
    'name': 'grafana-dashboard-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vince Chan',
    'author_email': 'vince@beamconnectivity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
