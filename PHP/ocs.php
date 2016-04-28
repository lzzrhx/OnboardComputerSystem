<?php

//Last.fm intergration requires https://github.com/erikjansson/Now-Playing

//Last.fm
require_once 'incl/lastfm.php';
$lastfm_user='Zeph0n';
$lastfm_key='afe5ef00fe3c06f26ccc8b7a155e7a6c';
$lastfm_secret='3cc0c6415002fdbaf8c3689e4c2969bb';
$nowPlaying = new NowPlaying($lastfm_user,$lastfm_key);
$nowPlaying->setNoTrackPlayingMessage('-');
$lastfm=$nowPlaying->getNowPlaying();

//Onboard Computer System
$db = new SQLite3('db/ocs.db');
$results = $db->query('SELECT * FROM OCS LIMIT 1');
while ($row = $results->fetchArray()) {
$ocs_time=$row["TIME"];
$ocs_lat=$row["LAT"];
$ocs_lon=$row["LON"];
$ocs_spd=$row["SPD"];
$ocs_spd_max=$row["SPD_MAX"];
$ocs_cog=$row["COG"];
$ocs_hdg=$row["HDG"];
$ocs_uptime=$row["UPTIME"];
$ocs_uptime_max=$row["UPTIME_MAX"];
$ocs_dist=$row["DIST"];
$ocs_dist_start=$row["DIST_START"];
$ocs_baro=$row["BARO"];
$ocs_temp1=$row["TEMP1"];
$ocs_temp2=$row["TEMP2"];
$ocs_temp3=$row["TEMP3"];
$ocs_clinox=$row["CLINOX"];
$ocs_clinox_min=$row["CLINOX_MIN"];
$ocs_clinox_max=$row["CLINOX_MAX"];
$ocs_clinoy=$row["CLINOY"];
$ocs_clinoy_min=$row["CLINOY_MIN"];
$ocs_clinoy_max=$row["CLINOY_MAX"];
$ocs_winddir=$row["WINDDIR"];
$ocs_windspd=$row["WINDSPD"];
$ocs_sunrise=$row["SUNRISE"];
$ocs_sunset=$row["SUNSET"];
//Format time
$ocs_time_format=date('d.m.Y H:i', $ocs_time);
//Format latitude
$ocs_lat_expl=explode(".",$ocs_lat);$ocs_lat_deg=$ocs_lat_expl[0];$ocs_lat_min=$ocs_lat_expl[1];
if(substr($ocs_lat_deg,0,1)=="-"){$ocs_lat_dir='S';$ocs_lat_deg2=substr($ocs_lat_deg,1);}else{$ocs_lat_dir='N';$ocs_lat_deg2=$ocs_lat_deg;};
$ocs_lat_min=('0.'.$ocs_lat_min)*60;
$ocs_lat_min=sprintf("%06.3f", $ocs_lat_min);
$ocs_lat_format=$ocs_lat_deg2.'° '.$ocs_lat_min.'\''.$ocs_lat_dir;
//Format longitude
$ocs_lon_expl=explode(".",$ocs_lon);$ocs_lon_deg=$ocs_lon_expl[0];$ocs_lon_min=$ocs_lon_expl[1];
if(substr($ocs_lon_deg,0,1)=="-"){$ocs_lon_dir='W';$ocs_lon_deg2=substr($ocs_lon_deg,1);}else{$ocs_lon_dir='E';$ocs_lon_deg2=$ocs_lon_deg;};
$ocs_lon_min=('0.'.$ocs_lon_min)*60;
$ocs_lon_min=sprintf("%06.3f", $ocs_lon_min);
$ocs_lon_format=$ocs_lon_deg2.'° '.$ocs_lon_min.'\''.$ocs_lon_dir;
//Format speed
$ocs_spd_format=number_format(($ocs_spd*1.9438444924574),1).' KN';
$ocs_spd_max_format=number_format(($ocs_spd_max*1.9438444924574),1).' KN';
//Format course
$ocs_cog_format=round($ocs_cog).'°';
//Format uptime
$ocs_uptime_days = floor($ocs_uptime/60/60/24);$ocs_uptime_days=str_pad($ocs_uptime_days, 2, "0", STR_PAD_LEFT);
$ocs_uptime_hours = floor(($ocs_uptime - $ocs_uptime_days*24*60*60)/60/60);$ocs_uptime_hours=str_pad($ocs_uptime_hours, 2, "0", STR_PAD_LEFT);
$ocs_uptime_minutes = floor(($ocs_uptime - $ocs_uptime_days*24*60*60 - $ocs_uptime_hours*60*60)/60);$ocs_uptime_minutes=str_pad($ocs_uptime_minutes, 2, "0", STR_PAD_LEFT);
$ocs_uptime_format=$ocs_uptime_days.' days - '.$ocs_uptime_hours.' hours - '.$ocs_uptime_minutes.' minutes';
//Format max uptime
$ocs_uptime_max_days = floor($ocs_uptime_max/60/60/24);$ocs_uptime_max_days=str_pad($ocs_uptime_max_days, 2, "0", STR_PAD_LEFT);
$ocs_uptime_max_hours = floor(($ocs_uptime_max - $ocs_uptime_max_days*24*60*60)/60/60);$ocs_uptime_max_hours=str_pad($ocs_uptime_max_hours, 2, "0", STR_PAD_LEFT);
$ocs_uptime_max_minutes = floor(($ocs_uptime_max - $ocs_uptime_max_days*24*60*60 - $ocs_uptime_max_hours*60*60)/60);$ocs_uptime_max_minutes=str_pad($ocs_uptime_max_minutes, 2, "0", STR_PAD_LEFT);
$ocs_uptime_max_format=$ocs_uptime_max_days.' days - '.$ocs_uptime_max_hours.' hours - '.$ocs_uptime_max_minutes.' minutes';
//Format heading
$ocs_hdg_format=round($ocs_hdg).'°';
//Format clinometer (X axis)
if(substr($ocs_clinox,0,1)=="-"){$ocs_clinox_dir='starboard';$ocs_clinox=substr($ocs_clinox,1);}else{$ocs_clinox_dir='port';};
$ocs_clinox_format=round($ocs_clinox).'°';
if(substr($ocs_clinox_min,0,1)=="-"){$ocs_clinox_min=substr($ocs_clinox_min,1);}
if($ocs_clinox_max<$ocs_clinox_min){$ocs_clinox_max=$ocs_clinox_min;$ocs_clinox_max_dir='starboard';}else{$ocs_clinox_max_dir='port';}
$ocs_clinox_max_format=round($ocs_clinox_max).'°';
//Format clinometer (Y axis)
if(substr($ocs_clinoy,0,1)=="-"){$ocs_clinoy_dir='forward';$ocs_clinoy=substr($ocs_clinoy,1);}else{$ocs_clinoy_dir='backward';};
$ocs_clinoy_format=round($ocs_clinoy).'°';
if(substr($ocs_clinoy_min,0,1)=="-"){$ocs_clinoy_min=substr($ocs_clinoy_min,1);}
if($ocs_clinoy_max<$ocs_clinoy_min){$ocs_clinoy_max=$ocs_clinoy_min;$ocs_clinoy_max_dir='forward';}else{$ocs_clinoy_max_dir='backward';}
$ocs_clinoy_max_format=round($ocs_clinoy_max).'°';
//Format distance
$ocs_dist_total=$ocs_dist+$ocs_dist_start;
$ocs_dist_total_format=number_format(($ocs_dist_total*0.000539956803),1).' NM';
//Format barometer
$ocs_baro_format=round(($ocs_baro/100)).' mbar';
//Format temp1
$ocs_temp1_format=number_format($ocs_temp1,1).' °C';
//Format temp2
$ocs_temp2_format=number_format($ocs_temp2,1).' °C';
//Format temp3
$ocs_temp3_format=number_format($ocs_temp3,1).' °C';
//Format wind
$ocs_winddir_format=round($ocs_winddir).'°';
$ocs_windspd_format=number_format($ocs_windspd,1).' MS';
$ocs_wind_format=$ocs_winddir_format.' '.$ocs_windspd_format;
//Format google maps link
$ocs_location='https://www.google.no/maps/search/'.$ocs_lat_deg.'+'.$ocs_lat_min.',+'.$ocs_lon_deg.'+'.$ocs_lon_min.'';
}

//Print data
echo'<div class="onboard_computer_system">';
echo'<div class="onboard_computer_system_title">--------------------------------------------------------------</div>';
echo'<div class="onboard_computer_system_title">* O N B O A R D * C O M P U T E R * S Y S T E M *</div>';
echo'<div class="onboard_computer_system_title">--------------------------------------------------------------</div>';
echo'<p class="link_text"><a href="/if-camera">Camera</a>&nbsp;&nbsp;&#8226;&nbsp;&nbsp;<a href="/if-location">Location history</a>&nbsp;&nbsp;&#8226;&nbsp;&nbsp;<a href="/if-weather">Weather history</a></p>';
if ($lastfm!='-'){echo'<p>[ NOW PLAYING: '.$lastfm.' ]</p>';}
echo'<p>LAT: '.$ocs_lat_format.'&nbsp;&nbsp; // &nbsp;&nbsp;LON: '.$ocs_lon_format.'&nbsp;&nbsp; // &nbsp;&nbsp;<span title="MAX: '.$ocs_spd_max_format.'">SPD: '.$ocs_spd_format.'</span>&nbsp;&nbsp; // &nbsp;&nbsp;COG: '.$ocs_cog_format.'</p>';
echo'<p><span title="MAX: '.$ocs_clinox_max_format.'">CLINO: '.$ocs_clinox_format.'</span>&nbsp;&nbsp; // &nbsp;&nbsp;HDG: '.$ocs_hdg_format.'&nbsp;&nbsp; // &nbsp;&nbsp;LOG: '.$ocs_dist_total_format.'&nbsp;&nbsp; // &nbsp;&nbsp;WIND: '.$ocs_wind_format.'</p>';
echo'<p>BARO: '.$ocs_baro_format.'&nbsp;&nbsp; // &nbsp;&nbsp;INSIDE: '.$ocs_temp1_format.'&nbsp;&nbsp; // &nbsp;&nbsp;OUTSIDE: '.$ocs_temp2_format.'&nbsp;&nbsp; // &nbsp;&nbsp;WATER: '.$ocs_temp3_format.'</p>';
echo'<div class="onboard_computer_system_title">--------------------------------------------------------------</div>';
echo'<p>UPDATED: '.$ocs_time_format.'&nbsp;&nbsp; // &nbsp;&nbsp;<span title="MAX: '.$ocs_uptime_max_format.'">UPTIME: '.$ocs_uptime_format.'</span></p>';
echo'<div class="onboard_computer_system_title">--------------------------------------------------------------</div>';
echo'</div>';

?>
