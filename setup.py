# Copyright (c) 2009 The Plasma Project.
# See LICENSE for details.

import os.path

from distribute_setup import use_setuptools

use_setuptools()
from setuptools import setup, find_packages

here = os.path.dirname(__file__)
version_path = os.path.join(here, 'plasma', 'version.py')
exec(open(version_path))

readme = os.path.join(os.path.dirname(__file__), 'README.txt')

setup(
    name='plasma',
    version=version,
    description='Plasma is a Python implementation of Flex Messaging '\
                'and Remoting',
    long_description=open(readme, 'rt').read(),
    url='http://plasmads.org',
    author='The Plasma Project',
    install_requires=['PyAMF>=0.5.1'],
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
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
