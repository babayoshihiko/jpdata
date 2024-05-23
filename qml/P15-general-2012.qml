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
      <symbol force_rhr="0" type="marker" alpha="1" clip_to_extent="1" name="0" frame_rate="10" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SvgMarker" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="225,89,137,255" type="QString" name="color"/>
            <Option value="0" type="QString" name="fixedAspectRatio"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value=PLUGIN_DIR/jpdata/qml/Japanese_Map_symbol_(Chimney).svg" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255" type="QString" name="outline_color"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option name="parameters"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="7" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
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
    <Option/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="P15_001" configurationFlags="None"/>
    <field name="P15_002" configurationFlags="None"/>
    <field name="P15_003" configurationFlags="None"/>
    <field name="P15_004" configurationFlags="None"/>
    <field name="P15_005" configurationFlags="None"/>
    <field name="P15_006" configurationFlags="None"/>
    <field name="P15_007" configurationFlags="None"/>
    <field name="P15_008" configurationFlags="None"/>
    <field name="P15_009" configurationFlags="None"/>
    <field name="P15_010" configurationFlags="None"/>
    <field name="P15_011" configurationFlags="None"/>
    <field name="P15_012" configurationFlags="None"/>
    <field name="P15_013" configurationFlags="None"/>
    <field name="P15_014" configurationFlags="None"/>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="P15_001" name="施設名称"/>
    <alias index="1" field="P15_002" name="地方公共団体名"/>
    <alias index="2" field="P15_003" name="施設種別"/>
    <alias index="3" field="P15_004" name="施設タイプ"/>
    <alias index="4" field="P15_005" name="処理能力（t/日）"/>
    <alias index="5" field="P15_006" name="屋内面積"/>
    <alias index="6" field="P15_007" name="屋外面積"/>
    <alias index="7" field="P15_008" name="全体容量"/>
    <alias index="8" field="P15_009" name="処理能力（kL/日）"/>
    <alias index="9" field="P15_010" name="計画最大汚水量"/>
    <alias index="10" field="P15_011" name="処理物"/>
    <alias index="11" field="P15_012" name="処理方式"/>
    <alias index="12" field="P15_013" name="炉形式"/>
    <alias index="13" field="P15_014" name="発電能力"/>
  </aliases>
  <defaults>
    <default field="P15_001" applyOnUpdate="0" expression=""/>
    <default field="P15_002" applyOnUpdate="0" expression=""/>
    <default field="P15_003" applyOnUpdate="0" expression=""/>
    <default field="P15_004" applyOnUpdate="0" expression=""/>
    <default field="P15_005" applyOnUpdate="0" expression=""/>
    <default field="P15_006" applyOnUpdate="0" expression=""/>
    <default field="P15_007" applyOnUpdate="0" expression=""/>
    <default field="P15_008" applyOnUpdate="0" expression=""/>
    <default field="P15_009" applyOnUpdate="0" expression=""/>
    <default field="P15_010" applyOnUpdate="0" expression=""/>
    <default field="P15_011" applyOnUpdate="0" expression=""/>
    <default field="P15_012" applyOnUpdate="0" expression=""/>
    <default field="P15_013" applyOnUpdate="0" expression=""/>
    <default field="P15_014" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" field="P15_001" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_002" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_003" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_004" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_005" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_006" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_007" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_008" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_009" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_010" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_011" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_012" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_013" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="P15_014" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="P15_001" desc=""/>
    <constraint exp="" field="P15_002" desc=""/>
    <constraint exp="" field="P15_003" desc=""/>
    <constraint exp="" field="P15_004" desc=""/>
    <constraint exp="" field="P15_005" desc=""/>
    <constraint exp="" field="P15_006" desc=""/>
    <constraint exp="" field="P15_007" desc=""/>
    <constraint exp="" field="P15_008" desc=""/>
    <constraint exp="" field="P15_009" desc=""/>
    <constraint exp="" field="P15_010" desc=""/>
    <constraint exp="" field="P15_011" desc=""/>
    <constraint exp="" field="P15_012" desc=""/>
    <constraint exp="" field="P15_013" desc=""/>
    <constraint exp="" field="P15_014" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression></previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
