<?php

//Requires Chart.js (http://www.chartjs.org/) to work

//Stats
$db = new SQLite3('db/ocs.db');
$results = $db->query('SELECT * FROM OCS LIMIT 1');
while ($row = $results->fetchArray()) {
$ocs_baromin=$row[13];
$ocs_baromax=$row[14];
$ocs_temp1min=$row[16];
$ocs_temp1max=$row[17];
$ocs_temp2min=$row[19];
$ocs_temp2max=$row[20];
$ocs_temp3min=$row[22];
$ocs_temp3max=$row[23];
//Format barometer
$ocs_baromin_format=round($ocs_baromin/100).' mbar';
$ocs_baromax_format=round($ocs_baromax/100).' mbar';
//Format temp1
$ocs_temp1min_format=number_format($ocs_temp1min,1).' °C';
$ocs_temp1max_format=number_format($ocs_temp1max,1).' °C';
//Format temp2
$ocs_temp2min_format=number_format($ocs_temp2min,1).' °C';
$ocs_temp2max_format=number_format($ocs_temp2max,1).' °C';
//Format temp3
$ocs_temp3min_format=number_format($ocs_temp3min,1).' °C';
$ocs_temp3max_format=number_format($ocs_temp3max,1).' °C';
}

//Get weater data (hours)
$count=1;
$db = new SQLite3('db/weather.db');
$results = $db->query('SELECT * FROM (SELECT * FROM WEATHER ORDER BY ID DESC LIMIT 50) ORDER BY ID ASC');
while ($row = $results->fetchArray()) {
//$ocs_num=$row["ID"];
$ocs_time=$row["TIME"];
$ocs_baro=$row["BARO"];
$ocs_temp1=$row["TEMP1"];
$ocs_temp2=$row["TEMP2"];
$ocs_temp3=$row["TEMP3"];
$ocs_time_format=strtoupper(date('d. M H:i', $ocs_time));
$ocs_baro_format=($ocs_baro/100);
$ocs_temp1_format=$ocs_temp1;
$ocs_temp2_format=$ocs_temp2;
$ocs_temp3_format=$ocs_temp3;
if($count>1){
$weather_labels_hours.=',';
$weather_baro_data_hours.=',';
$weather_temp1_data_hours.=',';
$weather_temp2_data_hours.=',';
$weather_temp3_data_hours.=',';}
$weather_labels_hours.='"'.$ocs_time_format.'"';
$weather_baro_data_hours.=$ocs_baro_format;
$weather_temp1_data_hours.=$ocs_temp1_format;
$weather_temp2_data_hours.=$ocs_temp2_format;
$weather_temp3_data_hours.=$ocs_temp3_format;
$count++;}

//Get weater data (days)
$count=1;
$db = new SQLite3('db/weather.db');
$results = $db->query('SELECT * FROM (SELECT ID, AVG(TIME), AVG(BARO), AVG(TEMP1), AVG(TEMP2), AVG(TEMP3) FROM WEATHER GROUP BY strftime("%Y-%m-%d",TIME,"unixepoch") ORDER BY ID DESC LIMIT 50) ORDER BY ID ASC');
while ($row = $results->fetchArray()) {
$ocs_time=$row["AVG(TIME)"];
$ocs_baro=$row["AVG(BARO)"];
$ocs_temp1=$row["AVG(TEMP1)"];
$ocs_temp2=$row["AVG(TEMP2)"];
$ocs_temp3=$row["AVG(TEMP3)"];
$ocs_time_format=strtoupper(date('d. M', $ocs_time));
$ocs_baro_format=($ocs_baro/100);
$ocs_temp1_format=$ocs_temp1;
$ocs_temp2_format=$ocs_temp2;
$ocs_temp3_format=$ocs_temp3;
if($count>1){
$weather_labels_days.=',';
$weather_baro_data_days.=',';
$weather_temp1_data_days.=',';
$weather_temp2_data_days.=',';
$weather_temp3_data_days.=',';}
$weather_labels_days.='"'.$ocs_time_format.'"';
$weather_baro_data_days.=$ocs_baro_format;
$weather_temp1_data_days.=$ocs_temp1_format;
$weather_temp2_data_days.=$ocs_temp2_format;
$weather_temp3_data_days.=$ocs_temp3_format;
$count++;}

//Get weater data (months)
$count=1;
$db = new SQLite3('db/weather.db');
$results = $db->query('SELECT * FROM (SELECT ID, AVG(TIME), AVG(BARO), AVG(TEMP1), AVG(TEMP2), AVG(TEMP3) FROM WEATHER GROUP BY strftime("%Y-%m",TIME,"unixepoch") ORDER BY ID DESC LIMIT 50) ORDER BY ID ASC');
while ($row = $results->fetchArray()) {
$ocs_time=$row["AVG(TIME)"];
$ocs_baro=$row["AVG(BARO)"];
$ocs_temp1=$row["AVG(TEMP1)"];
$ocs_temp2=$row["AVG(TEMP2)"];
$ocs_temp3=$row["AVG(TEMP3)"];
$ocs_time_format=strtoupper(date('F Y', $ocs_time));
$ocs_baro_format=($ocs_baro/100);
$ocs_temp1_format=$ocs_temp1;
$ocs_temp2_format=$ocs_temp2;
$ocs_temp3_format=$ocs_temp3;
if($count>1){
$weather_labels_months.=',';
$weather_baro_data_months.=',';
$weather_temp1_data_months.=',';
$weather_temp2_data_months.=',';
$weather_temp3_data_months.=',';}
$weather_labels_months.='"'.$ocs_time_format.'"';
$weather_baro_data_months.=$ocs_baro_format;
$weather_temp1_data_months.=$ocs_temp1_format;
$weather_temp2_data_months.=$ocs_temp2_format;
$weather_temp3_data_months.=$ocs_temp3_format;
$count++;}

#Colors
$weather_color_white_hex='#A9A28F';list($weather_color_white_r, $weather_color_white_g, $weather_color_white_b) = sscanf($weather_color_white_hex, "#%02x%02x%02x");$weather_color_white_rgb=$weather_color_whiter.','.$weather_color_whiteg.','.$weather_color_whiteb;$weather_color_white_rgba=$weather_color_white_rgb.',1';
$weather_color_black_hex='#303030';list($weather_color_black_r, $weather_color_black_g, $weather_color_black_b) = sscanf($weather_color_black_hex, "#%02x%02x%02x");$weather_color_black_rgb=$weather_color_black_r.','.$weather_color_black_g.','.$weather_color_black_b;$weather_color_black_rgba=$weather_color_black_rgb.',1';
$weather_color_01_hex='#679794';list($weather_color_01_r, $weather_color_01_g, $weather_color_01_b) = sscanf($weather_color_01_hex, "#%02x%02x%02x");$weather_color_01_rgb=$weather_color_01_r.','.$weather_color_01_g.','.$weather_color_01_b;$weather_color_01_rgba=$weather_color_01_rgb.',1';
$weather_color_02_hex='#759766';list($weather_color_02_r, $weather_color_02_g, $weather_color_02_b) = sscanf($weather_color_02_hex, "#%02x%02x%02x");$weather_color_02_rgb=$weather_color_02_r.','.$weather_color_02_g.','.$weather_color_02_b;$weather_color_02_rgba=$weather_color_02_rgb.',1';
$weather_color_03_hex='#979267';list($weather_color_03_r, $weather_color_03_g, $weather_color_03_b) = sscanf($weather_color_03_hex, "#%02x%02x%02x");$weather_color_03_rgb=$weather_color_03_r.','.$weather_color_03_g.','.$weather_color_03_b;$weather_color_03_rgba=$weather_color_03_rgb.',1';
$weather_color_grid_hex='#979267';list($weather_color_grid_r, $weather_color_grid_g, $weather_color_grid_b) = sscanf($weather_color_grid_hex, "#%02x%02x%02x");$weather_color_grid_rgb=$weather_color_grid_r.','.$weather_color_grid_g.','.$weather_color_grid_b;$weather_color_grid_rgba=$weather_color_grid_rgb.',1';

echo'<div class="content">';

#Show barometric data
$weather_baro_label='Barometric pressure';
echo'<div class="weather_graph_container">';
echo'<div class="title_med">Barometric pressure</div>';
echo'<p>Lowest recorded value: '.$ocs_baromin_format.'&nbsp;&nbsp; // &nbsp;&nbsp;Highest recorded value: '.$ocs_baromax_format.'</p>';
echo'<div class="weather_graph"><canvas id="baro_hours_graph" height="500" width="1500"></canvas></div>';
echo'<div class="weather_graph"><canvas id="baro_days_graph" height="500" width="1500"></canvas></div>';
echo'<div class="weather_graph"><canvas id="baro_months_graph" height="500" width="1500"></canvas></div>';
echo'</div>';
echo'<script>';
echo'var baro_hours_ChartData = {';
echo'labels : ['.$weather_labels_hours.'],';
echo'datasets : [';
echo'{';
echo'label: "'.$weather_baro_label.'",';
echo'fillColor : "rgba('.$weather_color_01_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_01_rgb.',1)",';
echo'data : ['.$weather_baro_data_hours.']';
echo'}';
echo']';
echo'}';
echo"\n";
echo'var baro_days_ChartData = {';
echo'labels : ['.$weather_labels_days.'],';
echo'datasets : [';
echo'{';
echo'label: "'.$weather_baro_label.'",';
echo'fillColor : "rgba('.$weather_color_01_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_01_rgb.',1)",';
echo'data : ['.$weather_baro_data_days.']';
echo'}';
echo']';
echo'}';
echo"\n";
echo'var baro_months_ChartData = {';
echo'labels : ['.$weather_labels_months.'],';
echo'datasets : [';
echo'{';
echo'label: "'.$weather_baro_label.'",';
echo'fillColor : "rgba('.$weather_color_01_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_01_rgb.',1)",';
echo'data : ['.$weather_baro_data_months.']';
echo'}';
echo']';
echo'}';
echo'</script>';

#Show temperature data
$weather_temp1_label='Inside';
$weather_temp2_label='Outside';
$weather_temp3_label='Water';
echo'<div class="weather_graph_container">';
echo'<div class="weather_text">';
echo'<div class="weather_title">Temperature</div>';
echo'<p><div class="weather_legend_item"><div class="weather_legend_box" style="background:'.$weather_color_01_hex.';"></div><span style="color:'.$weather_color_01_hex.';">Inside &nbsp;&nbsp;(Lowest recorded value: '.$ocs_temp1min_format.'&nbsp;&nbsp; // &nbsp;&nbsp;Highest recorded value: '.$ocs_temp1max_format.')</span></div></p>';
echo'<p><div class="weather_legend_item"><div class="weather_legend_box" style="background:'.$weather_color_02_hex.';"></div><span style="color:'.$weather_color_02_hex.';">Outside &nbsp;&nbsp;(Lowest recorded value: '.$ocs_temp2min_format.'&nbsp;&nbsp; // &nbsp;&nbsp;Highest recorded value: '.$ocs_temp2max_format.')</span></div></p>';
echo'<p><div class="weather_legend_item"><div class="weather_legend_box" style="background:'.$weather_color_03_hex.';"></div><span style="color:'.$weather_color_03_hex.';">Water &nbsp;&nbsp;(Lowest recorded value: '.$ocs_temp3min_format.'&nbsp;&nbsp; // &nbsp;&nbsp;Highest recorded value: '.$ocs_temp3max_format.')</span></div></p>';
echo'</div>';
echo'<div class="weather_graph"><canvas id="temp_hours_graph" height="500" width="1500"></canvas></div>';
echo'<div class="weather_graph"><canvas id="temp_days_graph" height="500" width="1500"></canvas></div>';
echo'<div class="weather_graph"><canvas id="temp_months_graph" height="500" width="1500"></canvas></div>';
echo'</div>';
echo'<script>';
echo'var temp_hours_ChartData = {';
echo'labels : ['.$weather_labels_hours.'],';
echo'datasets : [';
echo'{';
echo'label: "'.$weather_temp1_label.'",';
echo'fillColor : "rgba('.$weather_color_01_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_01_rgb.',1)",';
echo'data : ['.$weather_temp1_data_hours.']';
echo'},';
echo'{';
echo'label: "'.$weather_temp2_label.'",';
echo'fillColor : "rgba('.$weather_color_02_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_02_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_02_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_02_rgb.',1)",';
echo'data : ['.$weather_temp2_data_hours.']';
echo'},';
echo'{';
echo'label: "'.$weather_temp3_label.'",';
echo'fillColor : "rgba('.$weather_color_03_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_03_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_03_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_03_rgb.',1)",';
echo'data : ['.$weather_temp3_data_hours.']';
echo'}';
echo']';
echo'}';
echo"\n";
echo'var temp_days_ChartData = {';
echo'labels : ['.$weather_labels_days.'],';
echo'datasets : [';
echo'{';
echo'label: "'.$weather_temp1_label.'",';
echo'fillColor : "rgba('.$weather_color_01_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_01_rgb.',1)",';
echo'data : ['.$weather_temp1_data_days.']';
echo'},';
echo'{';
echo'label: "'.$weather_temp2_label.'",';
echo'fillColor : "rgba('.$weather_color_02_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_02_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_02_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_02_rgb.',1)",';
echo'data : ['.$weather_temp2_data_days.']';
echo'},';
echo'{';
echo'label: "'.$weather_temp3_label.'",';
echo'fillColor : "rgba('.$weather_color_03_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_03_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_03_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_03_rgb.',1)",';
echo'data : ['.$weather_temp3_data_days.']';
echo'}';
echo']';
echo'}';
echo"\n";
echo'var temp_months_ChartData = {';
echo'labels : ['.$weather_labels_months.'],';
echo'datasets : [';
echo'{';
echo'label: "'.$weather_temp1_label.'",';
echo'fillColor : "rgba('.$weather_color_01_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_01_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_01_rgb.',1)",';
echo'data : ['.$weather_temp1_data_months.']';
echo'},';
echo'{';
echo'label: "'.$weather_temp2_label.'",';
echo'fillColor : "rgba('.$weather_color_02_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_02_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_02_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_02_rgb.',1)",';
echo'data : ['.$weather_temp2_data_months.']';
echo'},';
echo'{';
echo'label: "'.$weather_temp3_label.'",';
echo'fillColor : "rgba('.$weather_color_03_rgb.',0.2)",';
echo'strokeColor : "rgba('.$weather_color_03_rgb.',1)",';
echo'pointColor : "rgba('.$weather_color_03_rgb.',1)",';
echo'pointStrokeColor : "'.$weather_color_white_hex.'",';
echo'pointHighlightFill : "'.$weather_color_white_hex.'",';
echo'pointHighlightStroke : "rgba('.$weather_color_03_rgb.',1)",';
echo'data : ['.$weather_temp3_data_months.']';
echo'}';
echo']';
echo'}';
echo'</script>';

echo'</div>';

//Settings and stuff
echo'<script>';
echo'Chart.defaults.global.animation = false;';
echo'Chart.defaults.global.scaleLineWidth = 1;';
echo'Chart.defaults.global.scaleFontFamily = "\'Source Sans Pro\', \'Helvetica Neue\', \'Helvetica\', \'Arial\', sans-serif";';
echo'Chart.defaults.global.tooltipFontFamily = "\'Source Sans Pro\', \'Helvetica Neue\', \'Helvetica\', \'Arial\', sans-serif";';
echo'Chart.defaults.global.tooltipTitleFontFamily = "\'Source Sans Pro\', \'Helvetica Neue\', \'Helvetica\', \'Arial\', sans-serif";';
echo'Chart.defaults.global.scaleFontSize = 13;';
echo'Chart.defaults.global.tooltipFontSize = 13;';
echo'Chart.defaults.global.tooltipTitleFontSize = 13;';
echo'Chart.defaults.global.scaleFontStyle = "normal";';
echo'Chart.defaults.global.tooltipFontStyle = "normal";';
echo'Chart.defaults.global.tooltipTitleFontStyle = "normal";';
echo'Chart.defaults.global.scaleFontColor = "'.$weather_color_white_hex.'";';
echo'Chart.defaults.global.tooltipFontColor = "'.$weather_color_white_hex.'";';
echo'Chart.defaults.global.tooltipTitleFontColor = "'.$weather_color_white_hex.'";';
echo'Chart.defaults.global.responsive = true;';
echo'Chart.defaults.global.tooltipFillColor = "rgba('.$weather_color_black_rgba.')";';
echo'window.onload = function(){';
echo'var baro_hours_ctx = document.getElementById("baro_hours_graph").getContext("2d");';
echo'var baro_days_ctx = document.getElementById("baro_days_graph").getContext("2d");';
echo'var baro_months_ctx = document.getElementById("baro_months_graph").getContext("2d");';
echo'var temp_hours_ctx = document.getElementById("temp_hours_graph").getContext("2d");';
echo'var temp_days_ctx = document.getElementById("temp_days_graph").getContext("2d");';
echo'var temp_months_ctx = document.getElementById("temp_months_graph").getContext("2d");';
echo'window.baro_hours_line = new Chart(baro_hours_ctx).Line(baro_hours_ChartData, {';
//echo'bezierCurve : false,';
//echo'bezierCurveTension : 0.4,';
echo'scaleLabel: "<%=value%> Mbar",';
echo'pointDotRadius : 3,';
echo'pointHitDetectionRadius : 5,';
echo'datasetStrokeWidth : 2';
echo'});';
echo'window.baro_days_line = new Chart(baro_days_ctx).Line(baro_days_ChartData, {';
echo'scaleLabel: "<%=value%> Mbar",';
echo'pointDotRadius : 3,';
echo'pointHitDetectionRadius : 5,';
echo'datasetStrokeWidth : 2';
echo'});';
echo'window.baro_months_line = new Chart(baro_months_ctx).Line(baro_months_ChartData, {';
echo'scaleLabel: "<%=value%> Mbar",';
echo'pointDotRadius : 3,';
echo'pointHitDetectionRadius : 5,';
echo'datasetStrokeWidth : 2';
echo'});';
echo'window.temp_hours_line = new Chart(temp_hours_ctx).Line(temp_hours_ChartData, {';
echo'scaleLabel: "<%=value%> °C",';
echo'pointDotRadius : 3,';
echo'pointHitDetectionRadius : 5,';
echo'datasetStrokeWidth : 2';
echo'});';
echo'window.temp_days_line = new Chart(temp_days_ctx).Line(temp_days_ChartData, {';
echo'scaleLabel: "<%=value%> °C",';
echo'pointDotRadius : 3,';
echo'pointHitDetectionRadius : 5,';
echo'datasetStrokeWidth : 2';
echo'});';
echo'window.temp_months_line = new Chart(temp_months_ctx).Line(temp_months_ChartData, {';
echo'scaleLabel: "<%=value%> °C",';
echo'pointDotRadius : 3,';
echo'pointHitDetectionRadius : 5,';
echo'datasetStrokeWidth : 2';
echo'});';
echo'}';
echo'</script>';

?>
