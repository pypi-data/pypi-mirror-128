# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memrise', 'memrise.data', 'memrise.extract', 'memrise.googletrans']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'memrise',
    'version': '1.2.0rc5',
    'description': 'Scraping the vocabulary from the Memrise course',
    'long_description': '<p align="center">\n    <img src="https://raw.githubusercontent.com/tquangsdh20/memrise/main/.github/memrise.svg">\n</p>\n\n<p align="center"> \n    <img src="https://img.shields.io/github/license/tquangsdh20/memrise"> <img src = "https://img.shields.io/bitbucket/issues-raw/tquangsdh20/memrise"> <img src = "https://img.shields.io/pypi/pyversions/memrise"> <img src="https://img.shields.io/pypi/implementation/memrise"> <img src="https://img.shields.io/github/last-commit/tquangsdh20/memrise">\n</p>\n\n## Features:\n- Support scraping the courses in MEM to take the vocabulary\n\n## Appplication Requires\n\n### Install DB Browser : [SQLite](https://sqlitebrowser.org/dl/)\n\n### Install Library: \n<b>Window</b>\n```\n python -m pip install memrise\n```\n<b>Linux</b>\n  ```\n  pip install memrise\n  ```\n <b>macOS</b>\n ```\n sudo pip3 install memrise\n```\n## Guidelines\n\n### How to take Course ID?\n\nAccess the Website: [Memrise](https://app.memrise.com/course/) and copy the Course ID as the following picture:\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/tquangsdh20/memrise/main/.github/CourseID.PNG">\n</p>\n\n### Import library and initialize database\n\n```python\nfrom memrise import Course, Data\n#Create file database output\ndb = Data(\'English.sqlite\') #Other format is .db\n#Connect to file database and init\ndb.init_database()\n```\n\n### Scraping course with ID\n\nRegarding to Module Course with two paramemters:\n- `CourseID`: Get the Course ID as above\n- `LanguageID`: The Language ID of the Course which you study.\n\nWhere, the LanguageID is define as the followings:\nThe output will give you the List Language\'s ID of the Course, remember the ID for next step. \n\n```\nLanguage IDs:        \n    1. English UK    \n    2. English US    \n    3. Chinese       \n    4. Janpanese     \n    5. French        \n    6. Spanish Mexico\n    7. Italian\n    8. German\n    9. Russian\n    10. Dutch\n    11. Korean\n    12. Arabic\n    13. Spanish Spain\n\n```\n\nThe following example is scraping the English course for Vietnamese with IPA of English US, so the Language ID is 2.\n```python\n#Connect the course to scraping info this maybe take a few momment.\ncourse = Course(1658724,2)\n#Update information about the course\ndb.update_course(course)\n```\n\n### Update course with your language meaning\n\nUse the method `update_db_en()` if the LANGUAGE COURSE is **English** for scraping IPA.  \nUse the method `update_db()` if the Language Course is the others.  \nAbout the parameters of two above methods are the same:  \n- `CourseID` : the ID of the course\n- `Language` : your mother language with format <i>\'en\', \'fr\', \'ko\', \'vi\'...</i>\n\n```python\n#If your Course is English language use `update_db_en()`, otherwise use `update_db()` method.\ndb.update_db_en(1658724,\'fr\')\n```\n### Check the output with SQLite\n\nFile output\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/tquangsdh20/memrise/main/.github/OUTPUT.PNG" height=200 width=600 />\n</p>\n\nShow the words table as the following steps: **Browse Data > Table > Word**\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/tquangsdh20/memrise/main/.github/OUTPUT2.PNG" height=500 width=800>\n</p>\n\nIf you want to choose the raw meaning, you could run the following SQL statement.\n\n```SQL\nSELECT word, sub, IPA FROM words\n```\nSteps : **Execute SQL > Typing SQL Statements > Run**\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/tquangsdh20/memrise/main/.github/OUTPUT3.PNG" height=500 width=800>\n</p>\n\n[<b>Github:</b> https://github.com/tquangsdh20/memrise](https://github.com/tquangsdh20/memrise)\n\n### Log changes:\n\n**v1.0.0**: Implementation Scrapping Vocabulary  \n**v1.1.0**: Update IPA Function   \n**v1.2.0** : Update new TRANSLATE FUNCTION  \n',
    'author': 'Joseph Quang',
    'author_email': 'tquangsdh20@hcmut.edu.vn',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tquangsdh20/memrise',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
