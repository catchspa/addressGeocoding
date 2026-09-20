@echo off

REM This installs and starts the apache service
%OSGEO4W_ROOT%\apps\apache\bin\httpd -k install -n "Apache OSGeo4W Web Server"
%OSGEO4W_ROOT%\apps\apache\bin\httpd -k start -n "Apache OSGeo4W Web Server"
