"""
Setup for Collector
"""
from setuptools import setup, find_packages
import os
from collector.core.config import ISWINDOWS, ISOSX

NAME = 'Collector'
VERSION = "0.3"


def read(*rnames):
    """Reads the requestes files"""
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


OPTIONS = {}
REQUIRES = ["beautifulsoup4", 'sqlalchemy']
EXTRAOPTIONS = {}

if ISOSX:
    OPTIONS['py2app'] = {
        "iconfile": "collector.icns",
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
    EXTRAOPTIONS = dict(app=[os.path.join("collector", "main.py")])

if ISWINDOWS:
    __import__('py2exe')
    OPTIONS['py2exe'] = {
        "dist_dir": 'dist/windows',
        "skip_archive": False,
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
        "script": os.path.join("collector", "main.py"),
        "dest_base": "Collector",
        'icon_resources':[(1, 'collector.ico')]
    }])

setup(
    name=NAME,
    version=VERSION,
    description="Collector is a management application",
    long_description=(read('README.txt')),
    # Classifiers full list:
    #   http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: Spanish',
        'Natural Language :: Catalan',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities'
    ],
    author="Ariel von Barnekow",
    author_email="projects@arielvb.com",
    url="http://www.collector.cat",
    license="GPL2",
    zip_safe=True,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    options=OPTIONS,
    test_suite='tests',
    setup_requires=REQUIRES,
    entry_points={
        'console_scripts': ["collector=collector.main:main"]
    },
    **EXTRAOPTIONS
)
