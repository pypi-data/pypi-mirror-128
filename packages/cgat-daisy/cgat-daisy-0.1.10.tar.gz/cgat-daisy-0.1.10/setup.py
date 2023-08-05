# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['daisy', 'daisy.tasks', 'daisy.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.27,<2.0.0',
 'apsw>=3.36.0,<4.0.0',
 'cgatcore>=0.6.9,<0.7.0',
 'gevent>=21.8.0,<22.0.0',
 'pandas>=1.3.4,<2.0.0',
 'paramiko>=2.8.0,<3.0.0',
 'pysam>=0.17.0,<0.18.0',
 'ruamel.yaml>=0.17.17,<0.18.0',
 'ruffus>=2.8.4,<3.0.0']

entry_points = \
{'console_scripts': ['daisy = daisy.tools.cli:main']}

setup_kwargs = {
    'name': 'cgat-daisy',
    'version': '0.1.10',
    'description': 'A benchmarking framework',
    'long_description': None,
    'author': 'Andreas Heger',
    'author_email': 'andreas.heger@genomicsplc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
