#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from os.path import exists, dirname, join as pjoin
thisdir = dirname(__file__)

__version__ = open(pjoin(thisdir, "VERSION"), "r").read().strip()

import shutil
import argparse
from distutils.ccompiler import get_default_compiler
from tools import updatebadge
import skbuild.constants

from distutils.dist import Distribution

# setup.cfg metadata Infomation (`meta` of py dictionary)
_dt = Distribution()
_dt.parse_config_files()
_dt.parse_command_line()
_meta = _dt.get_option_dict('metadata')
def meta(s):
    return _meta[s][1]

# Please Setting ----------------------------------------------------------
# If you wan't install compiled scripts by C++ etc


PROJECT_NAME = meta("name")

skbuild.constants.SKBUILD_DIR = lambda: "build"  # If you wan't change build directory name

skbuild_opts = [
    '--skip-generator-test',
]

compiled_executefiles = [
    skbuild.constants.CMAKE_BUILD_DIR() + '/foo.exe',
]

setup_requires = [
]

cmake_args = {
    "common": [
    ],
    "nt": [
        '-G', "Visual Studio 16 2019",
    ],
    "posix": [
    ]
}
# -------------------------------------------------------------------------

from skbuild import setup

# OS Environment Infomation
iswin = os.name == "nt"
isposix = os.name == "posix"
ismsvc = get_default_compiler() == "msvc"

sys.argv.extend(skbuild_opts)
sys.argv.extend(cmake_args["common"] + cmake_args.get(os.name, []))


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


# Require pytest-runner only when running tests
if any(arg in sys.argv for arg in ('pytest', 'test')):
    setup_requires.extend(['pytest-runner>=2.0,<3dev'])


# Readme badge link update.
updatebadge.readme(pjoin(thisdir, "README.md"), new_version=__version__)


if compiled_executefiles:
    import distutils.command.build_scripts
    distutils.command.build_scripts.tokenize.detect_encoding = lambda x: ("utf-8", [])


# Edit posix platname for pypi upload error
if isposix and any(x.startswith("bdist") for x in sys.argv) \
        and not ("--plat-name" in sys.argv or "-p" in sys.argv):
    if "64" in os.uname()[-1]:
        from tools.platforms import get_platname_64bit
        sys.argv.extend(["--plat-name", get_platname_64bit()])
    else:
        from tools.platforms import get_platname_32bit
        sys.argv.extend(["--plat-name", get_platname_32bit()])

# Other Setting to setup.cfg
setup(
    packages=[PROJECT_NAME],
    scripts=compiled_executefiles,
    setup_requires=setup_requires
)
