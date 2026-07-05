<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.44.10-Solothurn" styleCategories="LayerConfiguration|Symbology|Fields">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 attr="" graduatedMethod="GraduatedColor" referencescale="-1" enableorderby="0" type="graduatedSymbol" forceraster="0" symbollevels="0">
    <ranges/>
    <symbols/>
    <source-symbol>
      <symbol force_rhr="0" is_animated="0" clip_to_extent="1" alpha="1" type="fill" frame_rate="10" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" id="{cbcce65b-d36a-44a2-b64a-2edd0b507599}" class="SimpleFill" locked="0" pass="0">
          <Option type="Map">
            <Option type="QString" value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale"/>
            <Option type="QString" value="196,60,57,255,rgb:0.7686275,0.2352941,0.2235294,1" name="color"/>
            <Option type="QString" value="bevel" name="joinstyle"/>
            <Option type="QString" value="0,0" name="offset"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="offset_map_unit_scale"/>
            <Option type="QString" value="MM" name="offset_unit"/>
            <Option type="QString" value="35,35,35,255,rgb:0.1372549,0.1372549,0.1372549,1" name="outline_color"/>
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
    </source-symbol>
    <colorramp type="gradient" name="[source]">
      <Option type="Map">
        <Option type="QString" value="255,255,255,255,rgb:1,1,1,1" name="color1"/>
        <Option type="QString" value="255,0,0,255,rgb:1,0,0,1" name="color2"/>
        <Option type="QString" value="ccw" name="direction"/>
        <Option type="QString" value="0" name="discrete"/>
        <Option type="QString" value="gradient" name="rampType"/>
        <Option type="QString" value="rgb" name="spec"/>
      </Option>
    </colorramp>
    <classificationMethod id="Fixed">
      <symmetricMode enabled="0" symmetrypoint="0" astride="0"/>
      <labelFormat format="%1 - %2" trimtrailingzeroes="1" labelprecision="4"/>
      <parameters>
        <Option type="Map">
          <Option type="double" value="10" name="INTERVAL"/>
        </Option>
      </parameters>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
    <data-defined-properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </data-defined-properties>
  </renderer-v2>
  <selection mode="Default">
    <selectionColor invalid="1"/>
    <selectionSymbol>
      <symbol force_rhr="0" is_animated="0" clip_to_extent="1" alpha="1" type="fill" frame_rate="10" name="">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" id="{9425f694-1d09-414f-b718-d23ff76a698a}" class="SimpleFill" locked="0" pass="0">
          <Option type="Map">
            <Option type="QString" value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale"/>
            <Option type="QString" value="0,0,255,255,rgb:0,0,1,1" name="color"/>
            <Option type="QString" value="bevel" name="joinstyle"/>
            <Option type="QString" value="0,0" name="offset"/>
            <Option type="QString" value="3x:0,0,0,0,0,0" name="offset_map_unit_scale"/>
            <Option type="QString" value="MM" name="offset_unit"/>
            <Option type="QString" value="35,35,35,255,rgb:0.1372549,0.1372549,0.1372549,1" name="outline_color"/>
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
    </selectionSymbol>
  </selection>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field configurationFlags="NoFlag" name="P09_001"/>
    <field configurationFlags="NoFlag" name="P09_002"/>
    <field configurationFlags="NoFlag" name="P09_003"/>
    <field configurationFlags="NoFlag" name="P09_004"/>
    <field configurationFlags="NoFlag" name="P09_005"/>
    <field configurationFlags="NoFlag" name="P09_006"/>
    <field configurationFlags="NoFlag" name="P09_007"/>
    <field configurationFlags="NoFlag" name="P09_008"/>
    <field configurationFlags="NoFlag" name="P09_009"/>
    <field configurationFlags="NoFlag" name="P09_010"/>
    <field configurationFlags="NoFlag" name="P09_011"/>
    <field configurationFlags="NoFlag" name="P09_012"/>
    <field configurationFlags="NoFlag" name="P09_013"/>
    <field configurationFlags="NoFlag" name="P09_014"/>
    <field configurationFlags="NoFlag" name="Capacity"/>
  </fieldConfiguration>
  <aliases>
    <alias field="P09_001" index="0" name="3次メッシュコード"/>
    <alias field="P09_002" index="1" name="施設数（ホテル）"/>
    <alias field="P09_003" index="2" name="施設数（旅館）"/>
    <alias field="P09_004" index="3" name="施設数（公共宿泊施設）"/>
    <alias field="P09_005" index="4" name="施設数（民宿）"/>
    <alias field="P09_006" index="5" name="施設数（ペンション）"/>
    <alias field="P09_007" index="6" name="施設数（宿坊）"/>
    <alias field="P09_008" index="7" name="施設数（コテージ・貸し別荘・山荘）"/>
    <alias field="P09_009" index="8" name="施設数（ユースホステル）"/>
    <alias field="P09_010" index="9" name="施設数（カプセルホテル）"/>
    <alias field="P09_011" index="10" name="施設数（研修センター）"/>
    <alias field="P09_012" index="11" name="施設総数"/>
    <alias field="P09_013" index="12" name="収容人数"/>
    <alias field="P09_014" index="13" name="客室数"/>
    <alias field="Capacity" index="14" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="P09_001"/>
    <default expression="" applyOnUpdate="0" field="P09_002"/>
    <default expression="" applyOnUpdate="0" field="P09_003"/>
    <default expression="" applyOnUpdate="0" field="P09_004"/>
    <default expression="" applyOnUpdate="0" field="P09_005"/>
    <default expression="" applyOnUpdate="0" field="P09_006"/>
    <default expression="" applyOnUpdate="0" field="P09_007"/>
    <default expression="" applyOnUpdate="0" field="P09_008"/>
    <default expression="" applyOnUpdate="0" field="P09_009"/>
    <default expression="" applyOnUpdate="0" field="P09_010"/>
    <default expression="" applyOnUpdate="0" field="P09_011"/>
    <default expression="" applyOnUpdate="0" field="P09_012"/>
    <default expression="" applyOnUpdate="0" field="P09_013"/>
    <default expression="" applyOnUpdate="0" field="P09_014"/>
    <default expression="" applyOnUpdate="0" field="Capacity"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" exp_strength="0" field="P09_001" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_002" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_003" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_004" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_005" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_006" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_007" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_008" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_009" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_010" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_011" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_012" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_013" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="P09_014" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="Capacity" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="P09_001" desc=""/>
    <constraint exp="" field="P09_002" desc=""/>
    <constraint exp="" field="P09_003" desc=""/>
    <constraint exp="" field="P09_004" desc=""/>
    <constraint exp="" field="P09_005" desc=""/>
    <constraint exp="" field="P09_006" desc=""/>
    <constraint exp="" field="P09_007" desc=""/>
    <constraint exp="" field="P09_008" desc=""/>
    <constraint exp="" field="P09_009" desc=""/>
    <constraint exp="" field="P09_010" desc=""/>
    <constraint exp="" field="P09_011" desc=""/>
    <constraint exp="" field="P09_012" desc=""/>
    <constraint exp="" field="P09_013" desc=""/>
    <constraint exp="" field="P09_014" desc=""/>
    <constraint exp="" field="Capacity" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field subType="0" typeName="integer" comment="" precision="0" expression="to_int( &quot;P09_014&quot; )" type="2" length="10" name="Capacity"/>
  </expressionfields>
  <previewExpression>COALESCE( "P09_001", '&lt;NULL>' )</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
