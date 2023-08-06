# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ss_test', 'ss_test.console']

package_data = \
{'': ['*']}

install_requires = \
['statsmodels>=0.13.1,<0.14.0']

entry_points = \
{'console_scripts': ['format = poetry_scripts:format_fix',
                     'format-check = poetry_scripts:format_check',
                     'lint = poetry_scripts:lint',
                     'qa = poetry_scripts:qa',
                     'ss-test = ss_test.console.application:main',
                     'test = poetry_scripts:test',
                     'type-check = poetry_scripts:type_check']}

setup_kwargs = {
    'name': 'ss-test',
    'version': '0.0.1a8',
    'description': 'A python module just to test publish',
    'long_description': "# ss-test\n\ntest pypi publish\n\nInstall\n\n```bash\npip install -i https://test.pypi.org/simple/ ss-test --extra-index-url https://pypi.org/simple\n```\n\n## Usage\n\n```\nusage: ss-test [-h] [--type {ratio,numeric,boolean}] [--effect EFFECT]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --type {ratio,numeric,boolean}\n                        The type\n  --effect EFFECT       The effect, should be a number/float\n```\n\nexample:\n```bash\nss-test --type numeric --effect 0.5\n\n# output\n# Welcome to test pacakage!\n# Calculating effect 0.5 of metric type numeric\n# And Here's your secret result: 64.0\n```",
    'author': None,
    'author_email': None,
    'maintainer': 'WendyChiang',
    'maintainer_email': 'wendypjchiang@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
