# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slapd']

package_data = \
{'': ['*'], 'slapd': ['certs/*']}

extras_require = \
{'doc': ['recommonmark', 'sphinx', 'sphinx-rtd-theme', 'sphinx-issues']}

setup_kwargs = {
    'name': 'slapd',
    'version': '0.1.2',
    'description': 'Controls a slapd process in a pythonic way',
    'long_description': '# python-slapd [![Documentation Status](https://readthedocs.org/projects/slapd/badge/?version=latest)](https://slapd.readthedocs.io/en/latest/?badge=latest)\nControls your OpenLDAP process in a pythonic way.\n\n```\npip install slapd\n```\n\n```python\n>>> import slapd\n>>> process = slapd.Slapd()\n>>> process.start()\n>>> process.ldapwhoami().stdout.decode("utf-8")\n\'dn:cn=manager,dc=slapd-test,dc=python-ldap,dc=org\\n\'\n>>> process.stop()\n```\n\n# Troubleshooting\n\nOn distributions like Ubuntu, apparmor may restrict *slapd* to access some files that\n*python-slapd* has generated. This situation can be solved by passing slapd in complain mode:\n\n```bash\nsudo apt install --yes apparmor-utils\nsudo aa-complain /usr/sbin/slapd\n```\n',
    'author': 'python-ldap team',
    'author_email': 'python-ldap@python.org',
    'maintainer': 'Éloi Rivard',
    'maintainer_email': 'eloi.rivard@aquilenet.fr',
    'url': 'https://slapd.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
