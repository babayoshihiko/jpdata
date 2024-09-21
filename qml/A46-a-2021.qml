<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" version="3.28.7-Firenze" simplifyLocal="1" symbologyReferenceScale="-1" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|Rendering|CustomProperties" maxScale="0" minScale="100000000" simplifyDrawingTol="1" simplifyAlgorithm="0" readOnly="0" labelsEnabled="0" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" forceraster="0" referencescale="-1" symbollevels="0">
    <symbols>
      <symbol is_animated="0" force_rhr="0" alpha="1" type="fill" name="0" clip_to_extent="1" frame_rate="10">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="152,125,183,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="141,90,153,255"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0.26"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
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
      <Option type="List" name="dualview/previewExpressions">
        <Option type="QString" value="&quot;A46-a_001&quot;"/>
      </Option>
      <Option type="int" name="embeddedWidgets/count" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field configurationFlags="None" name="A46-a_001">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_002">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_003">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_004">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_005">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_006">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy/MM/dd"/>
            <Option type="QString" name="field_format" value="yyyy/MM/dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_007">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_008">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="A46-a_009">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="int" name="Max" value="2147483647"/>
            <Option type="int" name="Min" value="-2147483648"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="int" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="都道府県コード" field="A46-a_001"/>
    <alias index="1" name="行政コード" field="A46-a_002"/>
    <alias index="2" name="市町村名" field="A46-a_003"/>
    <alias index="3" name="区域名" field="A46-a_004"/>
    <alias index="4" name="所在地" field="A46-a_005"/>
    <alias index="5" name="告示年月日" field="A46-a_006"/>
    <alias index="6" name="告示番号" field="A46-a_007"/>
    <alias index="7" name="指定面積（ha）" field="A46-a_008"/>
    <alias index="8" name="所管省庁" field="A46-a_009"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="A46-a_001"/>
    <default applyOnUpdate="0" expression="" field="A46-a_002"/>
    <default applyOnUpdate="0" expression="" field="A46-a_003"/>
    <default applyOnUpdate="0" expression="" field="A46-a_004"/>
    <default applyOnUpdate="0" expression="" field="A46-a_005"/>
    <default applyOnUpdate="0" expression="" field="A46-a_006"/>
    <default applyOnUpdate="0" expression="" field="A46-a_007"/>
    <default applyOnUpdate="0" expression="" field="A46-a_008"/>
    <default applyOnUpdate="0" expression="" field="A46-a_009"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_001"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_002"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_003"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_004"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_005"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_006"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_007"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_008"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="A46-a_009"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="A46-a_001"/>
    <constraint desc="" exp="" field="A46-a_002"/>
    <constraint desc="" exp="" field="A46-a_003"/>
    <constraint desc="" exp="" field="A46-a_004"/>
    <constraint desc="" exp="" field="A46-a_005"/>
    <constraint desc="" exp="" field="A46-a_006"/>
    <constraint desc="" exp="" field="A46-a_007"/>
    <constraint desc="" exp="" field="A46-a_008"/>
    <constraint desc="" exp="" field="A46-a_009"/>
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
    <field editable="1" name="A46-a_001"/>
    <field editable="1" name="A46-a_002"/>
    <field editable="1" name="A46-a_003"/>
    <field editable="1" name="A46-a_004"/>
    <field editable="1" name="A46-a_005"/>
    <field editable="1" name="A46-a_006"/>
    <field editable="1" name="A46-a_007"/>
    <field editable="1" name="A46-a_008"/>
    <field editable="1" name="A46-a_009"/>
  </editable>
  <labelOnTop>
    <field name="A46-a_001" labelOnTop="0"/>
    <field name="A46-a_002" labelOnTop="0"/>
    <field name="A46-a_003" labelOnTop="0"/>
    <field name="A46-a_004" labelOnTop="0"/>
    <field name="A46-a_005" labelOnTop="0"/>
    <field name="A46-a_006" labelOnTop="0"/>
    <field name="A46-a_007" labelOnTop="0"/>
    <field name="A46-a_008" labelOnTop="0"/>
    <field name="A46-a_009" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="A46-a_001"/>
    <field reuseLastValue="0" name="A46-a_002"/>
    <field reuseLastValue="0" name="A46-a_003"/>
    <field reuseLastValue="0" name="A46-a_004"/>
    <field reuseLastValue="0" name="A46-a_005"/>
    <field reuseLastValue="0" name="A46-a_006"/>
    <field reuseLastValue="0" name="A46-a_007"/>
    <field reuseLastValue="0" name="A46-a_008"/>
    <field reuseLastValue="0" name="A46-a_009"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"A46-a_001"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
