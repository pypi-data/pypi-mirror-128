# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_grpc_plugin']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.39.0,<2.0.0',
 'mypy-protobuf>=2.9,<3.0',
 'poetry>=1.2.0a2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['grpc = '
                               'poetry_grpc_plugin.plugins:GrpcApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-grpc-plugin',
    'version': '0.1.1',
    'description': 'gRPC Poetry plugin',
    'long_description': '# Poetry gRPC plugin\n\nA [**Poetry**](https://python-poetry.org/) plugin to run the Protocol Buffers compiler with gRPC support.\n\n### Installing the plugin\n\nRequires Poetry version `1.2.0a2` or above\n\n```shell\npoetry plugin add poetry-grpc-plugin\n```\n\n### Usage\n\nTo run it manually:\n\n```console\npoetry help protoc\n\nUsage:\n  protoc [options]\n\nOptions:\n      --proto_path[=PROTO_PATH]             [default: "."]\n      --python_out[=PYTHON_OUT]             [default: "."]\n      --grpc_python_out[=GRPC_PYTHON_OUT]   [default: "."]\n...\n```\n\nRun on `poetry update`\n\n```toml\n[tool.poetry-grpc-plugin]\n```\n\nAdditional config\n\n```toml\n[tool.poetry-grpc-plugin]\nproto_path = "dir/protos"\npython_out = "generated/"\ngrpc_python_out = "generated/"\n```\n',
    'author': 'Federico Jaite',
    'author_email': 'fede_654_87@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fedej/poetry-grpc-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
