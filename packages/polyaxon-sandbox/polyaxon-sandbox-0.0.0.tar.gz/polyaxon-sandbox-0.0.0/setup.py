#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='polyaxon-sandbox',
      version='0.0.0',
      description='An ML/AI tracking sandbox for debugging, organizing, and syncing local experiments.',
      maintainer='Polyaxon, Inc.',
      maintainer_email='contact@polyaxon.com',
      url='https://github.com/polyaxon/sandbox',
      license='Apache 2.0',
      platforms='any',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      keywords=['polyaxon', 'machine-learning', 'deep-learning', 'ai', 'ml', 'tracking', 'scikit-learn', 'pytorch', 'tensorflow', 'keras'],
      install_requires=[],
      classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest})
