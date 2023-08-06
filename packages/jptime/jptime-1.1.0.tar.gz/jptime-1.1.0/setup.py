# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jptime']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['japanese-number-converter==1.0.1', 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'jptime',
    'version': '1.1.0',
    'description': 'handle japanese time format',
    'long_description': '# jptime\n\njptime handle japanese time format.\n\n## Installation\n\n```sh\npip install jptime\n```\n\n## Usage\n\n```py\nfrom datetime import datetime\nimport jptime\n\n# from string\njpt = jptime.from_str("平成元年三月三日")\nassert jpt.to_tuple() == (4, 1, 3, 3)\nassert jpt.to_datetime() == datetime(1989, 3, 3)\n\n# from datetime\njpt = jptime.from_datetime(datetime(2019, 5, 1))\nassert jpt.to_tuple() == (5, 1, 5, 1) # 令和1年5月1日\n```\n\n## Supported formats\n\n- japanese era\n  - era_symbol/yy/mm/dd (allow kanji number)\n    (e.g. 昭和5年3月3日)\n  - era_code + yymmdd\n    (e.g. 3031123, H040323)\n- christian era (delegate to dateutil.parser)\n  (e.g. 19920323, 2018-12-12, 2018年8月13日)\n',
    'author': 'kitagawa-hr',
    'author_email': 'kitagawahr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kitagawa-hr/jptime',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
