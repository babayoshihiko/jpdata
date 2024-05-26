<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="100000000" maxScale="0" simplifyMaxScale="1" simplifyDrawingTol="1" simplifyAlgorithm="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Rendering|CustomProperties" simplifyDrawingHints="1" readOnly="0" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" simplifyLocal="1" version="3.28.7-Firenze" symbologyReferenceScale="-1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 enableorderby="0" symbollevels="0" type="singleSymbol" referencescale="-1" forceraster="0">
    <symbols>
      <symbol alpha="1" type="fill" force_rhr="0" frame_rate="10" is_animated="0" clip_to_extent="1" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option type="QString" value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale"/>
            <Option type="QString" value="51,160,44,127" name="color"/>
            <Option type="QString" value="bevel" name="joinstyle"/>
            <Option type="QString" value="0,0" name="offset"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="offset_map_unit_scale"/>
            <Option type="QString" value="MM" name="offset_unit"/>
            <Option type="QString" value="51,160,44,255" name="outline_color"/>
            <Option type="QString" value="solid" name="outline_style"/>
            <Option type="QString" value="0.26" name="outline_width"/>
            <Option type="QString" value="MM" name="outline_width_unit"/>
            <Option type="QString" value="solid" name="style"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
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
      <Option type="int" value="0" name="embeddedWidgets/count"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field configurationFlags="None" name="A42_001"/>
    <field configurationFlags="None" name="A42_002"/>
    <field configurationFlags="None" name="A42_003"/>
    <field configurationFlags="None" name="A42_004"/>
    <field configurationFlags="None" name="A42_005"/>
    <field configurationFlags="None" name="A42_006"/>
    <field configurationFlags="None" name="A42_007"/>
    <field configurationFlags="None" name="A42_008"/>
    <field configurationFlags="None" name="A42_009"/>
    <field configurationFlags="None" name="A42_010"/>
  </fieldConfiguration>
  <aliases>
    <alias field="A42_001" index="0" name="都道府県名"/>
    <alias field="A42_002" index="1" name="市町村名"/>
    <alias field="A42_003" index="2" name="行政コード"/>
    <alias field="A42_004" index="3" name="地区名称"/>
    <alias field="A42_005" index="4" name="種別"/>
    <alias field="A42_006" index="5" name="当初都市計画決定年月日"/>
    <alias field="A42_007" index="6" name="最新都市計画変更年月日"/>
    <alias field="A42_008" index="7" name="面積"/>
    <alias field="A42_009" index="8" name="中心地緯度"/>
    <alias field="A42_010" index="9" name="中心地経度"/>
  </aliases>
  <defaults>
    <default field="A42_001" applyOnUpdate="0" expression=""/>
    <default field="A42_002" applyOnUpdate="0" expression=""/>
    <default field="A42_003" applyOnUpdate="0" expression=""/>
    <default field="A42_004" applyOnUpdate="0" expression=""/>
    <default field="A42_005" applyOnUpdate="0" expression=""/>
    <default field="A42_006" applyOnUpdate="0" expression=""/>
    <default field="A42_007" applyOnUpdate="0" expression=""/>
    <default field="A42_008" applyOnUpdate="0" expression=""/>
    <default field="A42_009" applyOnUpdate="0" expression=""/>
    <default field="A42_010" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="A42_001" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_002" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_003" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_004" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_005" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_006" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_007" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_008" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_009" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
    <constraint field="A42_010" notnull_strength="0" constraints="0" exp_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="A42_001" exp="" desc=""/>
    <constraint field="A42_002" exp="" desc=""/>
    <constraint field="A42_003" exp="" desc=""/>
    <constraint field="A42_004" exp="" desc=""/>
    <constraint field="A42_005" exp="" desc=""/>
    <constraint field="A42_006" exp="" desc=""/>
    <constraint field="A42_007" exp="" desc=""/>
    <constraint field="A42_008" exp="" desc=""/>
    <constraint field="A42_009" exp="" desc=""/>
    <constraint field="A42_010" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression>"A42_001"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
