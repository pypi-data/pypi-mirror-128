# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="heureka_overene",
	version="0.0.3",
	author="Michal Kubek",
	author_email="kubek@wisdomtech.sk",
	description="Heureka API client for service overene zákazníkmi",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/wisdom-technologies/heureka-overene",
	project_urls={
		"Bug Tracker": "https://github.com/wisdom-technologies/heureka-overene/issues",
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	python_requires=">=3.6",
	install_requires=[
		'requests',
	],
	extras_require={
		'test': [
			'httpretty',
			'pytest'
		]
	}
)
