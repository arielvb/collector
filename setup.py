from setuptools import setup
import os

name = 'collector.app'
version = "0.1"
VERSION = "0.1"

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
  version=version,
  description="Collection ia a management application",
  long_description=(read('README.rst')),
  app=["main.py"],
  # TODO search classifiers
  classifiers=['Intended Auidence:: Developers'],
  author="Ariel",
  author_email="i@arielvb.com",
  url="http://www.arielvb.com",
  license="GPL2",
  zip_safe=False,
  options={
            "py2app": {
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
                    ],
                "argv_emulation": True,
                "includes": ["sip", "PyQt4.QtCore", "PyQt4.QtGui", "bs4"],
                "excludes": [
                            "IPython",
                            "PyQt4.uic.port_v3.proxy_base",
                            "PyQt4.QtOpenGL",
                            "PyQt4.QtDesigner",
                            "PyQt4.phonon",
                            "PyQt4.QtMultimedia"
                            ]
            }
        },
  setup_requires=["py2app", "beautifulsoup4"]
)
