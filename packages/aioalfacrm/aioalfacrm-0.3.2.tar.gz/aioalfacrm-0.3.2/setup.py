# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioalfacrm',
 'aioalfacrm.core',
 'aioalfacrm.entities',
 'aioalfacrm.fields',
 'aioalfacrm.managers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0,<4.0.0']

setup_kwargs = {
    'name': 'aioalfacrm',
    'version': '0.3.2',
    'description': 'Is an asynchronous implementation for AlfaCRM API',
    'long_description': "# AIOAlfacrm\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)\n[![Supported python versions](https://img.shields.io/pypi/pyversions/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)\n[![MIT License](https://img.shields.io/pypi/l/aioalfacrm.svg?style=flat-blue)](https://opensource.org/licenses/MIT)\n[![Downloads](https://img.shields.io/pypi/dm/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)\n[![Codecov](https://img.shields.io/codecov/c/github/stas12312/aioalfacrm?style=flat-square)](https://app.codecov.io/gh/stas12312/aioalfacrm)\n[![Tests](https://github.com/stas12312/aioalfacrm/actions/workflows/tests.yml/badge.svg)]( https://github.com/stas12312/aioalfacrm/actions)\n\n**aioalfacrm** - is an asynchronous implementation for the [AlfaCRM API](https://alfacrm.pro/rest-api)\n\n## Package is in development\n\n## Installation using pip\n\n```\n$ pip install aioalfacrm\n```\n\n*Example:*\n\n```python\nimport asyncio\nfrom aioalfacrm import AlfaClient\nfrom aioalfacrm.entities import Location\n\nHOSTNAME = 'demo.s20.online'\nEMAIL = 'api-email@email.example'\nAPI_KEY = 'user-api-token'\nBRANCH_ID = 1\n\n\nasync def main():\n    alfa_client = AlfaClient(\n        hostname=HOSTNAME,\n        email=EMAIL,\n        api_key=API_KEY,\n        branch_id=BRANCH_ID,\n    )\n    try:\n        # Check auth (Optionaly)\n        if not await alfa_client.check_auth():\n            print('Authentification error')\n            return\n        # Get branches\n        branches = await alfa_client.branch.list(page=0, count=20)\n\n        # Edit branch\n        for branch in branches:\n            branch.name = f'{branch.name} - Edited'\n            # Save branch\n            await alfa_client.branch.save(branch)\n\n        # Create location\n        location = Location(\n            branch_id=1,\n            is_active=True,\n            name='New location',\n        )\n        await alfa_client.location.save(location)\n\n    finally:\n        # Close session\n        await alfa_client.close()\n\n\nasyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # For Windows\nasyncio.run(main())\n\n\n```\n\n## Paginator\n\n```python\n# Get all entities\nfor page in alfa_client. < object >.get_paginator():\n    objects = page.items\n```\n\n## Custom fields\n\nTo work with custom fields, do the following\n\n```python\nfrom aioalfacrm import entities\nfrom aioalfacrm import fields\nfrom typing import Optional\n\n\n# Extend existing model\nclass CustomCustomer(entities.Customer):\n    custom_field: Optional[int] = fields.Integer()\n\n    # For IDE init support\n    def __init__(\n            self,\n            custom_field: Optional[int] = None,\n            *args,\n            **kwargs,\n    ):\n        super(CustomCustomer, self).__init__(custom_field=custom_field, *args, **kwargs)\n\n\n# Create custom alfa client with new model\nfrom aioalfacrm import AlfaClient\nfrom aioalfacrm import managers\n\n\nclass CustomAlfaClient(AlfaClient):\n\n    def __init__(self, *args, **kwargs):\n        super(CustomAlfaClient, self).__init__(*args, **kwargs)\n\n        self.customer = managers.Customer(\n            api_client=self.api_client,\n            entity_class=CustomCustomer,\n        )\n\n\n# Create custom alfa client\nimport asyncio\n\nHOSTNAME = 'demo.s20.online'\nEMAIL = 'api-email@email.example'\nAPI_KEY = 'user-api-token'\nBRANCH_ID = 1\n\n\nasync def main():\n    alfa_client = CustomAlfaClient(hostname=HOSTNAME, email=EMAIL, api_key=API_KEY, branch_id=BRANCH_ID)\n    try:\n        customers = await alfa_client.customer.list()\n        for customer in customers:\n            print(customer.custom_field)\n    finally:\n        await alfa_client.close()\n\n\nasyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # For Windows\nasyncio.run(main())\n```",
    'author': 'Stanislav Rush',
    'author_email': '911rush@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas12312/aioalfacrm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
