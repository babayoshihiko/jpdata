@echo off
call "C:\Program Files\QGIS 3.22.9\bin\o4w_env.bat"
if not exist "C:\Program Files\QGIS 3.22.9\bin\apps\qgis-ltr\bin\qgisgrass7.dll" goto nograss
set savedpath=%PATH%
call "C:\Program Files\QGIS 3.22.9\bin\apps\grass\grass78\etc\env.bat"
path C:\Program Files\QGIS 3.22.9\bin\apps\grass\grass78\lib;C:\Program Files\QGIS 3.22.9\bin\apps\grass\grass78\bin;%savedpath%
:nograss
@echo off
path C:\Program Files\QGIS 3.22.9\bin\apps\qgis-ltr\bin;%PATH%
set QGIS_PREFIX_PATH=C:\Program Files\QGIS 3.22.9\apps\qgis-ltr
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=C:\Program Files\QGIS 3.22.9\apps\qgis-ltr\qtplugins;C:\Program Files\QGIS 3.22.9\apps\qt5\plugins
start "QGIS" /B "C:\Program Files\QGIS 3.22.9\bin\qgis-ltr-bin.exe" %*
