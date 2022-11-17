from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hackon/__init__.py
from hackon import __version__ as version

setup(
	name="hackon",
	version=version,
	description="Frappe app to facilitate Hackathon Events",
	author="efeone",
	author_email="info@efeone.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
