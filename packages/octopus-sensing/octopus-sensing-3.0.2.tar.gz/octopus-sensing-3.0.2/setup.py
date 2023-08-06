# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_sensing',
 'octopus_sensing.common',
 'octopus_sensing.devices',
 'octopus_sensing.devices.network_devices',
 'octopus_sensing.preprocessing',
 'octopus_sensing.questionnaire',
 'octopus_sensing.stimuli',
 'octopus_sensing.tests',
 'octopus_sensing.windows']

package_data = \
{'': ['*'],
 'octopus_sensing': ['OpenVibe/*'],
 'octopus_sensing.tests': ['data/preprocess_expected/OpenBCI_16_continuous/*',
                           'data/preprocess_expected/OpenBCI_16_sep/*',
                           'data/preprocess_expected/OpenBCI_8_continuous/*',
                           'data/preprocess_expected/OpenBCI_8_sep/*',
                           'data/preprocess_expected/Shimmer_continuous/gsr/*',
                           'data/preprocess_expected/Shimmer_continuous/ppg/*',
                           'data/preprocess_expected/Shimmer_sep/gsr/*',
                           'data/preprocess_expected/Shimmer_sep/ppg/*',
                           'data/recorded/OpenBCI_16_continuous/*',
                           'data/recorded/OpenBCI_16_sep/*',
                           'data/recorded/OpenBCI_8_continuous/*',
                           'data/recorded/OpenBCI_8_sep/*',
                           'data/recorded/Shimmer_continuous/*',
                           'data/recorded/Shimmer_sep/*']}

install_requires = \
['PyGObject==3.40.1',
 'bitstring>=3.1.7,<4.0.0',
 'brainflow>=4.6.1,<5.0.0',
 'heartpy>=1.2.7,<2.0.0',
 'miniaudio>=1.45,<2.0',
 'mne>=0.23.0,<0.24.0',
 'msgpack>=1.0.0,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pyOpenBCI>=0.13,<0.14',
 'pycairo>=1.20.1,<2.0.0',
 'pyserial>=3.4,<4.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.2,<2.0.0',
 'screeninfo>=0.7,<0.8',
 'sounddevice>=0.4.0,<0.5.0',
 'xmltodict>=0.12.0,<0.13.0']

extras_require = \
{':os_name != "nt"': ['bluepy>=1.3.0,<2.0.0', 'pyaudio>=0.2.11,<0.3.0']}

setup_kwargs = {
    'name': 'octopus-sensing',
    'version': '3.0.2',
    'description': 'Library for recording data synchronously from different physiological sensors',
    'long_description': 'Octopus Sensing\n===============\n\n![Travis status](https://img.shields.io/travis/com/nastaran62/octopus-sensing)\n![Coveralls status](https://img.shields.io/coveralls/github/nastaran62/octopus-sensing)\n![PyPI - Version](https://img.shields.io/pypi/v/octopus-sensing)\n![PyPI - License](https://img.shields.io/pypi/l/octopus-sensing)\n\n\nOctopus Sensing is a tool to help you run scientific experiments that involve recording data synchronously from\nmultiple sources in human-computer interaction studies. You write steps of an experiment scenario, for example showing a stimulus and then a questionnaire. The tool takes care of the rest.\n\nIt can collect data from multiple devices such as OpenBCI EEG headset, Shimmer sensor (GSR and PPG),\nVideo and Audio and so forth simultaneously. Data collection can be started and stopped synchronously across all devices.\nCollected data will be tagged with the timestamp of the start and stop of the experiment, the ID of\nthe experiment, etc.\n\nThe aim is to make the scripting interface so simple that people with minimum or no software\ndevelopment skills can define experiment scenarios with no effort. \nAlso, this tool can be used as the base structure for creating real-time data processing systems like systems with capabilities of recognizing emotions, stress, cognitive load, or analyzing human behaviors.\n\n\n**To see the full documentation go to [Otopus Sensing](https://octopus-sensing.nastaran-saffar.me/) website.**\n\nMain features\n--------------\n\n* Controls data recording from multiple sources using a simple unified interface\n* Tags an event on collected data, such as the start of an experiment, and events during the experiment, etc.\n* Can show stimuli (images and videos) and questionnaires\n* Monitoring interface that visualizes collected data in real-time\n* Offline visualization of data from multiple sources simultanously\n\nCopyright\n---------\nCopyright © 2020 Nastaran Saffaryazdi, Aidin Gharibnavaz\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU\nGeneral Public License as published by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nSee [License file](https://github.com/nastaran62/octopus-sensing/blob/master/LICENSE) for full terms.\n',
    'author': 'Nastaran Saffaryazdi',
    'author_email': 'nsaffar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://octopus-sensing.nastaran-saffar.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
