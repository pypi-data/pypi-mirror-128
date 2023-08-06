# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stjudecloud-utilities']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['deduplicate-feature-counts = '
                     'stjudecloud-utilities.deduplicate_feature_counts:main',
                     'gtf-to-rseqc-bed = '
                     'stjudecloud-utilities.gtf_to_rseqc_bed:main',
                     'warden-counts-utils = '
                     'stjudecloud-utilities.warden_counts_utils:main']}

setup_kwargs = {
    'name': 'stjudecloud-utilities',
    'version': '1.1.0',
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
