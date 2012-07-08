from setuptools import setup

VERSION = "0.1"

setup(
  app=["main.py"],
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
                "includes": ["sip", "PyQt4.Qt", "bs4"],
                "excludes": [
                            # "IPython",
                            # "PyQt4.uic.port_v3.proxy_base",
                            # "PyQt4.QtOpenGL",
                            # "PyQt4.QtDesigner",
                            # "PyQt4.phonon",
                            # "PyQt4.QtMultimedia"
                            ]
            }
        },
  setup_requires=["py2app", "beautifulsoup4"]
)
