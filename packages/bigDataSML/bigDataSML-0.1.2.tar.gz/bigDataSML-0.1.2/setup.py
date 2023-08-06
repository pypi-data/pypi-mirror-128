from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.2'
DESCRIPTION = 'This package calculates average student performances'
this_directory=os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory+"/doc","ReadMe.md"),encoding="utf-8") as f:
    long_description = f.read()

# Setting up
setup(
    name="bigDataSML",
    version=VERSION,
    author="SML (Samuel Schlenker)",
    author_email="wi20067@lehre.dhbw-stuttgart.de",
    description=DESCRIPTION,
    url="https://github.com/Samu2021/bigDataSML",
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requieres=">=2.7.18",
    packages=find_packages(),
    install_requires=["pyspark >= 2.3.0"],
    keywords=["python","spark","pyspark","student","performance","calculation","bigdata","programming","fun","sml"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2.7",
        "Natural Language :: English",
        "Natural Language :: German",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)