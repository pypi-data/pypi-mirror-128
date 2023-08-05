# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_fesion']

package_data = \
{'': ['*'],
 'streamlit_fesion': ['frontend/build/*', 'frontend/build/static/js/*']}

install_requires = \
['streamlit>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-fesion',
    'version': '0.1.0',
    'description': '',
    'long_description': 'streamlit-fesion\n===\n',
    'author': 'Yuichiro Tachibana (Tsuchiya)',
    'author_email': 't.yic.yt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whitphx/streamlit-webrtc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
