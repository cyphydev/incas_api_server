# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "uiuc_incas_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="INCAS TA2-UIUC Datatypes",
    author_email="",
    url="",
    keywords=["Swagger", "INCAS TA2-UIUC Datatypes"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['uiuc_incas_server=uiuc_incas_server.__main__:main']},
    long_description="""\
    This API document is defined based on INCAS Common Datatypes version 0.0.6.
    """
)
