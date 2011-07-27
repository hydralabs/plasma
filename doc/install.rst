==========================
 Plasma Installation Guide
==========================

.. contents::

Plasma requires Python_ 2.5 or newer. Python 3.0 isn't supported yet.


Manual Installation
===================

Step 1
------

:doc:`community/download` and unpack the Plasma archive of your choice::

    tar zxfv Plasma-<version>.tar.gz
    cd Plasma-<version>


Step 2
------

Run the Python-typical setup at the top of the source directory
from a command-prompt::

    python setup.py install

This will byte-compile the Python source code and install it in the
``site-packages`` directory of your Python installation.

You can run the unit tests like this::

    nosetests


Advanced Options
================

To find out about other advanced installation options, run::
    
    easy_install --help

Also see `Installing Python Modules`_ for detailed information.

To install Plasma to a custom location::
   
    easy_install --prefix=/path/to/installdir


Documentation
=============

To build the main documentation you need:

- Sphinx_ 1.0 or newer
- a :doc:`copy <community/download>` of the Plasma source distribution

Unix users run the command below in the ``doc`` directory to create the
HTML version of the Plasma documentation::

    make html

Windows users can run the make.bat file instead::

    make.bat

This will generate the HTML documentation in the ``doc/_build/html``
folder. This documentation is identical to the content on the main Plasma
website_.

**Note**: if you don't have the `make` tool installed then you can invoke
Sphinx from the ``doc`` directory directly like this::

    sphinx-build -b html . build


.. _Python: http://python.org
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install
.. _uuid:	http://pypi.python.org/pypi/uuid
.. _Installing Python Modules: http://docs.python.org/inst/inst.html
.. _Sphinx:     		http://sphinx.pocoo.org
.. _website:    		http://plasmads.org
