<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" readOnly="0" version="3.28.7-Firenze" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Rendering|CustomProperties" minScale="50000" hasScaleBasedVisibilityFlag="1" simplifyDrawingHints="0" simplifyDrawingTol="1" simplifyAlgorithm="0" symbologyReferenceScale="-1" simplifyLocal="1" labelsEnabled="0" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" referencescale="-1" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol alpha="1" force_rhr="0" type="marker" frame_rate="10" name="0" is_animated="0" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
          <Option type="Map">
            <Option type="QString" name="angle" value="180"/>
            <Option type="QString" name="cap_style" value="square"/>
            <Option type="QString" name="color" value="225,89,137,255"/>
            <Option type="QString" name="horizontal_anchor_point" value="1"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="name" value="half_arc"/>
            <Option type="QString" name="offset" value="0,5"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="35,35,35,255"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0.8"/>
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="scale_method" value="diameter"/>
            <Option type="QString" name="size" value="8"/>
            <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="size_unit" value="MM"/>
            <Option type="QString" name="vertical_anchor_point" value="1"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
          <Option type="Map">
            <Option type="QString" name="angle" value="0"/>
            <Option type="QString" name="cap_style" value="square"/>
            <Option type="QString" name="color" value="255,0,0,255"/>
            <Option type="QString" name="horizontal_anchor_point" value="1"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="name" value="line"/>
            <Option type="QString" name="offset" value="0,1.99999999999999978"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="35,35,35,255"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0.8"/>
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="scale_method" value="diameter"/>
            <Option type="QString" name="size" value="6"/>
            <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="size_unit" value="MM"/>
            <Option type="QString" name="vertical_anchor_point" value="1"/>
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
      <Option type="int" name="embeddedWidgets/count" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="P17_001" configurationFlags="None"/>
    <field name="P17_002" configurationFlags="None"/>
    <field name="P17_003" configurationFlags="None"/>
    <field name="P17_004" configurationFlags="None"/>
  </fieldConfiguration>
  <aliases>
    <alias field="P17_001" index="0" name="名称"/>
    <alias field="P17_002" index="1" name="行政区域コード"/>
    <alias field="P17_003" index="2" name="種別コード"/>
    <alias field="P17_004" index="3" name="所在地"/>
  </aliases>
  <defaults>
    <default field="P17_001" applyOnUpdate="0" expression=""/>
    <default field="P17_002" applyOnUpdate="0" expression=""/>
    <default field="P17_003" applyOnUpdate="0" expression=""/>
    <default field="P17_004" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" field="P17_001" notnull_strength="0" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" field="P17_002" notnull_strength="0" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" field="P17_003" notnull_strength="0" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" field="P17_004" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="P17_001" desc=""/>
    <constraint exp="" field="P17_002" desc=""/>
    <constraint exp="" field="P17_003" desc=""/>
    <constraint exp="" field="P17_004" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression>"P17_001"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
