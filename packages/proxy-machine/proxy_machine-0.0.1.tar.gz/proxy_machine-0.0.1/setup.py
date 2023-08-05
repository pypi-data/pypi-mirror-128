# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proxy_machine', 'proxy_machine.tools']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'beautifulsoup4==4.9.3',
 'httpx>=0.19.0,<0.20.0',
 'lxml==4.6.2',
 'proxyscrape==0.3.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.4.0,<0.5.0',
 'user_agent==0.1.9']

entry_points = \
{'console_scripts': ['proxy_machine = proxy_machine.__main__:cli']}

setup_kwargs = {
    'name': 'proxy-machine',
    'version': '0.0.1',
    'description': 'Parse 30.000 free proxies!',
    'long_description': '<h1 align="center">Proxy Machine</h1>\n<h2 align="center">\n    <a href="https://github.com/batiscuff/proxy_machine/blob/main/LICENSE" target="_blank">\n        <img alt="License: GPLv3" src="https://img.shields.io/badge/License-GPLv3-green.svg" />\n    </a>\n    <a href="https://github.com/psf/black" target="_blank">\n        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" />\n    </a>\n    </a href="https://github.com/batiscuff/proxy_machine" target="_blank">\n        <img alt="Build with love <3" src="https://img.shields.io/badge/build%20with-%F0%9F%92%9D-green" />\n    </a>\n</h2>\n\n## Description \nThe maximum number of proxies you can get is 35.000 </br>\n\n**List of sites for parsing proxies:**\n- [free-proxy-list.net/anonymous-proxy.html](http://free-proxy-list.net/anonymous-proxy.html)\n- [free-proxy-list.net](http://free-proxy-list.net)\n- [proxy-daily.com](http://proxy-daily.com)\n- [sslproxies.org](http://sslproxies.org)\n- [free-proxy-list.net/uk-proxy.html](http://free-proxy-list.net/uk-proxy.html)\n- [us-proxy.org](http://us-proxy.org)\n- [api.proxyscrape.com](http://proxyscrape.com)\n- [checkerproxy.net](http://checkerproxy.net)\n- [proxy50-50.blogspot.com](http://proxy50-50.blogspot.com)\n- [hidester.com](http://hidester.com)\n- [awmproxy.net](http://awmproxy.net)\n- [api.openproxy.space](http://openproxy.space)\n- [aliveproxy.com](http://aliveproxy.com)\n- [community.aliveproxy.com](http://community.aliveproxy.com)\n- [hidemy.name](http://hidemy.name/en)\n- [proxy11.com](http://proxy11.com)\n- [spys.me](http://spys.me/proxy.txt)\n- [proxysearcher](http://proxysearcher.sourceforge.net)\n- [fatezero](http://static.fatezero.org/tmp/proxy.txt)\n- [pubproxy](http://pubproxy.com/)\n- [proxylists](http://www.proxylists.net/http_highanon.txt)\n- [ab57ru](http://ab57.ru/downloads/proxylist.txt)\n- [shifty-https](http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt)\n- [shifty-http](http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt)\n- [sunny9577](http://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt)\n- [multiproxy](http://multiproxy.org/txt_all/proxy.txt)\n- [rootjazz](http://rootjazz.com/proxies/proxies.txt)\n- [proxyscan.io](http://www.proxyscan.io/api/proxy?format=txt&ping=500&limit=10000&type=http,https)\n- [proxy-list.download](http://www.proxy-list.download/api/v0/get?l=en&t=http)\n- [proxylistplus.com](http://list.proxylistplus.com/SSL-List-1)\n- [proxyhub.me](http://www.proxyhub.me/ru/all-https-proxy-list.html)\n- [proxylist4all.com](http://www.proxylist4all.com)\n- [proxynova.com](http://www.proxynova.com/proxy-server-list)\n- [xiladaili.com](http://www.xiladaili.com/https)\n\n## Install through pip\n\n```sh\npip install proxy_machine\n```\n## Install \n```sh\nsudo apt update && sudo apt upgrade\nsudo apt-get install python3 python3-pip\ngit clone https://github.com/batiscuff/proxy_machine\ncd proxy_machine\npip3 install -r requirements.txt\n```\n\n## Usage\n```sh\npython3 -m proxy_machine\n```\nor\n```shell\nproxy_machine --help\n```\n#### Usage with proxy checker\n```sh\npython3 -m proxy_machine -pc\n```\nIn this case, all parsed proxies will pass through the \nchecker(this will take **2-4 hours**, prepare to wait) and\nonly working proxies will be written to *proxies.txt*.\n  However, remember that the main weakness of free proxies \nis that they rapidly expire.\n#### Usage with other options\n```sh\npython3 -m proxy_machine -h\n```\n\n## Future Development\n\n[x] - Add async checking of the proxy to improve timing. <br/>\n[x] - Improve cli options and args. <br/>\n[ ] - Upload to pypi. <br/>\n[ ] - Add proxy response time to the results by calculating execution in the checker <br />\n[ ] - Add proxy location to the results <br/>\n[ ] - Add filtering and sorting options to the results <br/>\n[ ] - Add early stop, if the required number of proxies are reached with given constrains <br/>\n[ ] - Add more websites to retrieve proxies\n\n## License\n**This project is GNU [General Public License v3.0](https://github.com/batiscuff/proxy_machine/blob/main/LICENSE) licensed**\n',
    'author': 'batiscuff',
    'author_email': 'batiscuff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zekiblue/proxy_machine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
