# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_workspace',
 'poetry_workspace.commands',
 'poetry_workspace.commands.workspace',
 'poetry_workspace.schemas',
 'poetry_workspace.vcs']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-workspace-plugin = '
                               'poetry_workspace.plugin:WorkspacePlugin']}

setup_kwargs = {
    'name': 'poetry-workspace-plugin',
    'version': '0.4.2',
    'description': 'Multi project workspace plugin for Poetry',
    'long_description': '# Poetry Workspace Plugin\n\nThis experimental tool is a [Poetry Plugin](https://python-poetry.org/docs/master/plugins) to support workflows in a multi-project repository.\n\n## Installation\n\nMake sure you are using at least Poetry 1.2.0a2. To install this preview release, run:\n\n```shell\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - --preview\n```\n\nInstall this plugin:\n\n```shell\npoetry plugin add poetry-workspace-plugin\n```\n\n## Workspace\n\nA workspace is a collection of Poetry projects that share a single environment.\n',
    'author': 'Martin Liu',
    'author_email': 'martin.xs.liu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
