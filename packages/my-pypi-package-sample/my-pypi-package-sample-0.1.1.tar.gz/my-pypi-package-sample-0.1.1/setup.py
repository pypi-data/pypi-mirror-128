# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_pypi_package_sample']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['my-pypi-package-sample = my_pypi_package_sample:main']}

setup_kwargs = {
    'name': 'my-pypi-package-sample',
    'version': '0.1.1',
    'description': 'Print hello',
    'long_description': '# Package for PyPI\n\n#### 1. update codes\n\n#### 2. update the version\n\n```\npoetry version 0.1.2\n```\n\n#### 3. build\n\n```\npoetry build\n```\n\n#### 4. push to test pypi then test\n\n```\npoetry config repositories.testpypi https://test.pypi.org/legacy/\npoetry publish -r testpypi\n```\n\n#### 5. push to pypi then test\n\n```\npoetry publish\n```\n\n#### 6. test\n\n```\nmkdir exam-x && cd exam-x\npyenv local 3.9.5\npoetry init --no-interaction\npoetry install\npoetry shell\npoetry add hello-xxx\nvi exam.py\n    from hello_xxx import print_this, main\n    print_this()\npython exam.py\npoetry run hello-xxx\n```',
    'author': 'Hojung',
    'author_email': 'hojung_yun@yahoo.co.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://yahoo.com',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
