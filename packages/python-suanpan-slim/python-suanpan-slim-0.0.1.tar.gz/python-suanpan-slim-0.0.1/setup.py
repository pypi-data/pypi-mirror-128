#!/usr/bin/env python

"""
suanpan
"""


import os
import re

from setuptools import find_packages, setup

VERSION_PARRTERN = r"__version__ = \"([\d\w\.]*)\""
VERSION_FILE = os.path.join("suanpan", "__init__.py")
VERSION = re.findall(VERSION_PARRTERN, open(VERSION_FILE, "r").read())[0]

BASE_REQUIRES = [
    "pyyaml",
    "pandas>=1.3.4",
    "xlrd>=2.0.1",
    "oss2>=2.9.1",
    "minio==7.0.0",
    "redis>=3.2.0",
    "gevent>=20.5.0",
    "python-socketio[client]==5.4.0",
    "gevent-websocket>=0.10.1",
]
INSTALL_REQUIRES = BASE_REQUIRES
README = "README.md"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


packages = find_packages(exclude=["tests"])

setup(
    name="python-suanpan-slim",
    version=VERSION,
    packages=packages,
    license="See License",
    author="yanqinghao",
    author_email="woshiyanqinghao@gmail.com",
    description="Suanpan SDK",
    long_description=read_file(README),
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
