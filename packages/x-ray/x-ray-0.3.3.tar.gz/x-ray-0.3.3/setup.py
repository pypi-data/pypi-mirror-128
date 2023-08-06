# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xray']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF==1.19.2', 'requests>=2.26.0,<3.0.0', 'types-requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['xray = xray.__init__:cli']}

setup_kwargs = {
    'name': 'x-ray',
    'version': '0.3.3',
    'description': 'A library and microservice to find bad redactions in PDFs',
    'long_description': '![Image of REDACTED STAMP](https://raw.githubusercontent.com/freelawproject/x-ray/main/redacted.png)\n\nx-ray is a Python library for finding bad redactions in PDF documents.\n\n## Why?\n\nAt Free Law Project, we collect millions of PDFs. An ongoing problem\nis that people fail to properly redact things. Instead of doing it the right\nway, they just draw a black rectangle or a black highlight on top of black\ntext and call it a day. Well, when that happens you just select the text under\nthe rectangle, and you can read it again. Not great.\n\nAfter witnessing this problem for years, we decided it would be good to figure\nout how common it is, so, with some help, we built this simple tool. You give\nthe tool the path to a PDF. It tells you if it has worthless redactions in it.\n\n\n## What next?\n\nRight now, `x-ray` works pretty well and we are using it to analyze documents\nin our collections. It could be better though. Bad redactions take many forms.\nSee the issues tab for other examples we don\'t yet support. We\'d love your\nhelp solving some of tougher cases.\n\n\n## Installation\n\nWith poetry, do:\n\n```text\npoetry add x-ray\n```\n\nWith pip, that\'d be:\n```text\npip install x-ray\n```\n\n## Usage\n\nYou can easily use this on the command line. Once installed, just:\n\n```bash\n% xray path/to/your/file.pdf\n{\n  "1": [\n    {\n      "bbox": [\n        58.550079345703125,\n        72.19873046875,\n        75.65007781982422,\n        739.3987426757812\n      ],\n      "text": "The Ring travels by way of Cirith Ungol"\n    }\n  ]\n}\n```\n\nOr if you have hte file on a server somewhere, give it a URL. If it starts\nwith `https://`, it will be interpreted as a PDF to download:\n\n```bash\n% xray https://free.law/pdf/congressional-testimony-michael-lissner-free-law-project-hearing-on-ethics-and-transparency-2021-10-26.pdf\n{}\n```\n\nA fun trick you can now do is to make a file with one URL per line, call it `urls.txt`. Then you can run this to check each URL:\n\n```bash\nxargs -n 1 xray  < urls.txt\n```\n\nHowever you run `xray` on the command line, you\'ll get JSON as output. When you have that, you can use it with tools like [`jq`][jq]. The format is as follows:\n\n - It\'s a dict.\n - The keys are page numbers.\n - Each page number maps to a list of dicts.\n - Each of those dicts maps to two keys.\n - The first key is `bbox`. This is a four-tuple that indicates the x,y positions of the upper left corner and then lower right corners of the bad redaction.\n - The second key is `text`. This is the text under the bad rectangle.\n\nSimple enough.\n\nYou can also use it as a Python module, if you prefer the long-form:\n\n```\n% pathon -m xray some-file.pdf\n```\n\nBut that\'s not as easy to remember.\n\nIf you want a bit more, you can, of course, use `xray` in Python:\n\n```python\nfrom pprint import pprint\nimport xray\nbad_redactions = xray.inspect("some/path/to/your/file.pdf")  # Pathlib works too\npprint(bad_redactions)\n{1: [{\'bbox\': (58.550079345703125,\n               72.19873046875,\n               75.65007781982422,\n               739.3987426757812),\n      \'text\': \'Aragorn is the one true king.\'}]}\n```\n\nThe output is the same as above, except it\'s a Python object, not a JSON object.\n\nIf you already have the file contents as a `bytes` object, that\'ll work too:\n\n```python\nsome_bytes = requests.get("https://lotr-secrets.com/some-doc.pdf").content\nbad_redactions = xray.inspect(some_bytes)\n```\n\nNote that because the `inspect` method uses the same signature no matter what,\nthe type of the object you give it is essential:\n\nInput | `xray`\'s Assumption\n-- | --\n`str` or Pathlib `Path` | local file\n`str` that starts with `https://` | URL to download\n`bytes` | PDF in memory\n\nThis means that if you provide the filename on disk as a bytes object instead\nof a `str`, it\'s not going to work. This will fail:\n\n```python\nxray.inspect(b"some-file-path.pdf")\n```\n\nThat\'s pretty much it. There are no configuration files or other variables to\nlearn. You give it a file name. If there is a bad redaction in it, you\'ll soon\nfind out.\n\n\n## How it works\n\nUnder the covers, `xray` uses the high-performant [PyMuPDF project][mu] to parse PDFs. It has been a wonderful project to work with.\n\nYou can read the source to see how it works, but the general idea is to:\n\n1. Find rectangles in a PDF.\n\n2. Find letters in the same location\n\n3. Render the rectangle\n\n4. Inspect the rectangle to see if it\'s all one color\n\nThe PDF format is a big and complicated one, so it\'s difficult to do all this l and perfectly. We do our best, but there\'s always more to do to make it better. Donations and sponsored work help.\n\n## Contributions\n\nPlease see the issues list on Github for things we need, or start a conversation if you have questions. Before you do your first contribution, we\'ll need a signed contributor license agreement. See the template in the repo.\n\n\n## Deployment\n\nReleases happen automatically via Github Actions. To trigger an automated build:\n\n1. Update the version in pyproject.toml\n\n2. Tag the commit with something like "v0.0.0".\n\n\nIf you wish to create a new version manually, the process is:\n\n1. Update version info in `pyproject.toml`\n\n2. Configure your Pypi credentials [with Poetry][creds]\n\n3. Build and publish the version:\n\n```sh\npoetry publish --build\n```\n\n\n\n## License\n\nThis repository is available under the permissive BSD license, making it easy and safe to incorporate in your own libraries.\n\nPull and feature requests welcome. Online editing in GitHub is possible (and easy!).\n\n[jq]: https://stedolan.github.io/jq/\n[mu]: https://pymupdf.readthedocs.io/\n[asc]: https://en.wikipedia.org/wiki/Ascender_(typography)\n[creds]: https://python-poetry.org/docs/repositories/#configuring-credentials\n',
    'author': 'Free Law Project',
    'author_email': 'info@free.law',
    'maintainer': 'Free Law Project',
    'maintainer_email': 'info@free.law',
    'url': 'https://github.com/freelawproject/pdf-redaction-detector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
