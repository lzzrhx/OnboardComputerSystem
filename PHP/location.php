<?php

//Requires a Google Maps API key to work
//Replace "perpetual.voyage" with your website
//And "if-location" with the url

$db = new SQLite3('db/location.db');
$google_maps_api_key='YOUR API KEY HERE';

//Generate .kml file
$expl_url=explode("if-location/",$url,2);$expl_url=$expl_url[1];
if($expl_url=='location_history.kml'){
echo"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n";
echo"<kml xmlns=\"http://earth.google.com/kml/2.1\">\r\n";
echo"  <Document>\r\n";
echo"    <name>location_history</name>\r\n";
echo"    <description>location_history</description>\r\n";
echo"\r\n";
echo"    <Style id=\"line01\">\r\n";
echo"      <LineStyle>\r\n";
echo"        <color>ff494886</color>\r\n";
echo"        <width>4</width>\r\n";
echo"      </LineStyle>\r\n";
echo"	</Style>\r\n";
echo"\r\n";
echo"    <Placemark>\r\n";
echo"      <name>line</name>\r\n";
echo"      <styleUrl>#line01</styleUrl>\r\n";
echo"      <LineString>\r\n";
echo"        <altitudeMode>relative</altitudeMode>\r\n";
echo"        <coordinates>\r\n";
echo"\r\n";
$gps_count=1;
$results = $db->query('SELECT * FROM LOCATION ORDER BY ID DESC');
while ($row = $results->fetchArray()) {
$gps_num=$row[0];$ocs_time=$row[1];$gps_lat=$row[2];$gps_lon=$row[3];$gps_speed=$row[4];$ocs_cog=$row[5];
if($gps_count!=1){echo"\r\n";}echo $gps_lon.','.$gps_lat.',0';$gps_count++;}
echo"\r\n";
echo"        </coordinates>\r\n";
echo"      </LineString>\r\n";
echo"    </Placemark>\r\n";
echo"\r\n";
echo"  </Document>\r\n";
echo"</kml>";
}else{

//Show map
echo'<div id="map_embed"><div id="map"></div></div>';
echo'<script>';
echo'function initMap() {';
echo'  var map = new google.maps.Map(document.getElementById(\'map\'), {';
echo'    zoom: 7,';
echo'    center: {lat: 59.0, lng: 10.0}';
echo'  });';
echo'  var ctaLayer = new google.maps.KmlLayer({';
echo'    url: \'http://perpetual.voyage/if-location/location_history.kml\',';
echo'    map: map';
echo'  });';
echo'}';
echo'</script>';
echo'<script async defer src="https://maps.googleapis.com/maps/api/js?key='.$google_maps_api_key.'&signed_in=true&callback=initMap"></script>';

//Location history
echo'<div class="content">';
$count=1;
$results = $db->query('SELECT * FROM LOCATION ORDER BY ID DESC');
while ($row = $results->fetchArray()) {
$ocs_num=$row["ID"];
$ocs_time=$row["TIME"];
$ocs_lat=$row["LAT"];
$ocs_lon=$row["LON"];
$ocs_speed=$row["SPD"];
$ocs_cog=$row["COG"];
$ocs_hdg=$row["HDG"];
$ocs_clinox=$row["CLINOX"];
$ocs_clinoy=$row["CLINOY"];
$ocs_dist=$row["DIST"];
//Format time
$ocs_time_format=date('d.m.Y H:i', $ocs_time);
#Format latitude
$ocs_lat_expl=explode(".",$ocs_lat);$ocs_lat_deg=$ocs_lat_expl[0];$ocs_lat_min=$ocs_lat_expl[1];
if(substr($ocs_lat_deg,0,1)=="-"){$ocs_lat_dir='S';$ocs_lat_deg2=substr($ocs_lat_deg,1);}else{$ocs_lat_dir='N';$ocs_lat_deg2=$ocs_lat_deg;};
$ocs_lat_min=('0.'.$ocs_lat_min)*60;
$ocs_lat_min=sprintf("%06.3f", $ocs_lat_min);
$ocs_lat_format=$ocs_lat_deg2.'° '.$ocs_lat_min.'\''.$ocs_lat_dir;
#Format longitude
$ocs_lon_expl=explode(".",$ocs_lon);$ocs_lon_deg=$ocs_lon_expl[0];$ocs_lon_min=$ocs_lon_expl[1];
if(substr($ocs_lon_deg,0,1)=="-"){$ocs_lon_dir='W';$ocs_lon_deg2=substr($ocs_lon_deg,1);}else{$ocs_lon_dir='E';$ocs_lon_deg2=$ocs_lon_deg;};
$ocs_lon_min=('0.'.$ocs_lon_min)*60;
$ocs_lon_min=sprintf("%06.3f", $ocs_lon_min);
$ocs_lon_format=$ocs_lon_deg2.'° '.$ocs_lon_min.'\''.$ocs_lon_dir;
#Format speed
$ocs_speed_format=number_format(($ocs_speed*1.9438444924574),1).' KN';
#Format course
$ocs_cog_format=sprintf("%03d", $ocs_cog).'°';
//Format heading
$ocs_hdg_format=sprintf("%03d", $ocs_hdg).'°';
//Format clinometer (X axis)
if(substr($ocs_clinox,0,1)=="-"){$ocs_clinox_dir='starboard';$ocs_clinox=substr($ocs_clinox,1);}else{$ocs_clinox_dir='port';};
$ocs_clinox_format=round($ocs_clinox).'°';
//Format clinometer (Y axis)
if(substr($ocs_clinoy,0,1)=="-"){$ocs_clinoy_dir='forward';$ocs_clinoy=substr($ocs_clinoy,1);}else{$ocs_clinoy_dir='backward';};
$ocs_clinoy_format=round($ocs_clinoy).'°';
//Format distance
$ocs_dist_format=number_format(($ocs_dist*0.000539956803),1).' NM';
#Format google maps link
$ocs_location_link='https://www.google.no/maps/search/'.$ocs_lat_deg.'+'.$ocs_lat_min.',+'.$ocs_lon_deg.'+'.$ocs_lon_min.'';
#Print data
if($count>1){echo'<div class="seperator_small"></div>';}
echo'<div class="gps_item">';
echo'<p><a target="_blank" href="'.$ocs_location_link.'">Entry no. '.sprintf('%04d', $ocs_num).'&nbsp;&nbsp;&#8226;&nbsp;&nbsp;'.$ocs_time_format.'</a></p>';
echo'<p>LAT: '.$ocs_lat_format.'&nbsp;&nbsp; // &nbsp;&nbsp;LON: '.$ocs_lon_format.'&nbsp;&nbsp; // &nbsp;&nbsp;SPD: '.$ocs_speed_format.'&nbsp;&nbsp; // &nbsp;&nbsp;COG: '.$ocs_cog_format.'&nbsp;&nbsp; // &nbsp;&nbsp;CLINO: '.$ocs_clinox_format.'&nbsp;&nbsp; // &nbsp;&nbsp;LOG: '.$ocs_dist_format.'</p>';
echo'</div>';$count++;}
echo'</div>';

?>
