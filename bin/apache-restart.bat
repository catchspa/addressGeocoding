@echo off

REM This restarts the apache service
%OSGEO4W_ROOT%\apps\apache\bin\httpd -k restart -n "Apache OSGeo4W Web Server"
