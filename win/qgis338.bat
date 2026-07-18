@echo off

call "C:\Program Files\QGIS 3.38.2\bin\o4w_env.bat"

if not exist "C:\Program Files\QGIS 3.38.2\bin\qgisgrass8.dll" goto nograss

set savedpath=%PATH%
call "C:\Program Files\QGIS 3.38.2\apps\grass\grass84\etc\env.bat"
path C:\Program Files\QGIS 3.38.2\apps\grass\grass84\lib;C:\Program Files\QGIS 3.38.2\apps\grass\grass84\bin;%savedpath%

:nograss
path C:\Program Files\QGIS 3.38.2\apps\qgis\bin;%PATH%

set QGIS_PREFIX_PATH=C:/OSGeo4W/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES

rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000

set QT_PLUGIN_PATH=C:\Program Files\QGIS 3.38.2\apps\qgis\qtplugins;C:\Program Files\QGIS 3.38.2\apps\qt5\plugins

start "QGIS" /B "C:\Program Files\QGIS 3.38.2\bin\qgis-bin.exe" %*