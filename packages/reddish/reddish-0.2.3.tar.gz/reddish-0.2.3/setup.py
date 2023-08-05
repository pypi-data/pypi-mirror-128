# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reddish', 'reddish.models']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0', 'pydantic>=1.8.2,<2.0.0', 'trio>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'reddish',
    'version': '0.2.3',
    'description': 'An async redis client library with a minimal api',
    'long_description': "# reddish - an async redis client with minimal api\n\n* [Features](#features)\n* [Installation](#installation)\n* [Minimal Example](#minimal-example)\n* [Usage](#usage)\n\n## Features\n* `async`/`await` using `trio`'s stream primitives (TCP, TCP+TLS, Unix domain sockets)\n* minimal api so you don't have to relearn how to write redis commands\n* supports all redis commands including modules except `SUBSCRIBE`, `PSUBSCRIBE` and `MONITOR` [^footnote]\n* parses responses back into python types if you like (powered by [pydantic](https://github.com/samuelcolvin/pydantic))\n* works with every redis version and supports both `RESP2`and `RESP3` protocols\n\n[^footnote]: Commands like `SUBSCRIBE` or `MONITOR` take over the redis connection for listeting to new events \nbarring regular commands from being issued over the connection. \n\n## Installation\n```\npip install reddish\n```\n\n## Minimal Example\n```python\nimport trio\nfrom reddish import Redis, Command\n\nredis = Redis(await trio.open_tcp_stream('localhost', 6379))\n\nassert b'PONG' == await redis.execute(Command('PING'))\n```\n\n## Usage\n\n### Commands with a fixed number of arguments\n```python\n# simple command without any arguments\nCommand('PING')\n\n# commands with positional arguments\nCommand('ECHO {}', 'hello world')\n\n# commands with keyword arguments\nCommand('SET {key} {value}', key='foo', value=42)\n```\n\n### Commands with response parsing\n```python\n# return response unchanged from redis\nassert b'42' == await redis.execute(Command('ECHO {}', 42))\n\n# parse response as type\nassert 42 == await redis.execute(Command('ECHO {}', 42).into(int))\n\n# use any type that works with pydantic\nfrom pydantic import Json\nimport json\n\ndata = json.dumps({'alice': 30, 'bob': 42})\nresponse == await redis.execute(Command('ECHO {}', data).into(Json))\nassert response == json.loads(data)\n```\n\n### Commands with variadic arguments\n```python\nfrom reddish import Args\n\n# inlining arguments\nCommand('DEL {keys}', keys=Args(['foo', 'bar']))  # DEL foo bar\n\n# inlining pairwise arguments \ndata = {'name': 'bob', 'age': 42}\nCommand('XADD foo * {fields}', fields=Args.from_dict(data))  # XADD foo * name bob age 42\n``` \n\n### Pipelining commands\n```python\nfoo, bar = await redis.execute(Command('GET', 'foo'), Command('GET', 'bar'))\n```\n\n### Transactions\n```python\nfrom reddish import MultiExec\n\ntx = MultiExec(\n    Command('ECHO {}', 'foo'),\n    Command('ECHO {}', 'bar')\n)\n\nfoo, bar = await redis.execute(tx)\n\n# pipelining together with transactions\n[foo, bar], baz = await redis.execute(tx, Command('ECHO {}', 'baz'))\n```",
    'author': 'Sascha Desch',
    'author_email': 'sascha.desch@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stereobutter/reddish',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
