# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luga']

package_data = \
{'': ['*']}

install_requires = \
['fasttext>=0.9.2,<0.10.0', 'httpx>=0.20.0,<0.21.0', 'numpy>=1.21,<2.0']

setup_kwargs = {
    'name': 'luga',
    'version': '0.1.8',
    'description': 'Sensing the language of the text using Machine Learning',
    'long_description': 'Luga\n==============================\n- A blazing fast language detection using fastText\'s language models\n\n_Luga_ is a Swahili word for language. [fastText](https://github.com/facebookresearch/fastText) provides blazing-fast\nlanguage detection tool. Lamentably, [fastText\'s](https://fasttext.cc/docs/en/support.html) API is beauty-less and the documentation is a bit fuzzy.\nIt is also funky that we have to manually [download](https://fasttext.cc/docs/en/language-identification.html) and load models.\n\nHere is where _luga_ comes in. We abstract unnecessary steps and allow you to do precisely one thing: detecting text language.\n\n\n### Installation\n```bash\npython -m pip install -U luga\n```\n\n### Usage:\n⚠️ Note: The first usage downloads the model for you. It will take a bit longer to import depending on internet speed.\nIt is done only once.\n\n```python\nfrom luga import language\n\nprint(language("the world has ended yesterday"))\n\n# Language(name=\'en\', score=0.9804665446281433)\n```\n\n### Without Luga:\n\nDownload the model\n```bash\nwget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -O /tmp/lid.176.bin\n```\n\nLoad and use\n```python\nimport fasttext\n\nPATH_TO_MODEL = \'/tmp/lid.176.bin\'\nfmodel = fasttext.load_model(PATH_TO_MODEL)\nfmodel.predict(["the world has ended yesterday"])\n\n# ([[\'__label__en\']], [array([0.98046654], dtype=float32)])\n```\n### Comming soon ...\n\n\n### Dev:\n\n```bash\npoetry run pre-commit install\n```\n\n# Release Flow\n`git tag -l:` lists tags\n`git tag v*.*.*`\n`git push origin tag v*.*.*`\n\n# to delete tag:\n`git tag -d v*.*.* && git push origin tag -d v*.*.*`\n\n#### TODO:\n- [ ] refactor artifacts.py\n- [ ] auto checkers with pre-commit | invoke\n- [ ] write more tests\n- [ ] write github actions\n- [ ] create a smart data checker (a fast List[str], what do with none strings)\n- [ ] make it faster with Cython\n',
    'author': 'Prayson W. Daniel',
    'author_email': 'praysonwilfred@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Proteusiq/luga',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
