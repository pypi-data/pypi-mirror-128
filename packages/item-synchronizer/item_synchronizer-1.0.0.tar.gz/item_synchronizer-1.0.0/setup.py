# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['item_synchronizer']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.21.4,<0.22.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'item-synchronizer',
    'version': '1.0.0',
    'description': 'Synchronize items between two different sources',
    'long_description': '# Items Synchronizer\n\n## Description\n\nTODO Add a diagram to explain it.\n\nSynchronize items from two different sources.\n\nThis library aims to offer an abstract and versatile way to _create_, _update_\nand/or _delete_ items to keep two "sources" in bi-directional sync.\n\nThese "items" may range from Calendar entries, TODO task lists, or whatever else\nyou want as long as the user registers the appropriate functions/methods to\nconvert from one said item to another.\n\n## Installation\n\nAdd it as a dependency to either your `requirements.txt` or to `pyproject.toml`\n\nTODO - Add example\n\n## Example Usage\n\nProjects using this:\n\n* [Taskwarrior <-> Google Calendar Bidirectonal Synchronisation](https://github.com/bergercookie/taskw_gcal_sync/blob/master/taskw_gcal_sync/TWGCalAggregator.py)\n\n<!-- ## TODO Extra Configuration -->\n',
    'author': 'Nikos Koukis',
    'author_email': 'nickkouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bergercookie/item_synchronizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
