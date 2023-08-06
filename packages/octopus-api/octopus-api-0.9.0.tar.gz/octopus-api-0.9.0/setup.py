# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['octopus_api']
install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'more-itertools>=8.11.0,<9.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['octopus = octopus:octopus']}

setup_kwargs = {
    'name': 'octopus-api',
    'version': '0.9.0',
    'description': 'Octopus-api is a python library for performing optimized concurrent requests and API limits set by the endpoint contract. The goal with octopus is to provide the limitations and then use the standard requests library to perform the calls. The tentacles of the octopus are then used to call the endpoint and provide the responses efficiently.',
    'long_description': '# octopus-api\n![octopus_icon](image.png)\n### About\nOctopus-api is a python library for performing optimized concurrent requests and limit rate set by the endpoint contract. \nThe goal with octopus is to provide the limitations and then use the standard request library to perform the calls.\nThe tentacles of the octopus are then used to call the endpoint and provide the responses efficiently. \n\n\n## Example',
    'author': 'Filip Byrén',
    'author_email': 'filip.j.byren@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FilipByren/octopus-api',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
