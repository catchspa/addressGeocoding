@echo off
call set path=%%path:%OSGEO4W_ROOT%\apps\Qt5\bin=%%

path %OSGEO4W_ROOT%\apps\qt6\bin;%PATH%

set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt6\plugins

set O4W_QT_PREFIX=%OSGEO4W_ROOT:\=/%/apps/Qt6
set O4W_QT_BINARIES=%OSGEO4W_ROOT:\=/%/apps/Qt6/bin
set O4W_QT_PLUGINS=%OSGEO4W_ROOT:\=/%/apps/Qt6/plugins
set O4W_QT_LIBRARIES=%OSGEO4W_ROOT:\=/%/apps/Qt6/lib
set O4W_QT_TRANSLATIONS=%OSGEO4W_ROOT:\=/%/apps/Qt6/translations
set O4W_QT_HEADERS=%OSGEO4W_ROOT:\=/%/apps/Qt6/include
set O4W_QT_DOC=%OSGEO4W_ROOT:\=/%/apps/Qt6/doc

set QTWEBENGINE_RESOURCES_PATH=%OSGEO4W_ROOT%\apps\Qt6\resources
