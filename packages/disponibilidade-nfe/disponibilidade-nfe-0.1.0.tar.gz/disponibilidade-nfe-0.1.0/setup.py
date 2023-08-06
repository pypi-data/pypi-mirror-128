# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disponibilidade_nfe']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'requests-mock>=1.9.3,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'disponibilidade-nfe',
    'version': '0.1.0',
    'description': 'Web scraping da Disponibilidade dos Webservices da Sefaz através do portal NFe.',
    'long_description': "# Disponibilidade NFe\n\n[![Test](https://github.com/leogregianin/disponibilidade-nfe/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/leogregianin/disponibilidade-nfe/actions/workflows/main.yml)\n\nProjeto de Web scraping para verificar a disponibilidade dos Webservices de todas as Secretarias de Fazenda (Sefaz) emitente de Nota Fiscal Eletrônica (NFe) através do Portal Nacional da NFe: http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx\n\n\n## Instalar\n\n```console\n$ poetry install\n```\n\n## Rodar testes\n\n```console\n$ poetry run tox\n```\n\n## Exemplos\n\n```python\nfrom disponibilidade_nfe.nfe import DisponibilidadeNFe\n\ndisp_nfe = DisponibilidadeNFe()\nprint(disp_nfe.get_status())\n```\n\nResultado:\n```console\n[\n    {\n        'autorizador': 'AM',\n        'autorizacao': 'verde',\n        'retorno_autorizacao': 'verde',\n        'inutilizacao': 'verde',\n        'consulta_protocolo': 'verde',\n        'status_servico': 'verde',\n        'tempo_medio': '-',\n        'consulta_cadastro': '',\n        'recepcao_evento': 'verde',\n        'ultima_verificacao': '23/11/2021 23:06:31'\n    }, {\n        'autorizador': 'BA',\n        'autorizacao': 'verde',\n        'retorno_autorizacao': 'verde',\n        'inutilizacao': 'verde',\n        'consulta_protocolo': 'verde',\n        'status_servico': 'verde',\n        'tempo_medio': '-',\n        'consulta_cadastro': 'verde',\n        'recepcao_evento': 'verde',\n        'ultima_verificacao': '23/11/2021 23:06:31'\n    }, {\n        ...\n    }\n]\n```\n\n## License\n\nThis package is licensed under [MIT license](/LICENSE).",
    'author': 'Leonardo Gregianin',
    'author_email': 'leogregianin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leogregianin/disponibilidade-nfe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
