#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent


def read(rel_path):
    with open(here / rel_path) as fh:
        return fh.read()



setup(
    name="Puffin",
    version='0.0.4', 
    description="Simplify IO for your data science projects!",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Daan Duppen",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3 :: Only",
    ],
    # everything in the src directory will be made a package
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=[
        'pandas',

    ]
)
