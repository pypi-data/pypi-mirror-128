# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['examples', 'examples.webapi', 'serde', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['jinja2', 'stringcase', 'typing_inspect>=0.4.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses',
                             'backports-datetime-fromisoformat>=1,<2'],
 'all': ['msgpack', 'toml', 'pyyaml'],
 'msgpack': ['msgpack'],
 'toml': ['toml'],
 'yaml': ['pyyaml']}

setup_kwargs = {
    'name': 'pyserde',
    'version': '0.5.3',
    'description': 'Yet another serialization library on top of dataclasses',
    'long_description': '# `pyserde`\n\nYet another serialization library on top of [dataclasses](https://docs.python.org/3/library/dataclasses.html).\n\n[![image](https://img.shields.io/pypi/v/pyserde.svg)](https://pypi.org/project/pyserde/)\n[![image](https://img.shields.io/pypi/pyversions/pyserde.svg)](https://pypi.org/project/pyserde/)\n![Tests](https://github.com/yukinarit/pyserde/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/yukinarit/pyserde/branch/master/graph/badge.svg)](https://codecov.io/gh/yukinarit/pyserde)\n\n[Guide](https://yukinarit.github.io/pyserde/guide) | [API Docs](https://yukinarit.github.io/pyserde/api/serde.html) | [Examples](./examples)\n\n## Overview\n\nDeclare a class with pyserde\'s `@serialize` and `@deserialize` decorators.\n\n```python\n@deserialize\n@serialize\n@dataclass\nclass Foo:\n    i: int\n    s: str\n    f: float\n    b: bool\n```\n\nYou can serialize `Foo` object into JSON.\n\n```python\n>>> to_json(Foo(i=10, s=\'foo\', f=100.0, b=True))\n{"i": 10, "s": "foo", "f": 100.0, "b": true}\n```\n\nYou can deserialize JSON into `Foo` object.\n```python\n>>> from_json(Foo, \'{"i": 10, "s": "foo", "f": 100.0, "b": true}\')\nFoo(i=10, s=\'foo\', f=100.0, b=True)\n```\n\n## Features\n\n- Supported data formats\n    - JSON\n\t- Yaml\n\t- Toml\n\t- MsgPack\n- Supported types\n    - Primitives (`int`, `float`, `str`, `bool`)\n    - Containers (`List`, `Set`, `Tuple`, `Dict`)\n    - [`typing.Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)\n    - [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union)\n    - User defined class with [`@dataclass`](https://docs.python.org/3/library/dataclasses.html)\n    - [`typing.NewType`](https://docs.python.org/3/library/typing.html#newtype) for primitive types\n    - [`typing.Any`](https://docs.python.org/3/library/typing.html#the-any-type)\n    - [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum) and [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum)\n    - Standard library\n        - [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html)\n        - [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html)\n        - [`uuid.UUID`](https://docs.python.org/3/library/uuid.html)\n        - [`datetime.date`](https://docs.python.org/3/library/datetime.html#date-objects), [`datetime.time`](https://docs.python.org/3/library/datetime.html#time-objects), [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects)\n        - [`ipaddress`](https://docs.python.org/3/library/ipaddress.html)\n- [Python 3.9 type hinting](docs/features/python3.9-type-hinting.md)\n- [Postponed evaluation of type annotation](docs/features/postponed-evaluation-of-type-annotation.md)\n- [Forward reference](docs/features/forward-reference.md)\n- [Case Conversion](docs/features/case-conversion.md)\n- [Rename](docs/features/rename.md)\n- [Skip](docs/features/skip.md)\n- [Conditional Skip](docs/features/conditional-skip.md)\n- [Custom field (de)serializer](docs/features/custom-field-serializer.md)\n- [Custom class (de)serializer](docs/features/custom-class-serializer.md)\n- [Flatten](docs/features/flatten.md)\n\n## LICENSE\n\nThis project is licensed under the [MIT license](https://github.com/yukinarit/pyserde/blob/master/LICENSE).\n',
    'author': 'yukinarit',
    'author_email': 'yukinarit84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yukinarit/pyserde',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
