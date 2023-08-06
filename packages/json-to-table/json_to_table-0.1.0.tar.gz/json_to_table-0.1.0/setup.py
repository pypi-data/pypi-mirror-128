# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json_to_table']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'typer>=0.4.0,<0.5.0',
 'xlwt>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['j2t = json_to_table.__main__:main']}

setup_kwargs = {
    'name': 'json-to-table',
    'version': '0.1.0',
    'description': 'Convert Json File to CSV(XLSX)',
    'long_description': '# JSON-TO-Table\n\nConvert JSON File to CSV or XLSX File.\n\n## Installation\n\nInstall JSON-TO-Table using pip:\n\n```bash\npip install json-to-table\n```\n\n## Usage/Examples\n\n```bash\n# Show Header\n$ j2t head data/example.json --n 5\n    name  age  married\n0   Mike   18     True\n1    Tom   25    False\n2   Jane   20     True\n3    Bob   30    False\n4  Alice   22     True\n# Convert JSON to CSV\n$ j2t convert data/example.json\n# Convert JSON to XLSX\n$ j2t convert data/example.json --t xlsx\n```\n\n## Authors\n\n- [@duyixian1234](https://www.github.com/duyixian1234)\n',
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/duyixian1234/json2table',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
