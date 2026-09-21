@echo off

IF "%1"=="" (
   echo kea-config.bat [OPTIONS]
   echo Options:
   echo     [--prefix]
   echo     [--version]
   echo     [--libs]
   echo     [--cflags]
   echo     [--includes]
   EXIT /B 1
) ELSE (
:printValue
    if "%1" neq "" (
	    IF "%1"=="--prefix" echo %OSGEO4W_ROOT%
	    IF "%1"=="--version" echo 1.5.3
	    IF "%1"=="--cflags" echo -I%OSGEO4W_ROOT%/include
	    IF "%1"=="--libs" echo -LIBPATH:%OSGEO4W_ROOT%/lib libkea.lib 
	    IF "%1"=="--includes" echo %OSGEO4W_ROOT%/include
		shift
		goto :printValue
    )
	EXIT /B 0
)
