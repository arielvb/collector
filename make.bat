set UI_DIR=ui\designer
set BUILD_DIR=ui\gen
set PYQT_PATH=C:\Python27\Lib\site-packages\PyQt4
echo # > %BUILD_DIR%\__init__.py
call %PYQT_PATH%\pyuic4 -x %UI_DIR%\mainWindow.ui -o %BUILD_DIR%\mainWindow.py
echo Next
call %PYQT_PATH%\pyuic4 -x %UI_DIR%\dashboard.ui -o %BUILD_DIR%\dashboard.py
call %PYQT_PATH%\pyuic4 -x %UI_DIR%\fitxa.ui -o %BUILD_DIR%\fitxa.py
call %PYQT_PATH%\pyuic4 -x %UI_DIR%\search_results.ui -o %BUILD_DIR%\search_results.py
call %PYQT_PATH%\pyuic4 -x %UI_DIR%\search_quick.ui -o %BUILD_DIR%\search_quick.py
call %PYQT_PATH%\pyrcc4 -o %BUILD_DIR%\resources_rc.py %UI_DIR%\resources.qrc
