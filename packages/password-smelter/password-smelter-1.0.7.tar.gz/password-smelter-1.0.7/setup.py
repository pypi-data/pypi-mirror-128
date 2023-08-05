# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['password_smelter', 'password_smelter.lib']

package_data = \
{'': ['*'], 'password_smelter.lib': ['assets/*']}

install_requires = \
['XlsxWriter>=1.4.0,<2.0.0',
 'dash-bootstrap-components>=0.12.0,<0.13.0',
 'dash>=1.20.0,<2.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'password-stretcher>=1.0.4,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'psutil>=5.8.0,<6.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['password-smelter = password_smelter.smelter:main']}

setup_kwargs = {
    'name': 'password-smelter',
    'version': '1.0.7',
    'description': 'A password analyzer with pretty graphs and a dark mode',
    'long_description': None,
    'author': 'TheTechromancer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheTechromancer/password-smelter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
