# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rst_language_server']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'docutils>=0.18,<0.19', 'pygls>=0.11.3,<0.12.0']

entry_points = \
{'console_scripts': ['rst-ls = rst_language_server.cli:main']}

setup_kwargs = {
    'name': 'rst-language-server',
    'version': '0.1.0',
    'description': 'Server implementation of the Language Server Protocol for reStructuredText',
    'long_description': '===================\nRST Language Server\n===================\nRST Language Server implements the server side of the `Language Server Protocol`_ (LSP) for the `reStructuredText`_ markup language.\n\nRST Language Server is intended to be used by text editors implementing the client side of the protocol. See `langserver.org <https://langserver.org/#implementations-client>`_ for a list of implementing clients.\n\n.. _reStructuredText: https://docutils.sourceforge.io/rst.html\n.. _Language Server Protocol: https://microsoft.github.io/language-server-protocol/\n\nFeatures\n========\nAutocompletion of title adornments\n\n.. image:: https://raw.githubusercontent.com/digitalernachschub/rst-language-server/a4c81b4805d8ea913042c82e73eb8bae56e88c58/assets/autocomplete_title_adornments.webp\n\nInstallation\n============\nRST Language Server is available as a package on PyPI and can be installed via `pip`:\n\n.. code:: sh\n\n    $ pip install --user rst-language-server\n\nUsage with Kate\n===============\n\nUsing RST Language Server with `Kate`_ requires the `LSP Client Plugin`_. Once the plugin is activated in the settings a new settings symbol named *LSP-Client* appears. Click on the section, select the *User Server Settings* tab and paste the following server configuration.\n\n.. code:: json\n\n    {\n        "servers": {\n            "rst": {\n                "command": ["rst-ls"],\n                "highlightingModeRegex": "^reStructuredText$"\n            }\n        }\n    }\n\nThis will start RST Language Server when opening any file that is configured to use the reStructuredText syntax highlighting.\n\n.. _Kate: https://apps.kde.org/kate/\n.. _LSP Client Plugin: https://docs.kde.org/stable5/en/kate/kate/kate-application-plugin-lspclient.html\n\n\nIs my editor supported?\n=======================\nRST Language Server can be used with any text editor that implements a Language Client. See `this list <https://langserver.org/#implementations-client>`_ of Language Client implementations.\n\n\nDevelopment configuration with Kate\n===================================\nThe RST Language Server is executed as a subprocess of the Language Client. Therefore, if we want to see log output in Kate we need to write the logs to a file using the `--log-file` command line option. We also set the log level to `debug` in order to view the JSON-RPC messages exchanged between client and server. Lastly, we configure the `root` (i.e. the working directory of the executed command) to the directory where our source code lives in and use `poetry run` to execute the code in the Git repository:\n\n.. code:: json\n\n    {\n        "servers": {\n            "rst": {\n                "command": ["poetry", "run", "rst-ls", "--log-file=/tmp/rst-ls.log", "--log-level=debug"],\n                "root": "/path/to/rst-language-server-repo",\n                "highlightingModeRegex": "^reStructuredText$"\n            }\n        }\n    }\n',
    'author': 'Michael Seifert',
    'author_email': 'm.seifert@digitalernachschub.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digitalernachschub/rst-language-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
