@echo off

REM This stops and uninstalls apache service
%OSGEO4W_ROOT%\apps\apache\bin\httpd -k stop -n "Apache OSGeo4W Web Server"
%OSGEO4W_ROOT%\apps\apache\bin\httpd -k uninstall -n "Apache OSGeo4W Web Server"
