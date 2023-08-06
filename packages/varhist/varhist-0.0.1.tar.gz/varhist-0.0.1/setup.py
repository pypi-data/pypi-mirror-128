from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read();

setup(
	name='varhist',
	version='0.0.1',
	description='Get Variable History of specific variables',
	long_description=long_description,
	extras_require = {
		"dev" : [
			"pytest>=3.7",
		]
	},
	long_description_content_type="text/markdown",
	py_modules=["varhist"],
	package_dir={'': 'src'},
	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 2",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
	],
	url="https://github.com/Rithwik-G/VarHist-Python-Package",
	author="Rithwik Gupta",
	author_email="rithwikca2020@gmail.com"

)