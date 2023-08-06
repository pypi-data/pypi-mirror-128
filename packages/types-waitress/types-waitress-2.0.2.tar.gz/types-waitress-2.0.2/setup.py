from setuptools import setup

name = "types-waitress"
description = "Typing stubs for waitress"
long_description = '''
## Typing stubs for waitress

This is a PEP 561 type stub package for the `waitress` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `waitress`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/waitress. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `2445eddb4b67fdaa58ec7c2113ff1542021a6206`.
'''.lstrip()

setup(name=name,
      version="2.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['waitress-stubs'],
      package_data={'waitress-stubs': ['__init__.pyi', 'adjustments.pyi', 'buffers.pyi', 'channel.pyi', 'compat.pyi', 'parser.pyi', 'proxy_headers.pyi', 'receiver.pyi', 'rfc7230.pyi', 'runner.pyi', 'server.pyi', 'task.pyi', 'trigger.pyi', 'utilities.pyi', 'wasyncore.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
