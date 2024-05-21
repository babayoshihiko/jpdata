<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Rendering|CustomProperties" hasScaleBasedVisibilityFlag="0" maxScale="0" symbologyReferenceScale="-1" simplifyDrawingHints="1" simplifyAlgorithm="0" simplifyLocal="1" readOnly="0" version="3.28.7-Firenze" simplifyDrawingTol="1" minScale="100000000" labelsEnabled="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 referencescale="-1" forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol name="0" frame_rate="10" clip_to_extent="1" force_rhr="0" type="fill" alpha="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" pass="0" class="SimpleFill" enabled="1">
          <Option type="Map">
            <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="color" type="QString" value="253,191,111,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
            <Option name="outline_style" type="QString" value="no"/>
            <Option name="outline_width" type="QString" value="0.26"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
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
      <Option name="embeddedWidgets/count" type="int" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="OBJECTID" configurationFlags="None"/>
    <field name="PREFEC_CD" configurationFlags="None"/>
    <field name="AREA_CD" configurationFlags="None"/>
    <field name="CTV_NAME" configurationFlags="None"/>
    <field name="FIS_YEAR" configurationFlags="None"/>
    <field name="THEMA_NO" configurationFlags="None"/>
    <field name="LAYER_NO" configurationFlags="None"/>
    <field name="OBJ_NAME" configurationFlags="None"/>
    <field name="AREA_SIZE" configurationFlags="None"/>
    <field name="IOSIDE_DIV" configurationFlags="None"/>
    <field name="REMARK_STR" configurationFlags="None"/>
    <field name="Shape_Leng" configurationFlags="None"/>
    <field name="Shape_Area" configurationFlags="None"/>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="OBJECTID"/>
    <alias name="都道府県コード" index="1" field="PREFEC_CD"/>
    <alias name="地区コード" index="2" field="AREA_CD"/>
    <alias name="市町村名" index="3" field="CTV_NAME"/>
    <alias name="年度" index="4" field="FIS_YEAR"/>
    <alias name="主題番号" index="5" field="THEMA_NO"/>
    <alias name="レイヤ番号" index="6" field="LAYER_NO"/>
    <alias name="名称" index="7" field="OBJ_NAME"/>
    <alias name="ポリゴン面積(ha)" index="8" field="AREA_SIZE"/>
    <alias name="内外区分" index="9" field="IOSIDE_DIV"/>
    <alias name="備考" index="10" field="REMARK_STR"/>
    <alias name="" index="11" field="Shape_Leng"/>
    <alias name="" index="12" field="Shape_Area"/>
  </aliases>
  <defaults>
    <default expression="" field="OBJECTID" applyOnUpdate="0"/>
    <default expression="" field="PREFEC_CD" applyOnUpdate="0"/>
    <default expression="" field="AREA_CD" applyOnUpdate="0"/>
    <default expression="" field="CTV_NAME" applyOnUpdate="0"/>
    <default expression="" field="FIS_YEAR" applyOnUpdate="0"/>
    <default expression="" field="THEMA_NO" applyOnUpdate="0"/>
    <default expression="" field="LAYER_NO" applyOnUpdate="0"/>
    <default expression="" field="OBJ_NAME" applyOnUpdate="0"/>
    <default expression="" field="AREA_SIZE" applyOnUpdate="0"/>
    <default expression="" field="IOSIDE_DIV" applyOnUpdate="0"/>
    <default expression="" field="REMARK_STR" applyOnUpdate="0"/>
    <default expression="" field="Shape_Leng" applyOnUpdate="0"/>
    <default expression="" field="Shape_Area" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="OBJECTID" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="PREFEC_CD" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="AREA_CD" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="CTV_NAME" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="FIS_YEAR" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="THEMA_NO" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="LAYER_NO" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="OBJ_NAME" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="AREA_SIZE" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="IOSIDE_DIV" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="REMARK_STR" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="Shape_Leng" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="Shape_Area" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="OBJECTID"/>
    <constraint desc="" exp="" field="PREFEC_CD"/>
    <constraint desc="" exp="" field="AREA_CD"/>
    <constraint desc="" exp="" field="CTV_NAME"/>
    <constraint desc="" exp="" field="FIS_YEAR"/>
    <constraint desc="" exp="" field="THEMA_NO"/>
    <constraint desc="" exp="" field="LAYER_NO"/>
    <constraint desc="" exp="" field="OBJ_NAME"/>
    <constraint desc="" exp="" field="AREA_SIZE"/>
    <constraint desc="" exp="" field="IOSIDE_DIV"/>
    <constraint desc="" exp="" field="REMARK_STR"/>
    <constraint desc="" exp="" field="Shape_Leng"/>
    <constraint desc="" exp="" field="Shape_Area"/>
  </constraintExpressions>
  <expressionfields/>
  <previewExpression>"CTV_NAME"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
