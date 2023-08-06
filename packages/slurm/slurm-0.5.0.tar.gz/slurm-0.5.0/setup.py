# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurm']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'dill', 'pyyaml']

setup_kwargs = {
    'name': 'slurm',
    'version': '0.5.0',
    'description': 'A bunch tools I have created over the years',
    'long_description': '![](https://github.com/MomsFriendlyRobotCompany/slurm/blob/master/pics/slurm.jpg?raw=true)\n\n# Slurm\n\n\n[![Actions Status](https://github.com/MomsFriendlyRobotCompany/slurm/workflows/walchko%20pytest/badge.svg)](https://github.com/MomsFriendlyRobotCompany/slurm/actions)\n![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/slurm)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slurm)\n![PyPI](https://img.shields.io/pypi/v/slurm)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/slurm?color=aqua)\n\nThis is a collection of tools I have used over the years collected together.\n\n## Signal Catcher\n\n`SignalCatch` catches `SIGINT` and `SIGTERM` signals and sets\n`SignalCatch.kill` to `True`.\n\n```python\nfrom slurm import SignalCatch\n\nsig = SignalCatch()\n\nwhile True:\n    if sig.kill == True:\n        exit(0)\n```\n\n## Simple Processes\n\n```python\nfrom slurm import SimpleProcess\n\ndef func():\n    # some simple process that does something\n    for _ in range(10):\n        print(".", end="")\n        time.sleep(0.1)\n    print("")\n\ndef test_process():\n    p = SimpleProcess()\n    p.start(func)\n    print(p)\n    p.join(timeout=2.0) # if not ended in 2 sec, will terminate() the process\n```\n\n## Storage\n\n```python\nfrom slurm import storage\n\npick = storage.read("file.pickle")\nyaml = storage.read("file.yaml")\njson = storage.read("file.json")\njson = storage.read("file", "json")\n\n\ndata = [1,2,3,4]\nstorage.write("tom.pickle", data)\nstorage.write("bob.json", data)\nstorage.write("guess.file", data, "yml")\n```\n\nAlso, for YAML files, you can put comments in:\n\n```python\ninfo = {\n    "a": 1\n}\n\nnum = 5\ncomm = f"""\n# hello {num} dogs!!\n# there\n# big boy\n"""\nstorage.write("t.yaml", info, comments=comm)\n```\n\nwhich will produce:\n\n```yaml\n# hello 5 dogs!!\n# there\n# big boy\n\na: 1\n```\n\n## Science Storage\n\nOver the years I have collected a lot of data, but not completely documented\nthe sensors or their settings. I am trying to setup a data file that can:\n\n- use primarly standard python libraries to read (exception `dill` for `namedtuples`)\n- self documenting with info and `namedtuples`\n- can use `gzip` for compression of large files\n\n```python\nfrom slurm import scistorage\nfrom collections import namedtuple\n\nSensor = namedtuple("Sensor","x y z")\n\n# document sensor setting in this data file\ninfo = {\n    "TFmini": {\n        "min": 0.3,\n        "max": 12.0,\n        "fov_deg": 4.6,\n        "units": "m"\n    },\n    "LSM6DSOX": {\n        "accel": {\n            "range": (-4,4),\n            "units": "g"\n        },\n        "gyro": {\n            "range": (-2000,2000),\n            "units": "dps"\n        }\n    },\n    "LIS3MDL": {\n        "range": (-4,4), # 4 gauss = 400 uT\n        "units": "gauss"\n    },\n    "DPS310": {\n        "sensors": ("temperature", "pressure")\n    }\n}\n\ndata = [] # some data stored in an array or deque\nfor i in range(100):\n    data.append(Sensor(i,i,i)) # pretend you got some data from a sensor\n\n\nscistorage.write(info, data, "data.dil.gz") # *.gz uses gzip compression\n\nbag = scistorage.read("data.dil.gz")\nprint(bag["info"])\nprint(bag["data"])\n```\n\n## Network\n\n```python\nfrom slurm import network\n\nprint(network.get_ip()) # -> ip_address\nprint(network.host()) # -> (hostname, ip_address)\n```\n\n## Sleep Rate\n\nWill sleep for a prescribed amount of time inside of a loop\nirregardless of how long the loop takes\n\n```python\nfrom slurm import Rate\n\nrate = Rate(10)  # let loop run at 10 Hz\n\nwhile True:\n    # do some processing\n    rate.sleep()\n```\n\n## Files\n\n```python\nfrom slurm.files import rmdir, mkdir, run, rm, find\n\nmkdir("some/path")\nrmdir("some/path")\nrm("/path/file.txt")\nrm(["path/a.txt", "path/2/b.txt", "path/3/c.txt"])\n\nfind("/path/to/somewhere", "file_to_find") # -> list\nfind("/path/to/somewhere", "*.html") # -> list\n\nrun("ls -alh") # -> output\n```\n\n# MIT License\n\n**Copyright (c) 2014 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/slurm/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
