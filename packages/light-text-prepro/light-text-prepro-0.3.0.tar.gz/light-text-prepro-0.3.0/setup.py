# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['light_text_prepro']

package_data = \
{'': ['*'], 'light_text_prepro': ['rules/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'flake8>=3.9.1,<4.0.0']

setup_kwargs = {
    'name': 'light-text-prepro',
    'version': '0.3.0',
    'description': 'Light Text Pre-processing permits to apply a chain of built-in regex rules to a input string.',
    'long_description': '# Light Text Pre-processing\n\n`Light Text Pre-processing` is an easy-to-use python module that permits to apply a chain of built-in regex rules to a input string. Regex rules are stored in a separate YML file and compiled at run-time. The compiling mechanism and how to add a custom regex are described below.\n\n![ci/cd](https://github.com/Arfius/light-text-prepro/actions/workflows/light-text-prepro.yml/badge.svg)\n\n## How it works\n\nPackage reads a list of regex from `light_text_prepro/rules/regex.yml`.  Each row in `regex.yml` identifies a regex rule such as `user_tag: \'"@[0-9a-z](\\.?[0-9a-z])*"\'`. In this row, `user_tag` is the `key` of the regex, whereas the `\'"@[0-9a-z](\\.?[0-9a-z])*"\'`is its `value`.\n\nAt run-time, the package reads the `regex.yml` and compiles a method for each regex, the method is named as the the `key` of the row. For example, at the end of the process, you will be able to call the `user_tag()`method, that permit to match the user tagged. Each method has the optional parameter `replace_with` that allow you to replace the string matched by regex rule with an arbitrary text.\n\n## Package installation\n\n### List of Regex \n```yaml\nuser_tag: \'"@[0-9a-z](\\.?[0-9a-z])*"\'\nemail: \'"^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,6})$"\'\nurl: \'"(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]+\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]+\\.[^\\s]{2,})"\'\nspecial_chars: \'"[-!$%^&*()_+|~=`{}<>?,.\\"\\[\\]:;/\\\\]"\'\nip_address: \'"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"\'\nhtml_tag: \'"^<([a-z]+)([^<]+)*(?:>(.*)<\\/\\1>|\\s+\\/>)$"\'\ntab_new_line: \'"(\\n|\\t|\\r)"\'\nmultiple_space: \'"[ ]+"\'\n```\n\nIf you are happy wiht the list above, you can install the package via pip.\n\n```\npip install light-text-prepro\n```\n\n## How to use\n\n```python\nfrom light_text_prepro.lprepro import LPrePro\n...\nobj = LPrePro()\n...\nresult = obj.set_text(\'Hey @username, this is my email my@email.com\') \\\n\t\t .user_tag(replace_with=\'[user]\') \\\n\t\t .email(replace_with=\'[email]\') \\\n    \t.get_text()\n# result -> Hey [user], this is my email [email]\n```\n\n\nOtherwise, if you want to contribute to enrich the package adding your regex rule, please follow section below.\n\n## How to add a regex rules\n\n### Setup project\n\n````\n$> git clone https://github.com/Arfius/light-text-prepro.git\n$> cd light-text-prepro\n$> pip install poetry flake8\n$> poetry install\n````\n\n### Add  new regex\n\n1. Open `light_text_prepro/rules/regex.yml` and add a new row. Make sure to use a unique key for the rule. If  you get issue adding the regex rule, use any online regex validation tool and export the regex rule for python. (i.e. https://regex101.com/ => FLAVOR python => Copy to clipboard )\n2. Add a `unit tests` under the  `tests` folder and make all test passed.  Use`$> poetry run pytest` to run unit tests.\n3. Update the  section `List of Regex` at the end of this file.\n4. Create a Pull Request\n\n\n',
    'author': 'Alfonso Farruggia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arfius/light-text-prepro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
