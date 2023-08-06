# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udn_songbook']

package_data = \
{'': ['*'], 'udn_songbook': ['stylesheets/*', 'templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'Markdown==3.3.4',
 'PyYAML==5.4.1',
 'WeasyPrint>=53.4,<54.0',
 'beautifulsoup4==4.9.3',
 'ukedown>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'udn-songbook',
    'version': '1.0.0',
    'description': 'songbook and songsheet management for songsheets in ukedown format',
    'long_description': None,
    'author': 'Stuart Sears',
    'author_email': 'stuart@sjsears.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
