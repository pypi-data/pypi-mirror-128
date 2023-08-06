# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ActiveList']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0', 'tomlkit>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'active-list-mc',
    'version': '0.1',
    'description': 'Facade to simplify usage of Gtk.TreeView with Gtk.ListStore model',
    'long_description': 'This module is a Facade to simplify usage of the\nGtk.TreeView with Gtk.ListStore model.\n\nThe module creates the ListStore model and initialises it\nwith the required columns and cell renderers.\n\nThe information as to the required columns and cell renderers\nis specified as a list of tuples in the calling module.\n',
    'author': 'Chris Brown',
    'author_email': 'chris@marcrisoft.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
