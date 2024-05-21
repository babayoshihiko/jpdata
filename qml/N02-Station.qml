<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="100000000" maxScale="0" labelsEnabled="0" version="3.28.7-Firenze" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" simplifyDrawingTol="1" simplifyMaxScale="1" simplifyLocal="1" readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Rendering" simplifyDrawingHints="1" symbologyReferenceScale="-1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0" referencescale="-1">
    <symbols>
      <symbol force_rhr="0" type="line" alpha="1" is_animated="0" frame_rate="10" name="0" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <Option type="Map">
            <Option type="QString" value="0" name="align_dash_pattern"/>
            <Option type="QString" value="square" name="capstyle"/>
            <Option type="QString" value="5;2" name="customdash"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale"/>
            <Option type="QString" value="MM" name="customdash_unit"/>
            <Option type="QString" value="0" name="dash_pattern_offset"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale"/>
            <Option type="QString" value="MM" name="dash_pattern_offset_unit"/>
            <Option type="QString" value="0" name="draw_inside_polygon"/>
            <Option type="QString" value="bevel" name="joinstyle"/>
            <Option type="QString" value="179,179,179,255" name="line_color"/>
            <Option type="QString" value="solid" name="line_style"/>
            <Option type="QString" value="3" name="line_width"/>
            <Option type="QString" value="MM" name="line_width_unit"/>
            <Option type="QString" value="0" name="offset"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="offset_map_unit_scale"/>
            <Option type="QString" value="MM" name="offset_unit"/>
            <Option type="QString" value="0" name="ring_filter"/>
            <Option type="QString" value="0" name="trim_distance_end"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale"/>
            <Option type="QString" value="MM" name="trim_distance_end_unit"/>
            <Option type="QString" value="0" name="trim_distance_start"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale"/>
            <Option type="QString" value="MM" name="trim_distance_start_unit"/>
            <Option type="QString" value="0" name="tweak_dash_pattern_on_corners"/>
            <Option type="QString" value="0" name="use_custom_dash"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="width_map_unit_scale"/>
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
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field configurationFlags="None" name="N02_001"/>
    <field configurationFlags="None" name="N02_002"/>
    <field configurationFlags="None" name="N02_003"/>
    <field configurationFlags="None" name="N02_004"/>
    <field configurationFlags="None" name="N02_005"/>
    <field configurationFlags="None" name="N02_005c"/>
    <field configurationFlags="None" name="N02_005g"/>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="N02_001" name="鉄道区分"/>
    <alias index="1" field="N02_002" name="事業者種別"/>
    <alias index="2" field="N02_003" name="路線名"/>
    <alias index="3" field="N02_004" name="運営会社"/>
    <alias index="4" field="N02_005" name="駅名"/>
    <alias index="5" field="N02_005c" name="駅コード"/>
    <alias index="6" field="N02_005g" name="グループコード"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="N02_001"/>
    <default applyOnUpdate="0" expression="" field="N02_002"/>
    <default applyOnUpdate="0" expression="" field="N02_003"/>
    <default applyOnUpdate="0" expression="" field="N02_004"/>
    <default applyOnUpdate="0" expression="" field="N02_005"/>
    <default applyOnUpdate="0" expression="" field="N02_005c"/>
    <default applyOnUpdate="0" expression="" field="N02_005g"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_001" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_002" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_003" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_004" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_005" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_005c" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="N02_005g" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="N02_001"/>
    <constraint exp="" desc="" field="N02_002"/>
    <constraint exp="" desc="" field="N02_003"/>
    <constraint exp="" desc="" field="N02_004"/>
    <constraint exp="" desc="" field="N02_005"/>
    <constraint exp="" desc="" field="N02_005c"/>
    <constraint exp="" desc="" field="N02_005g"/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression>"N02_001"</previewExpression>
  <layerGeometryType>1</layerGeometryType>
</qgis>
