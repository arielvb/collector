call make.bat
DEL /S /Q dist
C:\Python27\python.exe setup.py py2exe
XCOPY "data" "dist\data" /I /S
XCOPY "C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats" "dist\imageformats" /I /S