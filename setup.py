# Copyright (c) 2009 The Plasma Project.
# See LICENSE for details.

import os
import sys

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup, find_packages
from setuptools.command import test


class TestCommand(test.test):
    """
    A custom test class to ensure that if Twisted is available, it runs the
    tests.
    """

    def run_twisted(self):
        from twisted.trial import runner
        from twisted.trial import reporter

        from plasma.test import suite

        r = runner.TrialRunner(reporter.VerboseTextReporter)
        return r.run(suite())

    def run_tests(self):
        import logging
        logging.basicConfig()
        logging.getLogger().setLevel(logging.CRITICAL)

        try:
            import twisted

            return self.run_twisted()
        except ImportError:
            return test.test.run_tests(self)


def get_install_requirements():
    """
    Returns a list of dependancies for Tape to function correctly on the
    target platform.
    """
    install_requires = ['PyAMF>=0.5.1', 'zope.interface']

    if sys.version_info < (2, 5):
        install_requires.extend(['uuid>=1.30'])

    return install_requires


keyw = """ \
amf amf0 amf3 flex flash remoting rpc http flashplayer air bytearray
objectproxy arraycollection recordset actionscript"""

readme = os.path.join(os.path.dirname(__file__), 'README.txt')


setup(
    name='plasma',
    version='0.0.1',
    description='Blaze DS clone in Python',
    long_description=open(readme, 'rt').read(),
    url='http://plasmads.org',
    author='The Plasma Project',
    install_requires=get_install_requirements(),
    keywords=keyw,
    packages=find_packages(exclude=['*.tests']),
    license='MIT',
    platforms=['any'],
    cmdclass={
        'test': TestCommand
    },
    classifiers=[
        'Development Status :: 1 - Planning',
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
