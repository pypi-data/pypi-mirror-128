# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['which_key']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'toml>=0.10.2,<0.11.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['which-key = which_key.cli:app']}

setup_kwargs = {
    'name': 'which-key',
    'version': '0.2.2',
    'description': 'Universal command launcher',
    'long_description': "# Which-Key\n\nLike [Emacs which-key](https://github.com/justbur/emacs-which-key) but for anything.\n\nWhich-Key is a customizable command launcher. It lets you define any command,\nbe it starting an application, running a script, or _anything_ else, and bind\nit to a memorable sequence of keys. Just bind `which-key` to some keyboard\nshortcut, and then trigger your commands.\n\n**Note**: This is in early development, so the UI doesn't look amazing, and there will be bugs.\n",
    'author': 'Bendik Samseth',
    'author_email': 'b.samseth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bsamseth.github.io/which-key/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
