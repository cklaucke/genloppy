#!/usr/bin/env python

from distutils.core import setup
import os


def find_packages():
    for dir_path, _dir_names, file_names in os.walk('pym'):
        if '__init__.py' in file_names:
            yield os.path.relpath(dir_path, 'pym')


def find_scripts():
    for dir_path, _dir_names, file_names in os.walk('bin'):
        for f in file_names:
            yield os.path.join(dir_path, f)


setup(
    name='genloppy',
    version='0.0.0',
    packages=list(find_packages()),
    package_dir={'': 'pym'},
    url='https://github.com/cklaucke/genloppy',
    license='',
    author='cklaucke',
    author_email='33376323+cklaucke@users.noreply.github.com',
    description='',
    scripts=list(find_scripts()),
)
