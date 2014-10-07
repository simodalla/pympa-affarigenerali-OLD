#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import organigrammi

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = organigrammi.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='openpa-organigrammi',
    version=version,
    description="""Your project description goes here""",
    long_description=readme + '\n\n' + history,
    author='Simone Dalla',
    author_email='simodalla@gmail.com',
    url='https://github.com/simodalla/openpa-organigrammi',
    packages=[
        'organigrammi',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='openpa-organigrammi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)