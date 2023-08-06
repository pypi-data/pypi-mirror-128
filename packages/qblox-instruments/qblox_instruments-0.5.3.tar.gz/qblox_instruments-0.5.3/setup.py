#------------------------------------------------------------------------------
# Description    : The setup script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
from qblox_instruments import build

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("AUTHORS.rst") as authors_file:
    authors = authors_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

requirements = [
    "numpy",
    "qcodes",
    "jsonschema",
    "spirack"
]

setup_requirements = [
    "setuptools<57.1.0"
]

docs_requirements = [
    "sphinx<4.0.0", # jupyter_sphinx requires v2, but builds fail with v4 and up.
    "sphinx-togglebutton",
    "sphinx-jsonschema",
    "sphinx-rtd-theme",
    "nbsphinx",
    "jupyter_sphinx",
]

test_requirements = [
    "pylint",
    "pylint-exit",
    "anybadge",
    "pytest",
    "pytest-runner",
    "pytest-cov",
    "scipy",
    "twine",
] + docs_requirements # docs (docs are also built as a test)


setup(
    name                          = "qblox_instruments",
    author                        = "Qblox BV",
    author_email                  = "support@qblox.com",
    license                       = "BSD 4-Clause",
    version                       = build.__version__,
    url                           = "https://gitlab.com/qblox/packages/software/qblox_instruments",
    download_url                  = "https://gitlab.com/qblox/packages/software/qblox_instruments/-/archive/v{0}/qblox_instruments-v{0}.zip".format(build.__version__),
    description                   = "Instrument drivers for Qblox devices.",
    long_description              = readme + "\n\n" + authors + "\n\n" + history,
    long_description_content_type = "text/x-rst",
    keywords                      = ["Qblox", "QCoDeS", "instrument", "driver"],
    classifiers                   = classifiers,
    python_requires               = ">=3.7",
    install_requires              = requirements,
    extras_require                = {'dev': test_requirements, "docs": docs_requirements},
    include_package_data          = True,
    packages                      = find_packages(include=["qblox_instruments", "ieee488_2", "pulsar_qcm", "pulsar_qrm", "cluster", "spi_rack"]),
    package_dir                   = {"ieee488_2": "ieee488_2"},
    package_data                  = {"":          ["LICENSE", "README.rst", "AUTHORS.rst", "HISTORY.rst"],
                                   "ieee488_2": ["assembler/q1asm_linux", "assembler/q1asm_macos", "assembler/q1asm_windows.exe"]},
    setup_requires                = setup_requirements,
    test_suite                    = "tests",
    tests_require                 = test_requirements,
    zip_safe                      = False
)
