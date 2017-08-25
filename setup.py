try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'Diigo to Zotero Citation Converter',
	'version': '0.1',
	'url': 'https://github.com/parnellj/diigo_to_zotero',
	'download_url': 'https://github.com/parnellj/diigo_to_zotero',
	'author': 'Justin Parnell',
	'author_email': 'parnell.justin@gmail.com',
	'maintainer': 'Justin Parnell',
	'maintainer_email': 'parnell.justin@gmail.com',
	'classifiers': [],
	'license': 'GNU GPL v3.0',
	'description': 'Converts Diigo bookmarks into Zotero bibliographic entries.',
	'long_description': 'Converts Diigo bookmarks into Zotero bibliographic entries.',
	'keywords': '',
	'install_requires': ['nose'],
	'packages': ['diigo_to_zotero'],
	'scripts': []
}
	
setup(**config)
