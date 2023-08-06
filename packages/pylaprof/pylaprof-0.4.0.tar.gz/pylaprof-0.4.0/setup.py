# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylaprof']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pylaprof-merge = scripts.merge:main']}

setup_kwargs = {
    'name': 'pylaprof',
    'version': '0.4.0',
    'description': 'A Python sampling profiler for AWS Lambda functions (and not only).',
    'long_description': '# pylaprof\n🚧 **Work in progress** 🚧\n\nActually already usable (check the *examples* directory) but not yet production\nready.\n\nTo install:\n```\npip install pylaprof\n```\n\n(or just copy-paste the pylaprof directory where you need it)\n\nCredits:\n- This library is heavily inspired to [pprofile](\n  https://github.com/vpelletier/pprofile).\n',
    'author': 'Giuseppe Lumia',
    'author_email': 'g.lumia@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/glumia/pylaprof',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
