# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioudp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aioudp',
    'version': '0.1.0',
    'description': 'A better API for asynchronous UDP',
    'long_description': '# AioUDP\n\n[![Documentation Status](https://readthedocs.org/projects/aioudp/badge/?version=latest)](https://aioudp.readthedocs.io/en/latest/?badge=latest)\n\n> A better API for asynchronous UDP\n\nA [websockets](https://websockets.readthedocs.io/en/stable/index.html)-like API for [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)\n\nHere\'s an example echo server:\n\n```py\nimport aioudp\nimport asyncio\n\nasync def main():\n    async def handler(connection):\n        async for message in connection:\n            await connection.send(message)\n    async with aioudp.serve("localhost", 9999, handler):\n        await asyncio.Future()  # Serve forever\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\nAnd a client to connect to the server:\n\n```py\nimport aioudp\nimport asyncio\n\nasync def main():\n    async with aioudp.connect("localhost", 9999) as connection:\n        await connection.send(b"Hello world!")\n        assert await connection.recv() == b"Hello world!"\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/aioudp',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
