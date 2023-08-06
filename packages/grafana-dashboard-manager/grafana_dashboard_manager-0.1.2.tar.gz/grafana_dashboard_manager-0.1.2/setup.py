# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafana_dashboard_manager']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.14.0,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['grafana-dashboard-manager = '
                     'grafana_dashboard_manager.__main__:app']}

setup_kwargs = {
    'name': 'grafana-dashboard-manager',
    'version': '0.1.2',
    'description': "A cli utility that uses Grafana's HTTP API to easily save and restore dashboards.",
    'long_description': "# grafana-dashboard-manager\n\n![CodeQL](https://github.com/Beam-Connectivity/grafana-dashboard-manager/actions/workflows/codeql-analysis.yml/badge.svg)\n\n\nA simple cli utility for importing or exporting dashboard json definitions using the Grafana HTTP API.\n\nThis may be useful for:\n\n- Backing up your dashboards that already exist within your Grafana instance, e.g. if you are migrating from the internal sqlite database to MySQL.\n- Updating dashboard files for your Infrastructure-as-Code, for use with Grafana dashboard provisioning.\n- Making tweaks to dashboard JSON files directly and updating Grafana with one command.\n\nNotable features:\n\n- Mirrors the folder structure between a local set of dashboards and Grafana, creating folders where necessary.\n- Ensures links to dashboards folders in a `dashlist` Panel are consistent with the Folder IDs - useful for deploying one set of dashboards across mulitple Grafana instances, e.g. for dev, test, prod environments.\n\n### Workflow\n\nThe intended development process is:\n\n1. Develop existing dashboard, or create a new one and save it in the web UI.\n2. Ensure the dashboard is in the desired folder.\n3. Use `grafana-dashboard-manager` to extract the new dashboards and save them to a local directory.\n4. Dashboards can be created/updated from the local directory back into Grafana.\n\n# Usage\n\n#### Installation\n\nDependencies are managed with poetry.\n\nInstall from pypi:\n\n```bash\n$ poetry run pip install grafana-dashboard-manager\n```\n\nInstall from source\n\n```bash\n$ cd /path/to/grafana-dashboard-manager\n$ poetry install\n```\n\nNote that the admin login user and password are required, and its selected organization is correct.\n\nSee the full help text with `poetry run grafana-dashboard-manager --help`\n\n### Download dashboards from web to solution-data\n\n```bash\npoetry run grafana-dashboard-manager \\\n    --host https://my.grafana.com \\\n    --username admin --password mypassword \\\n    download all \\\n    --destination-dir /path/to/dashboards/\n```\n\n### Upload dashboards from solution-data to web\n\n```bash\npoetry run grafana-dashboard-manager \\\n    --host https://my.grafana.com \\\n    --username admin --password mypassword \\\n    upload all \\\n    --source-dir /path/to/dashboards/\n```\n\nN.B. if your Grafana is not at port 80/443 as indicated by the protocol prefix, the port needs to be specified as part of the `--host` argument, e.g. for a locally hosted instance on port 3000: `--host http://localhost:3000`\n\n## Limitations\n\n- The home dashboard new deployment needs the default home dashboard to be manually set in the web UI, as the API to set the organisation default dashboard seems to be broken, at least on v8.2.3.\n\n- Currently expects a hardcoded 'home.json' dashboard to set as the home.\n\n- Does not handle upload of dashboards more deeply nested than Grafana supports.\n\n- Does not support multi-organization deployments\n",
    'author': 'Vince Chan',
    'author_email': 'vince@beamconnectivity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.beamconnectivity.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
