import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="sqlreader",
	version="0.0.2",
	author="Sidq",
	author_email="dimax258223@gmail.com",
	description="Simple package to read sql files",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/sidqdev/sqlreader",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)