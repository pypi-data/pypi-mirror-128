# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

from qblox_instruments import build

import pulsar_qcm
import pulsar_qrm

import pulsar_qcodes_param


# -- Project information -----------------------------------------------------

project   = 'Qblox Instruments'
copyright = '2020, Qblox BV'
author    = 'Qblox'

# The full version, including alpha/beta/rc tags
release = build.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',   # auto document docstrings
              'sphinx.ext.napoleon',  # autodoc understands numpy docstrings
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx',
              'sphinx.ext.autosectionlabel',
              'sphinx-jsonschema',
              'sphinx_rtd_theme',
              "sphinx_togglebutton",
              'sphinx.ext.mathjax',
              'nbsphinx',
              'jupyter_sphinx'
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


intersphinx_mapping = {
    'qcodes': ('https://qcodes.github.io/Qcodes/', None),
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The master toctree document.
master_doc = 'index'

# Default autodoc settings
autodoc_default_options = {
    'members':          True,
    'show-inheritance': True,
    'member-order':     'bysource',
    'special-members':  '__init__',
    'undoc-members':    True,
    'exclude-members':  '__weakref__'
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_static_path = []
html_logo = "figures/qblox_block.png"
html_theme_options = {
    'display_version': False,
}

# -- Options for nbsphinx ----------------------------------------------------

nbsphinx_execute = 'never'
nbsphinx_prolog = """
.. seealso::
    An IPython notebook version of this tutorial can be downloaded here:

    :download:`{{ env.docname[10:] + ".ipynb" }} <{{ env.docname[10:] + ".ipynb" }}>`
"""

# -- Options for autosectionlabel --------------------------------------------

autosectionlabel_prefix_document = True
