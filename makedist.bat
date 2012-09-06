call make.bat
C:\Python27\python.exe setup.py py2exe
XCOPY "C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats" "C:\Documents and Settings\Ariel\Escritorio\collector\dist\imageformats" /I /S