# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sou_eu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sou-eu',
    'version': '0.1.1',
    'description': 'Pacote que gera crachá em pdf através do nome de usuário do Github com seus dados (Avatar e Bio) e, qrcode de redes sociais (Facebook, Instagram).',
    'long_description': None,
    'author': 'Wendel dos Santos Nunes',
    'author_email': 'wendelnunes9999@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
