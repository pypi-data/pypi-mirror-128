# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sou_eu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sou-eu',
    'version': '0.1.6',
    'description': 'Pacote que gera crachá em pdf através do nome de usuário do Github com seus dados (Avatar e Bio) e, qrcode de redes sociais (Facebook, Instagram).',
    'long_description': '# sou_eu\n\n## Crachá personalizado com dados do github e/ou QRcodes dos perfis do Facebook e Instagram\n\n<p> Usuário completo </p>\n\n![Usuário + QRcode do Facebook + QRcod do Instagram](https://raw.githubusercontent.com/WendelSantosNunes/thatsme/main/demo/UC.png)\n\n<p> Usuário básico </p>\n\n![Usuário + QRcode do Github](https://raw.githubusercontent.com/WendelSantosNunes/thatsme/main/demo/UB.png)\n\nO sou_eu foi criado em python3.8. O sistema pode ser usado em Windows, Linux e Mac.\n\nColaboradores: <br />\n\n1. [Wendel Nunes](https://github.com/WendelSantosNunes) <br />\n2. [Eva Luana](https://github.com/evalasilva) <br />\n\n### Descrição:\n\n> O sou_eu é um pacote criado durante a disciplina de Programação Orientada a Objetos 2 (POO2), ministrada no curso de Sistema de Informação na Universidade Federal do Piauí-CSHNB.\n> Não há intuito comercial, ou governamental.\n> O sou_eu foi produzido para fins de aprendizado e experiência em desenvolvimento de pacotes, contudo pode ser utilizado por qualquer usuário do Github que tenha interesse. O projeto possui a Licença do MIT disponibilizada pelo próprio Github.\n> O sou_eu pode ser utilizado como cartão virtual, em formato PDF, para qualquer pessoa física/jurídica que queira compartilhar suas informações de contato de forma padronizada, elegante e eficiente.\n\n## Requisitos:\n\n1. [python3](https://www.python.org/downloads/)\n2. [pip](https://pip.pypa.io/en/stable/installation/)\n3. [pyqrcode](https://pypi.org/project/PyQRCode/)\n4. [fpdf2](https://pypi.org/project/fpdf2/)\n5. [pypng](https://pypi.org/project/pypng/)\n\n## Instalação:\n\n### Python3\n\n1. Windows: [Download](https://www.python.org/downloads/)\n\n2. Linux Debian e derivados.\n\n   ```\n       $ sudo apt-get install python3\n   ```\n\n### PIP\n\n1. Instalação do PIP - LINUX\n\n   ```Debian\n   \t$ sudo  apt-get install python-pip\n   ```\n\n   ```Red Hat/ OpenSUSe\n   \t$ sudo  yum install python-pip\n   ```\n\n### thatsme\n\n1. Instalação do thatsme\n\n   pip install sou_eu\n\n## Execução:\n\n1.  Instale o pacote;\n2.  Importe a classe Cracha:\n    (from sou_eu import thatsme);\n3.  Crie um objeto da classe:\n\n    3.1. O objeto deve enviar como parâmetro("endereco_local_armazenar_pdf","nome_usuario_github","url_perfil_facebook", "url_perfil_instagram");\n\n        from sou_eu import thatsme\n\n        usuario = thatsme.Cracha(\'endereco\',\'usuario_github\', \'url_perfil_facebook\', \'url_perfil_instagram\')\n\n        usuario.cracha()\n\n    3.2. O parâmetro "nome_usuario_github" é obrigatório;\n    3.3. Caso não hajam as URLs dos perfins do Facebook e/ou Instagram, deve ser inserido "None" no local devido;\n\n        from sou_eu import thatsme\n\n        usuario = thatsme.Cracha(\'endereco\',\'usuario_github\', None, \'url_perfil_instagram\')\n\n        usuario.cracha()\n\n    3.4. Para o caso de não haver URL do Facebook nem do Instagram será adicionado o QRcode do perfil do usuário no Github;\n\n    3.5. Se o usuário do Github não for encontrado será apresentado o ERROR 404.\n',
    'author': 'Wendel dos Santos Nunes',
    'author_email': 'wendelnunes9999@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WendelSantosNunes/sou_eu',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
