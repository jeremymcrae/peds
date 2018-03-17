
import io
from setuptools import setup

setup (name="peds",
    description='Package for parsing pedigree files',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    version="1.3.2",
    author="Jeremy McRae",
    author_email="jmcrae@illumina.com",
    license="MIT",
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
