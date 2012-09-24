:: "Makefile" for windows
@ECHO OFF
REM Command file for develop collector

:: ISSC path
::  xp (es_ES): "C:\Archivos de programa\Inno Setup 5\ISCC.exe"
::  7: "c:\Program Files\Inno Setup 5\ISCC.exe"

set ISCC="C:\Archivos de programa\Inno Setup 5\ISCC.exe"
set QTPLUGINS="C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats"
set UI_DIR="ui\designer"
set BUILD_DIR="ui\gen"
set PYQT_PATH="C:\Python27\Lib\site-packages\PyQt4"
set PYTHON="C:\Python27\python.exe"

if "%1" == "" (
    echo Building widgets...
    :: Make the destination folder a python package
    echo # > %BUILD_DIR%\__init__.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\mainWindow.ui -o %BUILD_DIR%\mainWindow.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\dashboard.ui -o %BUILD_DIR%\dashboard.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\fitxa_edit.ui -o %BUILD_DIR%\fitxa_edit.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\fitxa.ui -o %BUILD_DIR%\fitxa.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\search_results.ui -o %BUILD_DIR%\search_results.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\search_quick.ui -o %BUILD_DIR%\search_quick.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\collection_items.ui -o %BUILD_DIR%\collection_items.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\plugins.ui -o %BUILD_DIR%\plugins.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\toolbar.ui -o %BUILD_DIR%\toolbar.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\topbar.ui -o %BUILD_DIR%\topbar.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\properties.ui -o %BUILD_DIR%\properties.py
    call %PYQT_PATH%\pyuic4 -x %UI_DIR%\field_details.ui -o %BUILD_DIR%\field_details.py
    :: Resources
    call %PYQT_PATH%\pyrcc4 -o %BUILD_DIR%\resources_rc.py %UI_DIR%\resources.qrc
    call %PYQT_PATH%\pyrcc4 -o %BUILD_DIR%\lang_rc.py %UI_DIR%\lang.qrc
    echo.Widgets finished
    goto end
)

if "%1" == "dist" (
    echo Building distribution...
    :: Carefull the next line calls to this file whitout params, don't call
    ::  it whit dist -> infinite loop
    call make.bat
    DEL /S /Q dist
    %PYTHON% setup.py py2exe
    XCOPY "data" "dist\windows\data" /I /S
    XCOPY %QTPLUGINS% "dist\windows\imageformats" /I /S
    echo Distribution finished
    goto end
)

if "%1" == "installer" (
    echo.Building installer...
    :: Carefull the next line calls to this file whit param dist, don't call
    ::  it whit installer -> infinite loop
    call make.bat dist
    call %ISCC% /Q /O"dist" /F"Collector Installer" "collector.iss"
    echo.Installer created
    goto end
)

if  "%1" == "test" (
    %PYTHON% -m unittest discover tests
)

:: TOOD rule clean

:end
