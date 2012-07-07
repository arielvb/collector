from distutils.core import setup
import py2exe

setup(name="main",
      version="0.1",
      author="Ariel von Barnekow",
      author_email="i@arielvb.com",
      url="https://dev.arielvb.com/collection",
      license="GNU General Public License (GPL)",
      #packages=['beautifulsoup4'],
      #packages=['ui', 'ui.gen', 'collector'],
      #package_data={"main": ["ui/*"]},
      #scripts=["main.py"],
      windows=[{"script": "main.py",
      'icon_resources':[(1,'collection.ico')]}],
      options={"py2exe": {"skip_archive": True, "includes": ["sip"],
      "dll_excludes": [
                  "MSVCP90.dll",
                  "MSWSOCK.dll",
                  "mswsock.dll",
                  "powrprof.dll",
                  ],

      }})