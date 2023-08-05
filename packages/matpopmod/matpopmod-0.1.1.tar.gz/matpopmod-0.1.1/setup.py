# This file is part of the matpopmod package.
# Copyright 2020, François Bienvenu - License LGPLv3+

import os, setuptools

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding = "utf-8") as fh:
    long_description = fh.read()

with open(os.path.join(here, "src", "matpopmod", "VERSION"), encoding = "utf-8") as fh:
    version = fh.read()


setuptools.setup(
    name = "matpopmod",
    author = "François Bienvenu et al.",
    author_email = "matpopmod@framalistes.org",
    description = "Matrix population models library with an interface to the COMPADRE / COMADRE databases.",
    keywords = "ecology demography populations compadre comadre",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/bienvenu/matpopmod",
    package_dir = {"": "src"},
    version=version,
    packages = setuptools.find_packages(where = "src"),
    license = "LGPLv3+",
    include_package_data=True,
    python_requires = ">=3",
    install_requires = ["numpy", "matplotlib"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    ]
)
