@echo off
call "%~dp0\o4w_env.bat"
if not exist "%OSGEO4W_ROOT%\apps\grass\grass85\etc\env.bat" goto nograss
set savedpath=%PATH%
call "%OSGEO4W_ROOT%\apps\grass\grass85\etc\env.bat"
path %OSGEO4W_ROOT%\apps\grass\grass85\lib;%OSGEO4W_ROOT%\apps\grass\grass85\bin;%savedpath%
:nograss
@echo off
path %OSGEO4W_ROOT%\apps\qgis-ltr-dev\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-ltr-dev
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr-dev\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr-dev\python;%PYTHONPATH%
"%OSGEO4W_ROOT%\apps\qgis-ltr-dev\bin\qgis_process.exe" %*
