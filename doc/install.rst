==========================
 Plasma Installation Guide
==========================

.. contents::

Plasma requires Python_ 2.3 or newer. Python 3.0 isn't supported yet.


Easy Installation
=================

If you have setuptools_ or the `easy_install`_ tool already installed,
simply type the following on the command-line to install Plasma::

    easy_install plasma

`Note: you might need root permissions or equivalent for these steps.`

If you don't have `setuptools` or `easy_install`, first download
ez_setup.py_ and run::

    python ez_setup.py

After `easy_install` is installed, run `easy_install plasma` again. If
you run into problems, try the manual installation instructions below.

To upgrade your existing Plasma installation to the latest version
use::

    easy_install -U plasma


Manual Installation
===================

To use Plasma with Python 2.3 or 2.4, the following software packages
must be installed. The ``easy_install`` command will automatically
install them for you, as described above, but you can also choose to
download and install the packages manually.

You **don't** need these packages if you're using Python 2.5 or newer.

- ElementTree_ 1.2.6 or newer
- uuid_ 1.30 or newer

Step 1
------

Download_ and unpack the Plasma archive of your choice::

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

    python setup.py test


Advanced Options
================

To find out about other advanced installation options, run::
    
    easy_install --help

Also see `Installing Python Modules`_ for detailed information.

To install Plasma to a custom location::
   
    easy_install --prefix=/path/to/installdir


.. _Python: 	http://www.python.org
.. _setuptools:	http://peak.telecommunity.com/DevCenter/setuptools
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install
.. _ez_setup.py: http://svn.pyamf.org/pyamf/trunk/ez_setup.py
.. _Download:	http://plasmads.org/install.html
.. _ElementTree: http://effbot.org/zone/element-index.htm
.. _uuid:	http://pypi.python.org/pypi/uuid
.. _Installing Python Modules: http://docs.python.org/inst/inst.html