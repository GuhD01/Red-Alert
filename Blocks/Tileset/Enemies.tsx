<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="Enemies" tilewidth="128" tileheight="128" tilecount="3" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <image width="128" height="128" source="../../Assets/Water/1.png"/>
 </tile>
 <tile id="1">
  <image width="70" height="70" source="../../Assets/Enemies/Spike_Up.png"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="35" y="0">
    <polygon points="0,0 35,49.7 -35,49.7"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="2">
  <properties>
   <property name="radius" type="float" value="61"/>
  </properties>
  <image width="98" height="98" source="../../Assets/Enemies/Saw/0.png"/>
 </tile>
</tileset>
