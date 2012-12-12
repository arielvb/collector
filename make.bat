:: "Makefile" for windows
@ECHO OFF
REM Command file for develop collector

:: ISSC path
::  xp (es_ES): "C:\Archivos de programa\Inno Setup 5\ISCC.exe"
::  7: "c:\Program Files\Inno Setup 5\ISCC.exe"

set ISCC="C:\Archivos de programa\Inno Setup 5\ISCC.exe"
set QTPLUGINS="C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats"
set UI_DIR="collector\ui\designer"
set BUILD_DIR="collector\ui\gen"
set PYQT_PATH="C:\Python27\Lib\site-packages\PyQt4"
set PYTHON="C:\Python27\python.exe"

if "%1" == "" (
    echo Building widgets...
    :: Make the destination folder a python package
    mkdir %BUILD_DIR%
    echo # > %BUILD_DIR%\__init__.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\mainWindow.ui -o %BUILD_DIR%\mainWindow.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\dashboard.ui -o %BUILD_DIR%\dashboard.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\fitxa.ui -o %BUILD_DIR%\fitxa.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\fitxa_edit.ui -o %BUILD_DIR%\fitxa_edit.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\search_results.ui -o %BUILD_DIR%\search_results.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\search_quick.ui -o %BUILD_DIR%\search_quick.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\collection_items.ui -o %BUILD_DIR%\collection_items.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\preferences.ui -o %BUILD_DIR%\preferences.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\toolbar.ui -o %BUILD_DIR%\toolbar.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\topbar.ui -o %BUILD_DIR%\topbar.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\properties.ui -o %BUILD_DIR%\properties.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\field_details.ui -o %BUILD_DIR%\field_details.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\file_data.ui -o %BUILD_DIR%\file_data.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\file_selector.ui -o %BUILD_DIR%\file_selector.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\widget_ref.ui -o %BUILD_DIR%\widget_ref.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\widget_multivalue.ui -o %BUILD_DIR%\widget_multivalue.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\advanced_search.ui -o %BUILD_DIR%\advanced_search.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\widget_filter.ui -o %BUILD_DIR%\widget_filter.py
    call %PYQT_PATH%\pyuic4 %UI_DIR%\im_export.ui -o %BUILD_DIR%\im_export.py

    :: Resources
    call %PYQT_PATH%\pyrcc4 -o %BUILD_DIR%\img_rc.py %UI_DIR%\img\img.qrc
    call %PYQT_PATH%\pyrcc4 -o %BUILD_DIR%\lang_rc.py %UI_DIR%\lang.qrc
    call %PYQT_PATH%\pyrcc4 -o %BUILD_DIR%\splash_rc.py %UI_DIR%\splash\splash.qrc

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
