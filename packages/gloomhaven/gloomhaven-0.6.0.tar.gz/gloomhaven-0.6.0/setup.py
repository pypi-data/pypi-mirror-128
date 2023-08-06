# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gloomhaven']

package_data = \
{'': ['*'], 'gloomhaven': ['templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0', 'PyYAML>=5.4.1,<6.0.0']

extras_require = \
{':extra == "analyze"': ['dictdiffer>=0.9.0,<0.10.0'],
 'analyze': ['pandas>=1.3.3,<2.0.0',
             'dask[distributed]>=2021.9.0,<2022.0.0',
             'matplotlib>=3.4.3,<4.0.0',
             'jupyter>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'gloomhaven',
    'version': '0.6.0',
    'description': 'Probability evaluation of Gloomhaven attack modifier decks',
    'long_description': None,
    'author': 'Zachary Coleman',
    'author_email': 'zacharywcoleman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zachcoleman/gloomhaven',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
