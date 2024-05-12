# jpdata

The plugin adds two identical menu items.

- Layer > Add Layer > Add Japan Data
- Plugins > jpdata > Add Japan Data

This is still an experimental plugin, and error handling etc. will be implemented in the future.

## National Land Numeric Data

First, set the destination folder. This will be loaded from the QGIS configuration file next time.

Select National Geo-information and then select a prefecture. Multiple selections can also be made.

Press the buttons in the order Download, Solution and Add. Note that if the file cannot be found, you will be asked to select a file.

Some maps do not have data for all prefectures. If this is the case, an error is generated. Error handling not yet available.

The corresponding 'QGIS Layer Style File' (QML) is in the plugins folder, but has not yet been created for all layers.

## Geographical Survey Institute tiles

Add the GSI tile server.

# jpdata （日本語）

このプラグインは、同じメニュー項目を２箇所に追加します。

- レイヤ > レイヤを追加 > 日本のデータを追加
- プラグイン > jpdata > Add Japan Data

まだ実験的プラグインであり、エラー処理などはこれから実装します。

## 国土数値情報  {#National-Land-Numeric-Data-ja}

まず、保存先フォルダを設定します。これは、次回以降は QGIS の設定ファイルから読み込まれます。

国土数値情報を選択し、都道府県を選択します。複数選択もできます。

ダウンロード、解答、追加の順番にボタンを押します。なお、ファイルが見つからない場合はファイルを選択するように求められます。

地図によっては、すべての都道府県に対してデータがあるわけではありません。その際は、エラーになります。まだエラー処理はできていません。

プラグインフォルダ内に「QGISレイヤスタイルファイル」 (QML) を用意していますが、まだすべてのレイヤに作成しているわけではありません。

## 地理院タイル  {#Geographical-Survey-Institute-tiles-ja}

国土地理院のタイルサーバーを追加します。
