from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Centrality Measure Algorithims'


# Setting up
setup(
    name="CentMeasureAlgo",
    version='1.0.1',
    author="rahulleoak",
    author_email="<rahulleoak@gmail.com>",
    description="Consolidation of Centrality Measure algorithims for quicker access",
    packages=find_packages(),
    install_requires=['networkx'],
    keywords=['python', 'personal', 'centrality measure'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)