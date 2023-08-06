# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aqstat', 'aqstat.cli', 'aqstat.cli.commands', 'aqstat.scripts']

package_data = \
{'': ['*'], 'aqstat': ['locales/*', 'locales/hu/LC_MESSAGES/*']}

install_requires = \
['asks>=2.4.12,<3.0.0',
 'click-option-group>=0.5.2,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'trio>=0.18.0,<0.19.0']

entry_points = \
{'console_scripts': ['aqstat = aqstat.cli.main:start']}

setup_kwargs = {
    'name': 'aqstat',
    'version': '1.0.1',
    'description': 'Toolset for visualizing Air Quality Data from https://sensor.community',
    'long_description': '# AQStat\n\n`aqstat` is a command line Python tool for visualizing air quality data collected under the [luftdaten.info](https://luftdaten.info/) project.\n\n# Install\n\n`aqstat` is written in Python, so installation and usage is platform-independent.\n\n## Requirements\n\n* Install git\n* Get Python 3.7 or later\n* If you need the latest development version or you wish to modify the code, install [Poetry](https://python-poetry.org/docs/#installation) as well.\n\n## Install latest release from PyPI\n\nThe latest release is hosted at the [Python Package Index (PyPI) ](https://pypi.org/project/aqstat). To install `aqstat` from there, simply run:\n\n```\npip install aqstat\n```\n\n## Install latest source from GitHub\n\nThe latest development code is available at [GitHub](https://github.com/vasarhelyi/aqstat). Installation should be as simple as running the following:\n\n```\ngit clone https://github.com/vasarhelyi/aqstat.git\ncd aqstat\npoetry install\n```\n\nAs `aqstat` uses Poetry, all Python package dependencies will be installed automatically in a local virtual environment under `.venv` in the project folder.\n\n# Usage\n\n## Basic usage\n\nRun `aqstat --help` to get a quick overview on the usage of `aqstat`. There are three basic commands currently available:\n\n  * `download` helps you retreive air quality sensor data from the net to your local computer for later analysis\n  * `plot` lets you visualize air quality data of selected sensors\n  * `stat` generates various statistical outputs for selected sensors\n\nAn additional `test` command is provided as a development section to test different work-in-progress stuff.\n\nMore detailed help on individual commands is also available. For example, run `aqstat download --help` to get help on data download options.\n\nTo get some examples on usage, check out the `doc\\examples\\commands.md` file.\n\n## Usage with Poetry\n\nTo execute `aqstat` using Poetry, type `poetry run aqstat` from the cloned project folder.\n\n\n## Sensor database\n\nLocal sensor data is stored in folders named after sensor IDs. There are two basic data sources supported currently, a bit of a problem is that they use different IDs for different sensors (madavi.de uses a single `chip_id`, sensor.community uses a `sensor_id` for all sensors in a given measurement unit. Furthermore, these two sources store slightly different information about the sensors.\n\nTo obtain a general easy-to-use reference for all sensor data, a local description of all sensors can be given optionally. A simple JSON format is used for that, please check out the `doc\\examples\\metadata.json` file as an example how to fill the JSON form for a single sensor, or use the `scripts\\convert_luftdaten_csv_to_metadata_json.py` script to generate .json files from the sensor data directly.\n\nThe overall sensor database structure should look like something like this:\n\n```\n12345/\n67890/\nBudapest-12345.json\nVerőce-67890.json\n```\n\nThe name of the `.json` files is arbitrary, it is useful to include human readable information, such as the location of the sensor, as in the example above.\n\nLater on, during the usage of the `plot` and `stat` commands, filters can be defined and several outputs can be generated based on various properties given in the .json files.\n\n# Contact and collaboration\n\n`aqstat` is made public and open-source to help each other in fighting air pollution. Please [contact](mailto:vasarhelyi@hal.elte.hu) if you have any questions on usage, something is not working properly, you have new ideas or feature requests or if you would like to help in development or collaboration or wish to support the project in any way.\n\n',
    'author': 'Gabor Vasarhelyi',
    'author_email': 'vasarhelyi@hal.elte.hu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vasarhelyi/aqstat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
