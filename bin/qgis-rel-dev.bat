@echo off
call "%~dp0\o4w_env.bat"
call "%~dp0\qt6_env.bat"
if not exist "%OSGEO4W_ROOT%\apps\qgis-rel-dev\bin\qgisgrass8.dll" goto nograss
if not exist "%OSGEO4W_ROOT%\apps\grass\grass85\etc\env.bat" goto nograss
set savedpath=%PATH%
call "%OSGEO4W_ROOT%\apps\grass\grass85\etc\env.bat"
path %OSGEO4W_ROOT%\apps\grass\grass85\lib;%OSGEO4W_ROOT%\apps\grass\grass85\bin;%savedpath%
:nograss
@echo off
path %OSGEO4W_ROOT%\apps\qgis-rel-dev\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-rel-dev
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-rel-dev\qtplugins;%OSGEO4W_ROOT%\apps\qt6\plugins
start "QGIS" /B "%OSGEO4W_ROOT%\bin\qgis-rel-dev-bin.exe" %*
