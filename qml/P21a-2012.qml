<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.7-Firenze" simplifyLocal="1" labelsEnabled="0" symbologyReferenceScale="-1" simplifyDrawingHints="1" minScale="100000000" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Rendering|CustomProperties" simplifyMaxScale="1" simplifyAlgorithm="0" simplifyDrawingTol="1" hasScaleBasedVisibilityFlag="0" maxScale="0" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 type="singleSymbol" enableorderby="0" referencescale="-1" symbollevels="0" forceraster="0">
    <symbols>
      <symbol force_rhr="0" type="fill" alpha="1" clip_to_extent="1" name="0" frame_rate="10" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SimpleFill" pass="0">
          <Option type="Map">
            <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale"/>
            <Option value="166,206,227,153" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="31,120,180,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.26" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
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
        <Option value="&quot;P21A_001&quot;" type="QString"/>
      </Option>
      <Option value="0" type="int" name="embeddedWidgets/count"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="P21A_001" configurationFlags="None"/>
    <field name="P21A_002" configurationFlags="None"/>
    <field name="P21A_003" configurationFlags="None"/>
    <field name="P21A_004" configurationFlags="None"/>
    <field name="P21A_005" configurationFlags="None"/>
    <field name="検査ID" configurationFlags="None"/>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="P21A_001" name="事業主体"/>
    <alias index="1" field="P21A_002" name="事業名称"/>
    <alias index="2" field="P21A_003" name="種別"/>
    <alias index="3" field="P21A_004" name="給水人口"/>
    <alias index="4" field="P21A_005" name="日最大給水量"/>
    <alias index="5" field="検査ID" name=""/>
  </aliases>
  <defaults>
    <default field="P21A_001" applyOnUpdate="0" expression=""/>
    <default field="P21A_002" applyOnUpdate="0" expression=""/>
    <default field="P21A_003" applyOnUpdate="0" expression=""/>
    <default field="P21A_004" applyOnUpdate="0" expression=""/>
    <default field="P21A_005" applyOnUpdate="0" expression=""/>
    <default field="検査ID" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" field="P21A_001" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P21A_002" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P21A_003" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P21A_004" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P21A_005" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="検査ID" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="P21A_001" desc=""/>
    <constraint exp="" field="P21A_002" desc=""/>
    <constraint exp="" field="P21A_003" desc=""/>
    <constraint exp="" field="P21A_004" desc=""/>
    <constraint exp="" field="P21A_005" desc=""/>
    <constraint exp="" field="検査ID" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression>"P21A_001"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
