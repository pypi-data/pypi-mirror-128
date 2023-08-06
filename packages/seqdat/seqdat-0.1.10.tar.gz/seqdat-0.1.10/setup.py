# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqdat']

package_data = \
{'': ['*']}

install_requires = \
['click-rich-help>=0.2.0,<0.3.0',
 'click>=8.0.3,<9.0.0',
 'rich>=10.12.0,<11.0.0',
 'ruamel.yaml>=0.17.17,<0.18.0']

entry_points = \
{'console_scripts': ['seqdat = seqdat.cli:main']}

setup_kwargs = {
    'name': 'seqdat',
    'version': '0.1.10',
    'description': 'sequencing data manager',
    'long_description': '# SEQDAT\n\n**Seq**uencing **Dat**a Manager\n\n## Usage\n\nSee [docs](docs/usage.md) for more info. Also view available commands with `--help`.\n\n```bash\nseqdat --help\n```\n\n## Development\n\nTo make changes to seqdat generate a new conda enviroment and install dependencies with poetry.\n\n```bash\ngit clone git@github.com:daylinmorgan/seqdat.git\ncd seqdat\nmamba create -n seqdatdev python=3.7 poetry\npoetry install\n```\n\n`Black`, `isort` and `flake8` are applied via `pre-commit`, additionally type checking should be enforced with `mypy seqdat`.\n\nAfter making some changes you can build a local executable using `pyinstaller`.\n\n```bash\n./build.sh\n```\n\nIf pyinstaller completes successfully the executable will be in `dist/`\n',
    'author': 'Daylin Morgan',
    'author_email': 'daylinmorgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daylinmorgan/seqdat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
