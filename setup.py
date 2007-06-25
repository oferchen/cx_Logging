"""Distutils script for cx_Logging.

Windows platforms:
    python setup.py build --compiler=mingw32 install

Unix platforms
    python setup.py build install

"""

import os
import sys

from distutils.core import setup
from distutils.extension import Extension
from distutils import sysconfig

BUILD_VERSION = "1.3"

# setup extra compilation and linking args
libs = []
extraLinkArgs = []
if sys.platform == "win32":
    extraLinkArgs.append("-Wl,--add-stdcall-alias")
    extraLinkArgs.append("-Wl,--enable-stdcall-fixup")
    if sys.version_info[:2] < (2, 4):
        import win32api
        extraLinkArgs.append(win32api.GetModuleFileName(sys.dllhandle))
    libs.append("ole32")
defineMacros = [
        ("CX_LOGGING_CORE",  None),
        ("BUILD_VERSION", BUILD_VERSION)
]

# define the list of files to be included as documentation for Windows
dataFiles = None
if sys.platform in ("win32", "cygwin"):
    baseName = "cx_Logging-doc"
    dataFiles = [ (baseName, [ "LICENSE.TXT", "HISTORY.TXT", "README.TXT" ]) ]
    allFiles = []
    for fileName in open("MANIFEST").readlines():
        allFiles.append(fileName.strip())
    for dir in ["html"]:
        files = []
        for name in allFiles:
            if name.startswith(dir):
                files.append(name)
        dataFiles.append( ("%s/%s" % (baseName, dir), files) )

# setup the extension
extension = Extension(
        name = "cx_Logging",
        define_macros = defineMacros,
        extra_link_args = extraLinkArgs,
        libraries = libs,
        sources = ["cx_Logging.c"])

# perform the setup
setup(
        name = "cx_Logging",
        version = BUILD_VERSION,
        description = "Python interface for logging",
        license = "See LICENSE.txt",
        data_files = dataFiles,
        long_description = "Python interface for logging",
        author = "Anthony Tuininga",
        author_email = "anthony.tuininga@gmail.com",
        url = "http://starship.python.net/crew/atuining",
        ext_modules = [extension])

