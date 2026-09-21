call "%~dp0\o4w_env.bat"
call "%~dp0\qt6_env.bat"
set PGMODELER_SCHEMAS_DIR=%OSGEO4W_ROOT%\apps\pgmodeler\schemas
set PGMODELER_CONF_DIR=%OSGEO4W_ROOT%\apps\pgmodeler\conf
set PGMODELER_SAMPLES_DIR=%OSGEO4W_ROOT%\apps\pgmodeler\samples
set PGMODELER_TMPL_CONF_DIR=%OSGEO4W_ROOT%\apps\pgmodeler\tmpl
set PGMODELER_TEMP_DIR=%TEMP%
set PGMODELER_CH_PATH=%OSGEO4W_ROOT%\apps\pgmodeler\pgmodeler-ch.exe
set PGMODELER_CLI_PATH=%OSGEO4W_ROOT%\apps\pgmodeler\pgmodeler-cli.exe
set PGMODELER_SE_PATH=%OSGEO4W_ROOT%\apps\pgmodeler\pgmodeler-se.exe
set PGMODELER_PATH=%OSGEO4W_ROOT%\apps\pgmodeler\pgmodeler.exe
start "PostgreSQL Database Modeler" /B "%OSGEO4W_ROOT%"\apps\pgmodeler\pgmodeler.exe %*
