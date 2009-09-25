# Copyright (c) 2009 The Plasma Project.
# See LICENSE for details.

import os
import sys

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup, find_packages
from setuptools.command import test


def get_version():
    """
    Gets the version number. Pulls it from the source files rather than
    duplicating it.
    """
    # we read the file instead of importing it as root sometimes does not
    # have the cwd as part of the PYTHONPATH

    fn = os.path.join(os.getcwd(), 'plasma', '__init__.py')
    lines = open(fn, 'rt').readlines()

    version = None

    for l in lines:
        # include the ' =' as __version__ is a part of __all__
        if l.startswith('__version__ =', ):
            x = compile(l, fn, 'single')
            eval(x)
            version = locals()['__version__']
            break

    if version is None:
        raise RuntimeError('Couldn\'t determine version number')

    return '.'.join([str(x) for x in version])


def get_install_requirements():
    """
    Returns a list of dependancies for Plasma to function correctly on the
    target platform.
    """
    install_requires = ['PyAMF>=0.5.1']

    if sys.version_info < (2, 5):
        install_requires.extend(['uuid>=1.30'])

    return install_requires


keyw = ''

readme = os.path.join(os.path.dirname(__file__), 'README.txt')


setup(
    name='plasma',
    version=get_version(),
    description='Plasma is a Python implementation of Flex Messaging '\
                'and Remoting',
    long_description=open(readme, 'rt').read(),
    url='http://plasmads.org',
    author='The Plasma Project',
    install_requires=get_install_requirements(),
    keywords=keyw,
    packages=find_packages(exclude=['*.test']),
    license='MIT',
    platforms=['any'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
