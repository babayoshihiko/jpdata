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
            <Option name="name" value="transport/transport_aerodrome2.svg" type="QString"/>
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
      <Option name="dualview/previewExpressions" type="List">
        <Option value="&quot;C28_014&quot;" type="QString"/>
      </Option>
      <Option name="embeddedWidgets/count" value="0" type="int"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="C28_014" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="C28_015" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="C28_016" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="C28_000" configurationFlags="None">
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
    <alias index="0" field="C28_014" name="調査年"/>
    <alias index="1" field="C28_015" name="１日あたりの着陸回数"/>
    <alias index="2" field="C28_016" name="１日あたりの乗降客数"/>
    <alias index="3" field="C28_000" name="調査内容ID"/>
  </aliases>
  <defaults>
    <default expression="" field="C28_014" applyOnUpdate="0"/>
    <default expression="" field="C28_015" applyOnUpdate="0"/>
    <default expression="" field="C28_016" applyOnUpdate="0"/>
    <default expression="" field="C28_000" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="C28_014" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="C28_015" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="C28_016" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="C28_000" exp_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="C28_014" desc="" exp=""/>
    <constraint field="C28_015" desc="" exp=""/>
    <constraint field="C28_016" desc="" exp=""/>
    <constraint field="C28_000" desc="" exp=""/>
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
    <field editable="1" name="C28_000"/>
    <field editable="1" name="C28_014"/>
    <field editable="1" name="C28_015"/>
    <field editable="1" name="C28_016"/>
  </editable>
  <labelOnTop>
    <field name="C28_000" labelOnTop="0"/>
    <field name="C28_014" labelOnTop="0"/>
    <field name="C28_015" labelOnTop="0"/>
    <field name="C28_016" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="C28_000" reuseLastValue="0"/>
    <field name="C28_014" reuseLastValue="0"/>
    <field name="C28_015" reuseLastValue="0"/>
    <field name="C28_016" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"C28_014"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
