# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dask_gateway_eks']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'boto3-stubs[iam]', 'dask-gateway>=0.9.0,<0.10.0']

extras_require = \
{'server': ['fastapi>=0.70.0,<0.71.0',
            'uvicorn[standard]>=0.15.0,<0.16.0',
            'kubernetes_asyncio>=18.20.0,<19.0.0',
            'sentry-sdk>=1.0.0,<2.0.0',
            'backoff>=1.0,<2.0',
            'cryptography>=35.0.0,<36.0.0']}

setup_kwargs = {
    'name': 'dask-gateway-eks',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
