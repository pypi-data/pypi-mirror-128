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


setup(name='polytune',
      version='0.0.0',
      description='Polyaxon Hyperparameter Optimization Engine.',
      maintainer='Polyaxon, Inc.',
      maintainer_email='contact@polyaxon.com',
      url='https://github.com/polyaxon/polytune',
      license='Apache 2.0',
      platforms='any',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      keywords=['pandas', 'numpy', 'optimization', 'sweeps', 'tuning', 'Hyperparameter Optimization', 'Hyperparameter Tuning', 'hyperopt', 'scikit-learn'],
      install_requires=[
          'polyaxon',
          'numpy',
          'pandas',
      ],
      classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest})
