# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obplatform']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'pandas': ['pandas>=1.3.4,<2.0.0']}

setup_kwargs = {
    'name': 'obplatform',
    'version': '0.1.3',
    'description': 'APIs to access ASHRAE OB Database',
    'long_description': '# OBPlatform\n\nA package to interact and download behavior data from [ASHRAE Global Occupant Behavior Database](https://ashraeobdatabase.com). Currently available on PyPI. More features coming in the furture.\n\n[![pypi](https://img.shields.io/pypi/v/obplatform.svg)](https://pypi.python.org/pypi/obplatform) [![CI](https://github.com/umonaca/obplatform/actions/workflows/test.yml/badge.svg?event=push)](https://github.com/umonaca/obplatform/actions?query=event%3Apush+branch%3Amaster) [![codecov](https://codecov.io/gh/umonaca/obplatform/branch/master/graph/badge.svg?token=SCFFFX2IKX)](https://codecov.io/gh/umonaca/obplatform) ![license](https://img.shields.io/github/license/umonaca/obplatform) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/obplatform) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![Read the Docs](https://img.shields.io/readthedocs/obplatform)\n\n## Installation\n\n### poetry\n\n```\npoetry install\n```\n\n### pip\n\n```\npip install obplatform\n```\n\n### conda\n\nWe are going to submit the package to `conda-forge`. It requires manual review process from Anaconda.\n\n## Features\n\n- List all behavior types available in the database.\n- Download data archive (ZIP file) based on behavior type and study id inputs (with progress bar).\n- Query studies based on (behaviors, countries, cities, (building type + room type)) (WIP).\n- Query available behavior types based on study ids (WIP)\n\n## Example\n\n```python\nimport logging\nimport zipfile\n\nimport pandas as pd\nfrom obplatform import Connector, logger\n\nconnector = Connector()\n\n# List all behaviors available in the database\nprint(connector.list_behaviors())\n\n# Print progress information\n# Comment out the following line to hide progress information\nlogger.setLevel(logging.INFO)\n\n# Download Appliance Usage + Occupant Presence behaviors from study 22, 11, and 2.\nconnector.download_export(\n    "data.zip",\n    ["Appliance_Usage", "Occupancy"],\n    ["22", "11", "2"],\n    show_progress_bar=True,  # False to disable progrees bar\n)\n\nbehavior_type = "Appliance_Usage"\nstudy_id = "22"\n\nzf = zipfile.ZipFile("data.zip")\ndf = pd.read_csv(zf.open(f"{behavior_type}_Study{study_id}.csv"))\nprint(df.head())\n```\n\n## Usage\n\n### Available behavior types\n\nPlease only use the following names as input. e.g. Please use `Lighting_Status` (listed below) instead of  `Lighting Adjustment`(displayed on the website).\n\n```\n\'Appliance_Usage\', \'Fan_Status\', \'Door_Status\', \'HVAC_Measurement\', \'Lighting_Status\', \'Occupant_Number\', \'Occupancy\', \'Other_HeatWave\', \'Other_Role of habits in consumption\', \'Other_IAQ in Affordable Housing\', \'Shading_Status\', \'Window_Status\'\n```\n\nIn the next version, the package will auto detect either type of input and convert to the correct query parameter.\n\n### Note: big data\n\nStudy 2 is a special case. It has very large source files (> 2 GB) so we compressed all data in study 2 as a single `.tar.gz`file. In the example above, `data.zip` contains a `tar.gz`file along with several separate csv files from other studies. When writing libraries to read from csv file from the downloaded zip, Study 2 should be treated as a special case.\n\n## Changelog\n\n- 2021-11-18:  Release 0.1.3\n\n## TODO\n\n- Add function to query available studies based on (behaviors, countries, cities, (building type + room type)) \n- Add function to query available behavior types based on study ids\n- Auto detect and convert behavior type inputs to correct query parameters for web API\n- Fix naming inconsistencies on the server side (Occupancy Presence on the website, Occupancy_Measurement in file name, Occupancy in API key field)\n\n## API Reference\n\nhttps://obplatform.readthedocs.io/en/latest/index.html\n\n',
    'author': 'Wei Mu',
    'author_email': 'wmu100@syr.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
