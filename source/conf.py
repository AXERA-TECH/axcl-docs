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
import re

DOC_SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

def _first_existing_path(paths, marker=None):
    for path in paths:
        if not path:
            continue
        abs_path = os.path.abspath(path)
        if marker:
            if os.path.exists(os.path.join(abs_path, marker)):
                return abs_path
        elif os.path.exists(abs_path):
            return abs_path
    return None

AXCL_PYTHON_PATH = _first_existing_path([
    os.environ.get('AXCL_PYTHON_PATH'),
    os.path.join(DOC_SOURCE_DIR, '../axcl/python'),
    os.path.join(DOC_SOURCE_DIR, '../../python'),
    os.path.join(DOC_SOURCE_DIR, '../python'),
], 'axcl/__init__.py')

if AXCL_PYTHON_PATH:
    sys.path.insert(0, AXCL_PYTHON_PATH)

AXCL_LIB_PATH = _first_existing_path([
    os.environ.get('AXCL_LIB_PATH'),
    os.path.join(DOC_SOURCE_DIR, '../axcl/out/axcl_linux_x86/lib'),
    os.path.join(DOC_SOURCE_DIR, '../../out/axcl_linux_x86/lib'),
], 'libspdlog.so')

if AXCL_LIB_PATH:
    os.environ['AXCL_LIB_PATH'] = AXCL_LIB_PATH

# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'AXCL'
copyright = '2025, AXERA Semiconductor Co., Ltd.'
author = 'kalcohol'

# The full version, including alpha/beta/rc tags
def get_sdk_version():
    v = 'V3.16.0'
    version_mak_path = os.path.abspath(os.path.join(DOC_SOURCE_DIR, '../build/version.mak'))
    if os.path.exists(version_mak_path):
        with open(version_mak_path, 'r') as f:
            content = f.read()

        m = re.search(r'^SDK_VERSION\s*=\s*([^\s_]+(?:\.[^\s_]+){2})', content, re.M)
        if m:
            v = m.group(1)
    return v

release = get_sdk_version()
version = release
html_title = f'{project} {release}'
html_short_title = html_title

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# myst_parser is incompatible with recommonmark, myst_parser support mermaid.
extensions = [
    'myst_parser',
    'sphinx_copybutton',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["examples/*[!.zip]", "axcl.lib.rst"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# html_theme = 'alabaster'
html_theme = 'sphinx_book_theme'

# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:

# source_parsers = {
#   '.md': CommonMarkParser,
# }
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# mermaid
mermaid_output_format = 'raw'
mermaid_version = 'latest'

# myst_parser
myst_enable_extensions = ["colon_fence"]

