# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtofdata',
 'rtofdata.datasource',
 'rtofdata.eventstream',
 'rtofdata.fake',
 'rtofdata.parser',
 'rtofdata.specification',
 'rtofdata.util',
 'rtofdata.validation',
 'rtofdata.validation.validators']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.11.0,<9.0.0',
 'GitPython>=3.1.19,<4.0.0',
 'Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.23,<2.0.0',
 'dacite>=1.6.0,<2.0.0',
 'docx>=0.2.4,<0.3.0',
 'docxtpl>=0.11.5,<0.12.0',
 'graphviz>=0.17,<0.18',
 'openpyxl>=3.0.7,<4.0.0',
 'pyhumps>=3.0.2,<4.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'tablib[xls,cli]>=3.0.0,<4.0.0',
 'tqdm>=4.62.2,<5.0.0']

setup_kwargs = {
    'name': 'rtofdata',
    'version': '0.1.1',
    'description': 'Data model for the Refugee Transitions Outcomes Fund (RTOF)',
    'long_description': None,
    'author': 'James Hearn',
    'author_email': 'james.hearn@socialfinance.org.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
