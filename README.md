# jpdata

The plugin adds two identical menu items.

- Layer > Add Layer > Add Japan Data
- Plugins > jpdata > Add Japan Data

This is still an experimental plugin, and error handling etc. will be implemented in the future.

## National Land Numeric Data

First, set the destination folder. This will be loaded from the QGIS configuration file next time.

Select National Geo-information and then select a prefecture. Multiple selections can also be made.

Press the buttons "Download" and "Add to Map". Note that if the file cannot be found, you will be asked to select a file.

Some maps do not have data for all prefectures. If this is the case, an error is generated. Error handling not yet available.

The corresponding 'QGIS Layer Style File' (QML) is in the plugins folder, but has not yet been created for all layers.

## Geographical Survey Institute tiles

Add the GSI tile server.

## Census

The Census is a survey conducted by the Ministry of Internal Affairs and Communications, with GIS data provided every five years since 2000. There are subregions (in units of cities, towns and villages, and wards for designated cities) and mesh units, and the plug-in supports subregions. Various geodetic systems are supported, but the plug-in uses the plane rectangular coordinate system, JGD2000 until 2010, and JGD2011 since 2015.
 JGD2011.

Choose a prefecture; then choose municipalities. Click "Download" to download the zip files. Click "Add to Map" to unzip the zip files and add shp files to QGIS map.

# jpdata （日本語）

このプラグインは、同じメニュー項目を２箇所に追加します。

- レイヤ > レイヤを追加 > 日本のデータを追加
- プラグイン > jpdata > Add Japan Data

まだ実験的プラグインであり、エラー処理などはこれから実装します。

## 国土数値情報  {#National-Land-Numeric-Data-ja}

まず、保存先フォルダを設定します。これは、次回以降は QGIS の設定ファイルから読み込まれます。

国土数値情報を選択し、都道府県を選択します。複数選択もできます。

ダウンロード、追加の順番にボタンを押します。なお、ファイルが見つからない場合はファイルを選択するように求められます。

地図によっては、すべての都道府県に対してデータがあるわけではありません。その際は、エラーになります。まだエラー処理はできていません。

プラグインフォルダ内に「QGISレイヤスタイルファイル」 (QML) を用意していますが、まだすべてのレイヤに作成しているわけではありません。

## 地理院タイル  {#Geographical-Survey-Institute-tiles-ja}

国土地理院のタイルサーバーを追加します。

## 国勢調査

国勢調査は、総務省が行なっている調査で、2000年以降 5 年ごとに GIS データが提供されています。小地域（市町村単位、なお司令指定都市は行政区単位）、メッシュ単位があり、プラグインでは小地域に対応しています。また、さまざまな測地系に対応していますが、プラグインでは平面直角座標系とし、2010年までは JGD2000、2015年以降は
 JGD2011 としています。

https://www.e-stat.go.jp/help/data-definition-information/download

都道府県を選択します。その後、市町村を選択します。zip ファイルをダウンロードするには、「ダウンロード」を押します。zip を解凍、shp ファイルを追加するには「地図に追加」を押します。

なお、政令指定都市の場合、市ではなく行政区単位の提供になります。市を選択してもダウンロードも地図へ追加もできません。

政令指定都市になった日時については、下記を参照。

https://www.soumu.go.jp/main_sosiki/jichi_gyousei/bunken/shitei_toshi-ichiran.html

## Issues

- 国土数値情報のうち、市町村単位で提供している地図
- 国土数値情報のうち、メッシュ単位で提供している地図（1 次メッシュ）
- 国土数値情報のうち、メッシュ単位で提供している地図（3 次メッシュ）
- 国土数値情報 過去のデータ
- 国勢調査 政令指定都市
- 国勢調査 市町村合併前の扱い
- 全データの英語名称

# Version History

## Version 0.6.2

* Enhanced LNI supports
  * Supports non-prefectural LNI datasets. For example, LNI datasets of Kanto region can be handled.
  * The prefecture list may be refreshed according to the LNI type.
  * Added more styles (qml files).
* Many bugfixes

## Version 0.6.1

* Added LNIs
* Many bugfixes

## Version 0.6

Released in July 2024

* Rewrote jpDownloader.py. Download can be cancelled.
* Updated Land Numerical Information (https://nlftp.mlit.go.jp/ksj_news.html)
* (LNI) Web button to open the information webpage on the default browser
* Message below the progress bar in the window

# Roadmap

## Version 0.6.3

* UI update: from dialogue to dock
* Supports proxy