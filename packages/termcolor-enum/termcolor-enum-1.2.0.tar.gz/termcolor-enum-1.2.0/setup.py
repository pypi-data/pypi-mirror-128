# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termcolor_enum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termcolor-enum',
    'version': '1.2.0',
    'description': 'Drop-in [termcolor](https://pypi.org/project/termcolor/) replacement with enums and type hinting',
    'long_description': '# Examples\n\n```python\nimport sys\nfrom termcolor_enum import *\n\ntext = colored(\'Hello, World!\', Colors.RED, attrs=[Attributes.REVERSE, Attributes.BLINK])\nprint(text)\ncprint(\'Hello, World!\', \'green\', Highlights.ON_RED)\n\nprint_red_on_cyan = lambda x: cprint(x, \'red\', \'on_cyan\')\nprint_red_on_cyan(\'Hello, World!\')\nprint_red_on_cyan(\'Hello, Universe!\')\n\nfor i in range(10):\n    cprint(i, \'magenta\', end=\' \')\n\ncprint("Attention!", \'red\', attrs=[\'bold\'], file=sys.stderr)\n```\n\n# Text Colors (`termcolor_enum.Colors`):\n\n| Color   | String      | Enum Value |\n| ------- | ----------- | ---------- |\n| Grey    | `\'grey\'`    | `GREY`     |\n| Red     | `\'red\'`     | `RED`      |\n| Green   | `\'green\'`   | `GREEN`    |\n| Yellow  | `\'yellow\'`  | `YELLOW`   |\n| Blue    | `\'blue\'`    | `BLUE`     |\n| Magenta | `\'magenta\'` | `MAGENTA`  |\n| Cyan    | `\'cyan\'`    | `CYAN`     |\n| White   | `\'white\'`   | `WHITE`    |\n\n# Text Highlights (`termcolor_enum.Highlights`):\n\n| Highlight  | String         | Enum Value   |\n| ---------- | -------------- | ------------ |\n| On Grey    | `\'on_grey\'`    | `ON_GREY`    |\n| On Red     | `\'on_red\'`     | `ON_RED`     |\n| On Green   | `\'on_green\'`   | `ON_GREEN`   |\n| On Yellow  | `\'on_yellow\'`  | `ON_YELLOW`  |\n| On Blue    | `\'on_blue\'`    | `ON_BLUE`    |\n| On Magenta | `\'on_magenta\'` | `ON_MAGENTA` |\n| On Cyan    | `\'on_cyan\'`    | `ON_CYAN`    |\n| On White   | `\'on_white\'`   | `ON_WHITE`   |\n\n# Text Attributes (`termcolor_enum.Attributes`):\n\n| Attribute | String        | Enum Value  |\n| --------- | ------------- | ----------- |\n| Bold      | `\'bold\'`      | `BOLD`      |\n| Dark      | `\'dark\'`      | `DARK`      |\n| Underline | `\'underline\'` | `UNDERLINE` |\n| Blink     | `\'blink\'`     | `BLINK`     |\n| Reverse   | `\'reverse\'`   | `REVERSE`   |\n| Concealed | `\'concealed\'` | `CONCEALED` |\n\n# Terminal Compatibility\n\n| Terminal     | Bold    | Dark | Underline | Blink      | Reverse | Concealed |\n| ------------ | ------- | ---- | --------- | ---------- | ------- | --------- |\n| xterm        | yes     | no   | yes       | bold       | yes     | yes       |\n| linux        | yes     | yes  | bold      | yes        | yes     | no        |\n| rxvt         | yes     | no   | yes       | bold/black | yes     | no        |\n| dtterm       | yes     | yes  | yes       | reverse    | yes     | yes       |\n| teraterm     | reverse | no   | yes       | rev/red    | yes     | no        |\n| aixterm      | normal  | no   | yes       | no         | yes     | yes       |\n| PuTTY        | color   | no   | yes       | no         | yes     | no        |\n| Windows      | no      | no   | no        | no         | yes     | no        |\n| Cygwin SSH   | yes     | no   | color     | color      | color   | yes       |\n| Mac Terminal | yes     | no   | yes       | yes        | yes     | yes       |\n',
    'author': 'aidan',
    'author_email': 'achaplin3@gatech.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/TheBicameralMind/termcolor-enum',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
