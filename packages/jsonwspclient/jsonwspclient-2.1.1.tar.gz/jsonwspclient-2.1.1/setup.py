# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonwspclient']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'jsonwspclient',
    'version': '2.1.1',
    'description': 'Flexible JSON-WSP client.',
    'long_description': "=============\njsonwspclient\n=============\n**jsonwspclient** wants to be a simple and, i hope, flexible python client for JSON-WSP services.\nIt is designed for make easy to call services methods and to access to response info and attachments.\n\n**JsonWspClient** is based on python Requests_ and uses the `Session object`_.\nSo allows you to persist certain parameters and the cookies across requests.\n\nIt supports also **events_handling**, **response_processing**, **params_mapping** and **fault_handling**.\nSo you can have a good control over your scripts flow.\n\n.. note::\n\n    **jsonwspclient**  is designed to be used with Ladon_. \n    and it is based on the original ladon's jsonwsp_ client.\n\n    However it should be flexible enough to be used with other JSON-WSP services.\n\n    See `JsonWspClient docs`_.\n\n    .. _Ladon: https://bitbucket.org/jakobsg/ladon\n    .. _Requests: http://docs.python-requests.org/\n    .. _jsonwsp: https://bitbucket.org/jakobsg/ladon/src/68b7b47bcf217e0511559d831c621e33ca548ca2/src/ladon/clients/jsonwsp.py?at=master&fileviewer=file-view-default\n    .. _`Session object`: http://docs.python-requests.org/en/master/user/advanced/#session-objects\n    .. _`JsonWspClient docs`: http://jsonwspclient.readthedocs.io/en/latest\n\n\nNote\n====\n\nThis project has been set up using PyScaffold 2.5. For details and usage\ninformation on PyScaffold see http://pyscaffold.readthedocs.org/.\n",
    'author': 'ellethee',
    'author_email': 'luca800@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/ellethee/jsonwspclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
