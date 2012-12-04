"""
Setup for Collector
"""
from setuptools import setup
import os
from collector.core.config import ISWINDOWS, ISOSX

NAME = 'Collector'
VERSION = "0.2"


def read(*rnames):
    """Reads the requestes files"""
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


OPTIONS = {}
REQUIRES = ["beautifulsoup4", 'sqlalchemy']

if ISOSX:
    OPTIONS['py2app'] = {
        "iconfile": "collection.icns",
        "plist": {
            'CFBundleGetInfoString':
            "Collector, a collection management application.",
            'CFBundleIdentifier': 'com.arielvb.collector',
            'CFBundleShortVersionString': VERSION,
            'CFBundleVersion': 'Collector' + ' ' + VERSION,
            'LSMinimumSystemVersion': '10.4.3',
            'LSMultipleInstancesProhibited': 'true',
            'NSHumanReadableCopyright':
            'Copyright 2012, arielvb.com'
        },
        "resources": [
            #'qt.conf'
            "data",
        ],
        "argv_emulation": True,
        "includes": ["sip", "PyQt4.QtCore", "PyQt4.QtGui", "bs4",
            'sqlalchemy.dialects.sqlite'],
        "excludes": [
            "IPython",
            "PyQt4.uic.port_v3.proxy_base",
            "PyQt4.QtOpenGL",
            "PyQt4.QtDesigner",
            "PyQt4.phonon",
            "PyQt4.QtMultimedia"
        ]
    }
    REQUIRES.append('py2app')
    EXTRAOPTIONS = dict(app=["main.py"])

if ISWINDOWS:
    __import__('py2exe')
    OPTIONS['py2exe'] = {
        "dist_dir": 'dist/windows',
        "skip_archive": True,
        "includes": [
            "sip",
            "sqlalchemy.dialects.sqlite"],
        "dll_excludes": [
            "MSVCP90.dll",
            "MSWSOCK.dll",
            "mswsock.dll",
            "powrprof.dll",
        ],
    }
    REQUIRES.append('py2exe')
    EXTRAOPTIONS = dict(windows=[{
        "script": "main.py",
        "dest_base": "Collector",
        'icon_resources':[(1, 'collection.ico')]
    }])

setup(
    name=NAME,
    version=VERSION,
    description="Collector is a management application",
    long_description=(read('README.txt')),
    # TODO search classifiers
    classifiers=['Intended Auidence:: Developers, Collectors'],
    author="Ariel von Barnekow",
    author_email="i@arielvb.com",
    url="http://www.arielvb.com",
    license="GPL2",
    zip_safe=False,
    packages=["engine", "plugins", "ui", "ui.views",
     "ui.helpers", "ui.gen", "tests", "ui.workers"],
    # data_files=[('data', 'data/*')],
    options=OPTIONS,
    test_suite='tests',
    setup_requires=REQUIRES,
    **EXTRAOPTIONS
)
