# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.
#
# Plasma documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

import sys, os, time
from shutil import copyfile

from docutils.core import publish_parts

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute.
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('html'))

def rst2html(input, output):
    """
    Create html file from rst file.
    
    :param input: Path to rst source file
    :type: `str`
    :param output: Path to html output file
    :type: `str`
    """
    file = os.path.abspath(input)
    rst = open(file, 'r').read()
    html = publish_parts(rst, writer_name='html')
    body = html['html_body']

    tmp = open(output, 'w')
    tmp.write(body)
    tmp.close()
    
    return body

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.intersphinx', 'sphinx.ext.extlinks']

# Paths that contain templates, relative to this directory.
templates_path = ['html']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
#master_doc = 'index'

# create content template for the homepage
readme = rst2html('../README.txt', 'html/intro.html')
readme = copyfile('../CHANGES.txt', 'changelog.rst')

# Location of the Plasma source root folder.
from plasma.version import version

# General substitutions.
project = 'Plasma'
url = 'http://plasmads.org'
description = 'Flex Messaging support for Python'
copyright = "Copyright &#169; %s The <a href='%s'>%s</a> Project. All rights reserved." % (
            time.strftime('%Y'), url, project)

# We look for the __init__.py file in the current Plasma source tree
# and replace the values accordingly.
#
# The full version, including alpha/beta/rc tags.
version = str(version)

# The short X.Y version.
release = version[:3]

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# A list of directory paths, relative to the source directory, that are to
# be recursively excluded from the search for source files, that is, their
# subdirectories won’t be searched too.
exclude_trees = ['_build', 'tutorials/examples']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'trac'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '%s - %s' % (project, description)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['html/static']

# The name of an image file (.ico) that is the favicon of the docs.
#html_favicon = 'plasma.ico'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    'toc': 'sidebartoc.html'
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
html_additional_pages = {
    'index': 'indexcontent.html',
    'tutorials/index': 'tutorials.html',
}

# Content template for the index page, filename relative to this file.
html_index = 'indexcontent.html'

# If false, no module index is generated.
html_use_modindex = True

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = True

# Output an OpenSearch description file.
html_use_opensearch = 'http://plasmads.org'

# Output file base name for HTML help builder.
htmlhelp_basename = 'plasma' + release.replace('.', '')

# Split the index
html_split_index = True


# -- Options for external links --------------------------------------------------

# refer to the Python standard library.
intersphinx_mapping = {'python': ('http://docs.python.org', None)}

# A list of regular expressions that match URIs that should
# not be checked when doing a 'make linkcheck' build (since Sphinx 1.1)
linkcheck_ignore = [r'http://localhost:\d+/']

# The base url of the Trac instance you want to create links to
trac_url = 'http://dev.plasmads.org'

# Trac url mapping
extlinks = {'ticket': (trac_url + '/ticket/%s', '#')}
