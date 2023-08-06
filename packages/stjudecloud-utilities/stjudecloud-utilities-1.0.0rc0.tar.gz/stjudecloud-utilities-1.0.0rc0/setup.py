# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['deduplicate-samples = src.deduplicate_samples:main',
                     'gtf-to-rseqc-bed = src.gtf_to_rseqc_bed:main']}

setup_kwargs = {
    'name': 'stjudecloud-utilities',
    'version': '1.0.0rc0',
    'description': 'A set of utilities used on the St. Jude Cloud project.',
    'long_description': None,
    'author': 'St. Jude Cloud',
    'author_email': 'support@stjude.cloud',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
