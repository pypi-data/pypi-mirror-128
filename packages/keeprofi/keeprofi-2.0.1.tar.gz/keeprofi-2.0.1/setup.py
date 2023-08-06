
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "keeprofi",
	version = "2.0.1",
	python_requires = '>=3.7',
	install_requires = [
		'pyxdg>=0.26',
		'pyyaml>=5.1',
		'xerox>=0.4.1',
		'pynput>=1.4.2',
		'pykeepass>=3.0.3',
		'keyring>=19.0.1',
		'desktop-notify>=1.2.1',
		'hxss.responsibility>=0.1.1'
	],
	entry_points = {
		'console_scripts': [
			'keeprofi = keeprofi:main',
		],
	},
	author = "hxss",
	author_email = "hxss@ya.ru",
	description = "Fast rofi drun menu for keepass database",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://gitlab.com/hxss-linux/keeprofi",
	packages = setuptools.find_packages(),
	keywords = ['keepass', 'rofi', 'keyring'],
	classifiers = [
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Topic :: Utilities",
	],
)
