#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from os.path import exists, dirname, join as pjoin
thisdir = dirname(__file__)

__version__ = open(pjoin(thisdir, "VERSION"), "r").read().strip()

import shutil
import argparse

from tools import updatebadge
import skbuild.constants
import platform

# OS Environment Infomation
iswin = os.name == "nt"
isposix = os.name == "posix"
islinux = platform.system() == "Linux"


# Please Setting ----------------------------------------------------------
# If you wan't install compiled scripts by C++ etc


PROJECT_NAME = '_PLEASE_PYPROJECT_NAME_'

skbuild.constants.SKBUILD_DIR = lambda: "build"  # If you wan't change build directory name

exename = '_PLEASE_EXECUTABLE_FILENAME_'
ext = ".exe" if iswin else ""
if not exename.endswith(ext):
    exename += ext

compiled_executefiles = [
    pjoin(skbuild.constants.CMAKE_BUILD_DIR(), exename),
]

cmake_args = {
    # https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/Useful-Variables
    # https://scikit-build.readthedocs.io/en/stable/usage.html#usage-scikit-build-options
    "common": [
    ],
    "nt": [
        '-G', "Ninja",
    ],
    "posix": [
    ]
}
# -------------------------------------------------------------------------

from skbuild import setup

ps = argparse.ArgumentParser()
ps.add_argument('-f', '--force', action="store_true", dest="is_force")
ps.add_argument('-g', '--debug', action="store_true", dest="is_debug")
ps.add_argument('--build-type', default="Release")
arg = ps.parse_known_args(sys.argv)[0]

if arg.is_force:
    for d in [skbuild.constants.SKBUILD_DIR(), "dist", PROJECT_NAME + ".egg-info"]:
        if exists(pjoin(thisdir, d)):
            shutil.rmtree(pjoin(thisdir, d))

if arg.is_debug and arg.build_type != "Debug":
    sys.argv.extend(['--build-type', "Debug"])


# Readme badge link update.
updatebadge.readme(pjoin(thisdir, "README.md"), new_version=__version__)


if compiled_executefiles:
    import distutils.command.build_scripts
    distutils.command.build_scripts.tokenize.detect_encoding = lambda x: ("utf-8", [])


# Edit posix platname for pypi upload error
if islinux and any(x.startswith("bdist") for x in sys.argv) \
        and not ("--plat-name" in sys.argv or "-p" in sys.argv):
    if "64" in os.uname()[-1]:
        from tools.platforms import get_platname_64bit
        sys.argv.extend(["--plat-name", get_platname_64bit()])
    else:
        from tools.platforms import get_platname_32bit
        sys.argv.extend(["--plat-name", get_platname_32bit()])

# Require pytest-runner only when running tests
is_test = 'pytest' in sys.argv or 'test' in sys.argv
# Other Setting to setup.cfg
setup(
    packages=[PROJECT_NAME],
    cmake_args=cmake_args["common"] + cmake_args.get(os.name, []),
    scripts=compiled_executefiles,
    setup_requires=['pytest-runner>=2.0,<3dev'] if is_test else []
)
