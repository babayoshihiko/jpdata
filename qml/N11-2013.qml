<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" minScale="100000000" simplifyLocal="1" symbologyReferenceScale="-1" version="3.28.7-Firenze" labelsEnabled="0" simplifyDrawingHints="0" simplifyDrawingTol="1" readOnly="0" simplifyMaxScale="1" simplifyAlgorithm="0" maxScale="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|Rendering|CustomProperties">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 enableorderby="0" referencescale="-1" forceraster="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol force_rhr="0" alpha="1" name="0" is_animated="0" clip_to_extent="1" frame_rate="10" type="marker">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" pass="0" locked="0" class="SvgMarker">
          <Option type="Map">
            <Option name="angle" value="0" type="QString"/>
            <Option name="color" value="31,120,180,255" type="QString"/>
            <Option name="fixedAspectRatio" value="0" type="QString"/>
            <Option name="horizontal_anchor_point" value="1" type="QString"/>
            <Option name="name" value="transport/transport_helicopter.svg" type="QString"/>
            <Option name="offset" value="0,0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="outline_color" value="35,35,35,255" type="QString"/>
            <Option name="outline_width" value="0" type="QString"/>
            <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="outline_width_unit" value="MM" type="QString"/>
            <Option name="parameters"/>
            <Option name="scale_method" value="diameter" type="QString"/>
            <Option name="size" value="8" type="QString"/>
            <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="size_unit" value="MM" type="QString"/>
            <Option name="vertical_anchor_point" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <Option type="Map">
      <Option name="embeddedWidgets/count" value="0" type="int"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="N11_001" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="N11_002" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="N11_003" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="N11_004" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="N11_005" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="N11_006" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="N11_007" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="N11_001" name="名称"/>
    <alias index="1" field="N11_002" name="航空法分類"/>
    <alias index="2" field="N11_003" name="地域防災計画分類"/>
    <alias index="3" field="N11_004" name="都道府県コード"/>
    <alias index="4" field="N11_005" name="所在地"/>
    <alias index="5" field="N11_006" name="管理者名"/>
    <alias index="6" field="N11_007" name="滑走路面積"/>
  </aliases>
  <defaults>
    <default expression="" field="N11_001" applyOnUpdate="0"/>
    <default expression="" field="N11_002" applyOnUpdate="0"/>
    <default expression="" field="N11_003" applyOnUpdate="0"/>
    <default expression="" field="N11_004" applyOnUpdate="0"/>
    <default expression="" field="N11_005" applyOnUpdate="0"/>
    <default expression="" field="N11_006" applyOnUpdate="0"/>
    <default expression="" field="N11_007" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="N11_001" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="N11_002" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="N11_003" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="N11_004" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="N11_005" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="N11_006" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="N11_007" exp_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="N11_001" desc="" exp=""/>
    <constraint field="N11_002" desc="" exp=""/>
    <constraint field="N11_003" desc="" exp=""/>
    <constraint field="N11_004" desc="" exp=""/>
    <constraint field="N11_005" desc="" exp=""/>
    <constraint field="N11_006" desc="" exp=""/>
    <constraint field="N11_007" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGISフォームは、フォームを開いた直後に実行されるPython関数を設定できます。

この関数でロジックを追加できます

"Python Init function"に関数の名前を入力します
以下はコード例です:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="N11_001"/>
    <field editable="1" name="N11_002"/>
    <field editable="1" name="N11_003"/>
    <field editable="1" name="N11_004"/>
    <field editable="1" name="N11_005"/>
    <field editable="1" name="N11_006"/>
    <field editable="1" name="N11_007"/>
  </editable>
  <labelOnTop>
    <field name="N11_001" labelOnTop="0"/>
    <field name="N11_002" labelOnTop="0"/>
    <field name="N11_003" labelOnTop="0"/>
    <field name="N11_004" labelOnTop="0"/>
    <field name="N11_005" labelOnTop="0"/>
    <field name="N11_006" labelOnTop="0"/>
    <field name="N11_007" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="N11_001" reuseLastValue="0"/>
    <field name="N11_002" reuseLastValue="0"/>
    <field name="N11_003" reuseLastValue="0"/>
    <field name="N11_004" reuseLastValue="0"/>
    <field name="N11_005" reuseLastValue="0"/>
    <field name="N11_006" reuseLastValue="0"/>
    <field name="N11_007" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"N11_001"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
