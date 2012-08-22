from setuptools import setup
import os
from engine.config import iswin, isosx

name = 'Collector'
version = "0.1"
VERSION = "0.1"


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


options = {}
requires = ["beautifulsoup4"]
if isosx:
    options['py2app'] = {
                "iconfile": "collection.icns",
                "plist": {
                        'CFBundleGetInfoString': '''Collection, a collection management application.''',
                        'CFBundleIdentifier': 'com.arielvb.collection',
                        'CFBundleShortVersionString': VERSION,
                        'CFBundleVersion': 'Collection' + ' ' + VERSION,
                        'LSMinimumSystemVersion': '10.4.3',
                        'LSMultipleInstancesProhibited': 'true',
                        'NSHumanReadableCopyright': 'Copyright 2012, arielvb.com',
                    },
                "resources": [
                        #'qt.conf'
                        "data",
                    ],
                "argv_emulation": True,
                "includes": ["sip", "PyQt4.QtCore", "PyQt4.QtGui", "bs4"],
                "excludes": [
                            "IPython",
                            "PyQt4.uic.port_v3.proxy_base",
                            "PyQt4.QtOpenGL",
                            "PyQt4.QtDesigner",
                            "PyQt4.phonon",
                            "PyQt4.QtMultimedia",
                            ]
            }
    requires.append('py2app')
    extraoptions = dict()

if iswin:

    options['py2exe'] = {
                "skip_archive": True,
                "includes": ["sip"],
                "dll_excludes": [
                      "MSVCP90.dll",
                      "MSWSOCK.dll",
                      "mswsock.dll",
                      "powrprof.dll",
                      ],
            }
    requires.append('py2exe')
    extraoptions = dict(windows=[{
            "script": "collector.py",
            'icon_resources':[(1, 'collection.ico')]
            }])

setup(
  name=name,
  version=version,
  description="Collector is a management application",
  long_description=(read('README.rst')),
  # TODO search classifiers
  classifiers=['Intended Auidence:: Developers'],
  author="Ariel",
  author_email="i@arielvb.com",
  url="http://www.arielvb.com",
  license="GPL2",
  zip_safe=False,
  app=["collector.py"],
  options=options,
  setup_requires=requires,
  **extraoptions
)