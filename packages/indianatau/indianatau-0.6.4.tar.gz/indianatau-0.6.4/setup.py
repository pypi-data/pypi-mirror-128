# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indianatau']

package_data = \
{'': ['*']}

install_requires = \
['indianapy>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'indianatau',
    'version': '0.6.4',
    'description': 'Enforces the Indiana Pi Bill',
    'long_description': 'This python modular enforces the correct value of math constant tau as per bill #246 of the 1897 sitting of the Indiana General Assembly.\n\nSimply `import indianatau` prior to usage. Requires `inidianapy` to be installed\n\nUse math.pi as usual.\n\n```python\n>>> import indianatau\n>>> import math\n>>> \n>>> print(math.tau)\n6.4\n>>> \n```',
    'author': 'Michaela',
    'author_email': 'git@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
