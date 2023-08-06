# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sortepy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sorte.py = sortepy.script:main']}

setup_kwargs = {
    'name': 'sorte.py',
    'version': '0.1.0.dev1',
    'description': 'Geração e conferência de apostas de loterias.',
    'long_description': "sorte.py\n========\n\n---\n\nAVISO\n-----\n\n`sorte.py` não consegue fazer mais consultas (o que também afeta as conferências),\ndesde que a Caixa mudou drasticamente o sistema. Este problema está sendo investigado.\n\nVeja https://github.com/wagnerluis1982/sorte.py/pull/4\n\n---\n\nSobre\n-----\n\nO `sorte.py` é um script Python de linha de comando para geração e conferência\nde apostas de loterias.  Surgiu com o propósito principal de conferir apostas\nfeitas nas Casas Lotéricas do Brasil.\n\nA geração de números é como a *surpresinha*, mas os jogos têm que ser\npreenchidos manualmente.\n\nInstalação\n----------\n\nAVISO: `sorte.py` requer no mínimo o Python 3 para a instalação com sucesso.\n\nPara instalar, basta executar o `pip` pondo como argumento o repositório.\n\n    $ pip3 install git+https://github.com/wagnerluis1982/sorte-py\n\nLicença\n-------\n\nO código fonte é licenciado sob a licença [GPLv3].\n\n[GPLv3]: http://licencas.softwarelivre.org/gpl-3.0.pt-br.html\n\nModo de uso\n-----------\n\n### Gerando números para aposta\n\nPara ter *uma* aposta gerada, na quantidade padrão da Quina, por exemplo, basta\n\n    $ sorte.py quina\n\n#### Todas as opções de geração\n\n    -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1\n    -n --numeros      Quantos números cada aposta gerada terá. Se não informado\n                        o padrão depende da LOTERIA informada\n    -h --help         Mostra esta ajuda e finaliza\n\nLoterias disponíveis: duplasena, lotofacil, lotomania, megasena, quina.\n\n### Conferindo apostas\n\nPara conferir três apostas do último concurso, execute\n\n    $ sorte.py quina '1,23,39,44,50' '5 9 15 50 75' '1-3 30 56'\n\nCada argumento é uma aposta. Os números podem ser separados por vírgula ou\nespaço em branco. Caso utilize hífens entre dois números, será considerado um\nintervalo.\n\nSe for preciso especificar o concurso, então basta utilizar o parâmetro\n`-c|--concurso`, conforme exemplo abaixo\n\n    $ sorte.py quina -c 1325 '1,23,39,44,50' '5 9 15 50 75'\n\nCaso o parâmetro `-i|--stdin` seja ativado, as apostas serão lidas da entrada\npadrão, uma por linha até encontrar o EOF (Ctrl-D no Linux).\n\n    $ sorte.py quina -c 1325 -i\n    1,23,39,44,50\n    5 9 15 50 75\n    1-3 30 56\n\nCom o parâmetro `-i`, fica possível a utilização de um arquivo com as apostas,\nconforme exemplo.\n\n    $ sorte.py quina -c 1325 -i < fezinha-na-quina.txt\n\nAs linhas que iniciam por `#` são consideradas comentários.\n\n#### Conferindo vários concursos\n\nO script permite conferir vários concursos de uma vez, passando o argumento `-c`\nvárias vezes\n\n    $ sorte.py duplasena -c 1130 -c 1131 -i < minhas_apostas.txt\n\nou informar uma faixa de valores\n\n    $ sorte.py quina -c 1325-1330 -i < fezinha.txt\n\n#### Todas as opções de conferência\n\n    -c --concurso     Número do concurso para consultar ou conferir. Pode ser\n                        passada várias vezes\n    -i --stdin        Recebe as apostas da entrada padrão, útil para manter as\n                        apostas em um arquivo\n\n### Consultando resultados\n\nPara consultar, execute\n\n    $ sorte.py JOGO -c|--concurso NUM\n\nonde o argumento `NUM` é o número do concurso em que quer o resultado. Se quiser\nobter o último resultado disponível, basta passar um argumento vazio, conforme\ncomando abaixo.\n\n    $ sorte.py lotofacil -c=\n\n#### Consultando vários concursos\n\nSemelhante à conferência, é possível consultar vários concursos de uma vez:\n\n    $ sorte.py duplasena -c 1130 -c 1131\n    $ sorte.py duplasena -c 1136-1145\n\n#### Todas as opções de consulta\n\n    -c --concurso     Número do concurso para consultar ou conferir. Pode ser\n                        passada várias vezes\n",
    'author': 'Wagner Macedo',
    'author_email': 'wagnerluis1982@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wagnerluis1982/sorte.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
