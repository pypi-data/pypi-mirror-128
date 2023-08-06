"""
Configuration file for the Sphinx documentation builder.

Description
-----------
This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))
sys.path.insert(2, os.path.abspath(os.path.join('..',
                                                '..',
                                               )))
sys.path.insert(3, os.path.abspath(os.path.join('..',
                                                '..',
                                                'dataframes',
                                               )))
sys.path.insert(4, os.path.abspath(os.path.join('..',
                                                '..',
                                                'doc',
                                               )))
sys.path.insert(5, os.path.abspath(os.path.join('..',
                                                '..',
                                                'io',
                                               )))
sys.path.insert(6, os.path.abspath(os.path.join('..',
                                                '..',
                                                'math',
                                               )))
sys.path.insert(6, os.path.abspath(os.path.join('..',
                                                '..',
                                                'test',
                                               )))
sys.path.insert(7, os.path.abspath(os.path.join('.',
                                                'usage',
                                               )))
sys.path.insert(8, os.path.abspath(os.path.join('.',
                                                'usage',
                                                'en',
                                               )))
sys.path.insert(10, os.path.abspath(os.path.join('.',
                                                 'usage',
                                                 'en',
                                                 'releases',
                                                )))
# -- Project information -----------------------------------------------------

project = 'pvlab'
copyright = '2021, Silva J.P.'
author = 'Silva J.P.'

# The full version, including alpha/beta/rc tags
release = '0.1.0.dev7'

# The major project version, use as the replacement for |version|
version = '0.1.0'


# -- General configuration ---------------------------------------------------

# Importing a module When necessary, if actions are required from py modules
# import pvlab

# The document name of the "master" document, that is, the document that
# contains the root ``toctree`` directive. Default is 'index'.
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx']

intersphinx_mapping = {'phython': ('https://docs.python.org/3', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The following example configures Sphinx to parse all files with the
# extensions ''.rst'' and ''.txt'' as *reStructuredText*, and ''.md'' as
# *Markdown*:
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

# This string of reStructuredText will be included at the beginning of
# every source file that is read.
rst_prolog = """
.. |psf| replace:: Python Software Foundation
"""
# This string of reStructuredText will be included at the end of every
# source file that is read.
rst_epilog = """
.. |app| replace:: ``pvlab``
"""

# If true, figures, tables and code-blocks are automatically numbered if
# they have a caption. The numref role is enabled. Obeyed so far only by
# HTML and LaTeX builders. Default is False.
numfig = True

# If set to 0, tables and code-blocks are continuosly numbered starting at 1.
# If 1 (default) numbers will be x.1, ... with x the section number. This
# apply only if setion numbering has been activated via the :numbered: option
# of the toctree directive.
numfig_secnum_depth = 1

# -- Options for internationalization ----------------------------------------

# The code for the language the docs are written in.
language = 'en'

# The filename format for language-specific figures. The default value is
# ``{root}.{language}{ext}``. It will be expanded to
# ``dirname/filename.en.png``
# from ``..image:: dirname/filename.png``. Setting this to ``{path}{language}/
# {basename}{ext}`` will expand to ``dirname/en/filename.png`` instead.
# figure_language_filename = '{path}{language}/{basename}{ext}'.

# -- Options for Math --------------------------------------------------------

# Set this option to True if you want all displayed math to be numbered. The
# default is False.
math_number_all = True

# A string used for formating the labels of references to equations. The
# {number} place-holder stands for the equation number.
math_eqref_format = 'Eq. {number}'

# If True, displayed math equations are numbered across pages when numfig is
# enabled. The numfig_secnum_depth setting is respected. The eq, not numref,
# role must be used to reference equation numbers. Default is True.
math_numfig = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_theme_options = {
    "rightsidebar": "true",
    "relbarbgcolor": "black"
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for LaTeX output ------------------------------------------------

# The LaTeX engine to build the docs. The default value is pdflatex.
latex_engine = 'pdflatex'

# If given, this must be the name of an image file (relative to the
# configuration directory) that is the logo of the docs.
# It is placed at the top of the title page. Default: None.
latex_logo = None
