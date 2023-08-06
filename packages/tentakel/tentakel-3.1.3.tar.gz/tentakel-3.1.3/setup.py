# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tentakel', 'tentakel.plugins']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tentakel = tentakel.main:main']}

setup_kwargs = {
    'name': 'tentakel',
    'version': '3.1.3',
    'description': 'distributed command execution',
    'long_description': 'About\n=====\n\nTentakel is a program for executing the same command on many hosts in parallel\nusing various remote methods. It can make use of several sets of hosts that are\ndefined in a configuration file as groups.\n\nIt also supports an interactive mode that can be used for repeated commands.\n\nThe author uses tentakel to simultaneously install software on many\nworkstations or ask and set parameters on a linux compute cluster.  With the\npower of format strings tentakel can also be used for monitoring purposes.\n\nSupported remote methods are ssh(1) and rsh(1).  Both must be configured to\nallow for password-less logins. Password-protected keyfiles for ssh can be\nused with ssh-agent(1).\n\nA plugin mechanism allows users to implement their own remote methods in\naddition to the builtin ones.\n\nFor more information on available options please refer to the manpage\ntentakel(1).\n\nThe project homepage is: <https://github.com/sfermigier/tentakel>\n\nThe current maintainer is:\n\n- Stefane Fermigier <sf@fermigier.com>\n\nThe original authors were:\n\n- Sebastian Stark <cran@users.sourceforge.net>\n- Marlon Berlin <imaginat@users.sourceforge.net>\n\nThis software contains the Toy Parser Generator (tpg.py)\nwritten by Christophe Delord.\n',
    'author': 'Sebastian Stark, Marlon Berlin',
    'author_email': 'cran@users.sourceforge.net, imaginat@users.sourceforge.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sfermigier/tentakel',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
