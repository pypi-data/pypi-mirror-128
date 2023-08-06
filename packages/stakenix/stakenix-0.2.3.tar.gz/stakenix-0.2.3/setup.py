# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stakenix', 'stakenix.core', 'stakenix.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy<1.4',
 'clickhouse-driver>=0.2.0,<0.3.0',
 'clickhouse-sqlalchemy>=0.1.5,<0.2.0',
 'google-cloud-bigquery-storage>=2.9.0,<3.0.0',
 'mysql-connector>=2.2.9,<3.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pyarrow>=5.0.0,<6.0.0',
 'pymongo>=3.11.3,<4.0.0',
 'pymssql>=2.2.2,<3.0.0',
 'pyodbc>=4.0.30,<5.0.0',
 'sqlalchemy-bigquery>=1.2.0,<2.0.0',
 'sshtunnel>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'stakenix',
    'version': '0.2.3',
    'description': "Package for work with different DB's by a simple interface",
    'long_description': None,
    'author': 'Pavlo Levin',
    'author_email': 'levin@bbq.agency',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
