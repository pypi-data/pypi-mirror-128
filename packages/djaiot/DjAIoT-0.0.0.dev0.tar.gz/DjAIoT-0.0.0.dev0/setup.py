# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djaiot',
 'djaiot.device_data',
 'djaiot.device_data.migrations',
 'djaiot.device_data.models',
 'djaiot.device_data.scripts',
 'djaiot.device_health',
 'djaiot.device_health.migrations',
 'djaiot.device_health.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'djaiot',
    'version': '0.0.0.dev0',
    'description': 'Artificial Intelligence (AI) in Internet-of-Things Applications based on Django',
    'long_description': '# Artificial Intelligence (AI) in Internet-of-Things (IoT) Applications based on Django\n',
    'author': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/Django-AI/DjAIoT',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
