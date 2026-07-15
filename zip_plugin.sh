#!/bin/sh -eV

# Translate
/Volumes/mac/App/QGIS-LTR.app/Contents/MacOS/bin/pylupdate -noobsolete i18n/jpdata.pro
/Volumes/mac/App/QGIS-LTR.app/Contents/MacOS/bin/pylupdate i18n.py -ts i18n/jpdata_ja.ts
open -a "/Volumes/mac/App/QGIS-LTR.app/Contents/Resources/python/site-packages/qt5_applications/Qt/bin/Linguist.app"

# Version

perl -pi -e "s|version=0.7.3.1|version=0.7.3.2|g" metadata.txt
git add .
git commit -m "Version 0.7.3.2"
git push origin main
git tag -a v0.7.3.2 -m 'version 0.7.3.2'
git push origin v0.7.3.2

# Create ZIP
mkdir ../qgis_plugins

cd ../qgis_plugins
rm -rf jpdata
rm -f jpdata.zip 

cp -R ../jpdata ./jpdata
perl -pi -e "s|self._verbose = True|self._verbose = False|g" jpdata/manager.py
perl -pi -e "s|self._verbose = True|self._verbose = False|g" jpdata/ui_handler.py
perl -pi -e "s|DEBUG_MODE = True|DEBUG_MODE = False|g" jpdata/jpDataUtils.py

rm -f jpdata/helper_script/*gtfs*

rm -f jpdata/csv/.~lock*
rm -f jpdata/MEMO.py
rm -f jpdata/MEMO.txt
rm -rf jpdata/win
rm -f pylupdate5
rm -rf jpdata/docs
rm -rf jpdata/temp

rm -f jpdata/.DS_Store
rm -f jpdata/qml/.DS_Store
rm -f jpdata/csv/.DS_Store
rm -f jpdata/.gitignore
rm -rf jpdata/__pycache__
rm -rf jpdata/.git
rm -f jpdata/i18n.sh
rm -f jpdata/CITATION.cff
rm -f jpdata/zip_plugin.sh
rm -f jpdata/README.md
rm -f jpdata/i18n/jpdata_ja.ts
rm -f jpdata/i18n/jpdata.pro
rm -rf jpdata/help
rm -rf jpdata/helper_script
rm -f jpdata/pylintrc
rm -f jpdata/qml/G04-a-2011-20250219.qml
rm -f jpdata/csv/*.py

zip -rX jpdata.zip jpdata

zip -d jpdata.zip .git/\*
zip -d jpdata.zip __MACOSX/\*
zip -d jpdata.zip \*/.DS_Store

