try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'usv',
	'author': 'Steve Loria',
	'url': 'URL to get it at',
	'download_url': 'Where to download it.',
	'author_email': 'sloria1@gmail.com',
	'version': '0.1',
	'install_requires': ['orange', 'numpy', 'scipy', 'nose'],
	'packages': ['usv'],
	'name': 'usv'
}

setup(**config)