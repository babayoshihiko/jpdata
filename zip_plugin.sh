#!/bin/sh -eV

mkdir ../qgis_plugins

cd ../qgis_plugins
rm -rf jpdata

cp -R ../jpdata ./jpdata
rm -f jpdata/.gitignore
rm -rf jpdata/__pycache__
rm -rf jpdata/.git
rm -f jpdata/i18n.sh
rm -f jpdata/CITATION.cff
rm -f jpdata/zip_plugin.sh
rm -f jpdata/i18n/jpdata_ja.ts
rm -f jpdata/i18n/jpdata.pro

zip -rX jpdata.zip jpdata

zip -d jpdata.zip .git/\*
zip -d jpdata.zip __MACOSX/\*
zip -d jpdata.zip \*/.DS_Store

