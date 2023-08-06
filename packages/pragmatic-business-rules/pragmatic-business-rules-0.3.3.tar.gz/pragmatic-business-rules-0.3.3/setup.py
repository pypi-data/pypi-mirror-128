from setuptools import setup
from pragmatic_business_rules import __version__
import pathlib

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()

setup(
	name="pragmatic-business-rules",
	version=__version__,
	description="Pragmatic business rules",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/Soremwar/pragmatic_business_rules",
	author="Soremwar",
	author_email="stephenguerrero43@gmail.com",
	license="MIT",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.9",
	],
	packages=["pragmatic_business_rules"],
	include_package_data=True,
	install_requires=["jsonschema"],
)
