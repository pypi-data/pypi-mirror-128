# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regta']

package_data = \
{'': ['*'], 'regta': ['templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'click>=8.0.3,<9.0.0', 'pathlib>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['regta = regta.console:main']}

setup_kwargs = {
    'name': 'regta',
    'version': '0.1.0a0',
    'description': 'Lightweight framework for executing periodic async and sync jobs in python',
    'long_description': '# regta\n**Lightweight framework for executing periodic async and sync jobs in python.**\n\n[![pypi](https://img.shields.io/pypi/v/regta.svg)](https://pypi.python.org/pypi/regta)\n[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)\n[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/master/LICENSE)\n\n## Installation\nInstall using `pip install regta` or `poetry add regta`. \nYou can check if **regta** was installed correctly with the following command\n`regta --version`, the correct output would be approximately `regta, version 0.1.0`.\n\n## Samples\n\n### To automatically create basic job use `regta new` command. \nYou can specify the job type `[async|thread|process]`.\nYou can **always** see other options by using the `--help` flag.\n```shell\n$ regta new some-async-job --type async\n> Async job SomeAsyncJob have been created at jobs/some_async_job.py.\n```\n\nThe previous command will create about this kind of code in `jobs/some_async_job.py`:\n```python\nfrom datetime import timedelta\n\nfrom regta import AsyncJob\n\n\nclass SomeAsyncJob(AsyncJob):\n    INTERVAL = timedelta(seconds=3)\n\n    async def execute(self):  # function is called every 3 seconds\n        return (\n            f"Hello from {self.__class__.__name__}! "\n            f"This message is displayed every {self.INTERVAL.seconds} seconds."\n        )\n```\n\n### To show the jobs list use `regta list` command:\n```shell\n$ regta list\n> [1] jobs were found at ./:\n> * jobs.some_async_job:SomeAsyncJob\n```\n\n### To start regta and all jobs use `regta run` command:\n```shell\n$ regta run\n> [1] jobs were found.\n> jobs.some_async_job:SomeAsyncJob - Hello from SomeAsyncJob! this message is displayed every 3 seconds.  # code of job\n.  .  .\n```\n\nIf you do not want to use the provided OOP, \nand you would like to easily reuse functions you have already written, \nyou can simply describe them as a list:\n\n[comment]: <> (`jobs/main.py`:)\n```python\n# jobs/main.py\n\ndef your_function(name):\n    print(f"Hello, {name}!")\n\nTASKS = [\n    {\n        "thread": your_function,\n        "kwargs": {"name": "User"},\n        "interval": {\n            "minutes": 5,\n        },\n    },\n]\n```\n...and pass them to the `regta run` command as `--list` param:\n```shell\n$ regta run --list jobs.main:TASKS\n> [1] jobs were found.\n> Hello, User!  # code of job\n.  .  .\n```',
    'author': 'Vladimir Alinsky',
    'author_email': 'Vladimir@Alinsky.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SKY-ALIN/regta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
