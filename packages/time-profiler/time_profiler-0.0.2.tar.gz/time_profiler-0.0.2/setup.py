# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_profiler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'time-profiler',
    'version': '0.0.2',
    'description': 'This project provides a method for determining how long it takes a function to complete its execution.',
    'long_description': "# time_profiler\n\nThis is a Python module for profiling a function's time usage. It's quite useful for determining how long a function will take to execute.\n\n# Installation\n\nInstall via pip:\n\n```\npip install time_profiler\n```\n\n# Usage\n\nFirst decorate the function you would like to profile with **@timer()** and then run that file containing function.\n\nIn the following example, we create a simple function called **sample_func** that allocates lists a, b and then deletes b:\n\n```\nfrom time_profiler import timer\n\n@timer()\ndef sample_func():\n    a = [1] * (10 ** 6)\n    b = [2] * (2 * 10 ** 7)\n    del b\n    \n    return a\n\nif __name__ == '__main__':\n    sample_func()\n```\n\nThen execute the code normally. For example, if the file name was *example.py*, this would result in:\n\n```\npython example.py\n```\n\nOutput will be displayed in the terminal as follow:\n\n```\n11-24-2021 10:07:05 AM - timer - INFO - sample_func function ran in 0.10 secs\n```\n\n# Parameters\n\nThis decorator(@timer()) takes two optional paramaters.\n- file_log: By default is set to false, which means that log file is not created but when set to true there should be a log file named **timer.log**. Breifly this argument is of boelen type.\n\n- exp_time: Here you can try to estimate the time to be used. When estimated time is less than actual used time, you get warning log instead of info.\n\n# Development\n\nLatest sources are available from github:\n\n> [https://github.com/harerakalex/timer](https://github.com/harerakalex/timer)\n\n# Author\n\nCarlos Harerimana\n\n# License\n\nMIT\n",
    'author': 'harerakalex',
    'author_email': 'hareraloston@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/harerakalex/timer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
