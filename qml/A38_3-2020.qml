<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" readOnly="0" version="3.28.7-Firenze" simplifyAlgorithm="0" simplifyDrawingHints="1" symbologyReferenceScale="-1" maxScale="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" labelsEnabled="0" simplifyDrawingTol="1" minScale="100000000" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Rendering|CustomProperties">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 type="singleSymbol" referencescale="-1" enableorderby="0" symbollevels="0" forceraster="0">
    <symbols>
      <symbol type="fill" clip_to_extent="1" alpha="1" is_animated="0" name="0" frame_rate="10" force_rhr="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <Option type="Map">
            <Option type="QString" value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale"/>
            <Option type="QString" value="190,178,151,255" name="color"/>
            <Option type="QString" value="bevel" name="joinstyle"/>
            <Option type="QString" value="0,0" name="offset"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="offset_map_unit_scale"/>
            <Option type="QString" value="MM" name="offset_unit"/>
            <Option type="QString" value="227,26,28,255" name="outline_color"/>
            <Option type="QString" value="solid" name="outline_style"/>
            <Option type="QString" value="2" name="outline_width"/>
            <Option type="QString" value="MM" name="outline_width_unit"/>
            <Option type="QString" value="no" name="style"/>
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
    <field name="A38c_001" configurationFlags="None"/>
    <field name="A38c_002" configurationFlags="None"/>
  </fieldConfiguration>
  <aliases>
    <alias field="A38c_001" name="都道府県名" index="0"/>
    <alias field="A38c_002" name="三次医療圏名" index="1"/>
  </aliases>
  <defaults>
    <default expression="" field="A38c_001" applyOnUpdate="0"/>
    <default expression="" field="A38c_002" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" exp_strength="0" field="A38c_001" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="A38c_002" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="A38c_001" exp=""/>
    <constraint desc="" field="A38c_002" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression>"A38c_001"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
