#!/bin/sh -eV

pylupdate5 -noobsolete i18n/jpdata.pro

# open .ts file with linguist 

lrelease

