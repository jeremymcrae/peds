
from setuptools import setup

setup (name="peds",
    description='Package for parsing pedigree files',
    version="1.1.0",
    author="Jeremy McRae",
    author_email="jmcrae@illumina.com",
    url='https://github.com/jeremymcrae/peds',
    packages=["peds"],
    install_requires=['networkx',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    test_suite="tests"
    )
