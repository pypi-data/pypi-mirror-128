#!/usr/bin/env python

from os import system
from os.path import abspath
from os.path import dirname
from os.path import join

import sys
from shutil import rmtree

from setuptools import find_packages
from setuptools import setup
from setuptools import Command


HERE = abspath(dirname(__file__))


# README
LONG_DESCR =''
with open(join(HERE, 'README.md'), encoding='utf-8') as data:
    LONG_DESCR = '\n' + data.read()


# Metadata
meta = {}
with open(join(HERE, 'vrelease', 'meta.py'), encoding='utf-8') as data:
    exec(data.read(), meta)


class UploadCommand(Command):
    '''Support setup.py upload.'''

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        '''Prints things in bold.'''
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        system('twine upload dist/*')

        sys.exit()


setup(
    name=meta['NAME'],
    version=meta['VERSION'],
    description=meta['DESCRIPTION'],
    long_description=LONG_DESCR,
    long_description_content_type='text/markdown',
    author=meta['AUTHOR'],
    author_email=meta['EMAIL'],
    python_requires=meta['REQUIRES_PYTHON'],
    url=meta['URL'],
    packages=find_packages(),
    include_package_data=True,
    license=meta['LICENSE'],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],
    entry_points={'console_scripts': ['vrelease = vrelease:main']},
    cmdclass={'upload': UploadCommand},
)
