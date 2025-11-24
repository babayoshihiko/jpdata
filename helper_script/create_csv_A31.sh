#!/bin/bash -eV


curl https://nlftp.mlit.go.jp/ksj/gml/data/A31a/A31a-24/A31a-24_81_10_SHP.zip -o ~/data.noindex/A31/A31a-24_81_10_SHP.zip
python3.10 helper_script/create_csv_A31.py 2024 81 北海道開発局

curl https://nlftp.mlit.go.jp/ksj/gml/data/A31a/A31a-24/A31a-24_82_10_SHP.zip -o ~/data.noindex/A31/A31a-24_82_10_SHP.zip
python3.10 helper_script/create_csv_A31.py 2024 82 東北地方整備局