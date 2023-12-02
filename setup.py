#!/usr/bin/env python

from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="genloppy",
    version="0.2.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/cklaucke/genloppy",
    license="",
    author="cklaucke",
    author_email="33376323+cklaucke@users.noreply.github.com",
    description="genlop drop in purely written in python",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "genloppy = genloppy.main:main",
        ]
    },
)
