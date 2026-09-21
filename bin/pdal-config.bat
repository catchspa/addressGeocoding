@echo off

SET prefix=%OSGEO4W_ROOT%
SET exec_prefix=%OSGEO4W_ROOT%/bin
SET libdir=%OSGEO4W_ROOT%/lib


IF "%1" == "--libs" echo -L%OSGEO4W_ROOT%/lib -lpdalcpp & goto exit
IF "%1" == "--plugin-dir" echo ../install/apps/pdal/plugins & goto exit
IF "%1" == "--prefix" echo %prefix% & goto exit
IF "%1" == "--ldflags" echo -L%libdir% & goto exit
IF "%1" == "--defines" echo  & goto exit
IF "%1" == "--includes" echo -I%OSGEO4W_ROOT%/include -I%OSGEO4W_ROOT%/include/libxml2 & goto exit
IF "%1" == "--cflags" echo /DWIN32 /D_WINDOWS /W3 & goto exit
IF "%1" == "--cxxflags" echo /DWIN32 /D_WINDOWS /W3 /GR /EHsc -std=c++11 & goto exit
IF "%1" == "--version" echo 2.10.0 & goto exit


echo Usage: pdal-config [OPTIONS]
echo Options:
echo    [--cflags]
echo    [--cxxflags]
echo    [--defines]
echo    [--includes]
echo    [--libs]
echo    [--plugin-dir]
echo    [--version]

:exit
