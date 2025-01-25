#!/bin/sh -eV

git tag -a v0.6.13 -m 'version 0.6.13'
git push origin v0.6.13

mkdir ../qgis_plugins

cd ../qgis_plugins
rm -rf jpdata
rm -f jpdata.zip 

cp -R ../jpdata ./jpdata
perl -pi -e "s|self._verbose = True|self._verbose = False" jpdata/jpdata.py

rm -f jpdata/.gitignore
rm -rf jpdata/__pycache__
rm -rf jpdata/.git
rm -f jpdata/i18n.sh
rm -f jpdata/CITATION.cff
rm -f jpdata/zip_plugin.sh
rm -f jpdata/i18n/jpdata_ja.ts
rm -f jpdata/i18n/jpdata.pro
rm -rf jpdata/helper_script

zip -rX jpdata.zip jpdata

zip -d jpdata.zip .git/\*
zip -d jpdata.zip __MACOSX/\*
zip -d jpdata.zip \*/.DS_Store

