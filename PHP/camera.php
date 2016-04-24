<?php

//Title
echo'<div class="header_sub">';
echo'<div class="title_big">Camera</div>';
echo'<div class="title_small">[ <a href="/">Go back</a> ]</div>';
echo'</div>';

//Camera
echo'<div class="content">';
$camera_list=array_diff(scandir('img/if-camera'), array('..', '.'));rsort($camera_list);
$count=0;foreach ($camera_list as $camera_file) {
if($count==0){echo'<img class="media_item_bordered" alt="camera" src="/img/if-camera/'.$camera_file.'">';}
else{
if($count>1){echo'<div class="seperator_small"></div>';}
$camera_num=count($camera_list)-$count;
$camera_title=$camera_file;$camera_title=substr($camera_title,0,-4);$camera_title=substr($camera_title,11);$camera_title=explode('_',$camera_title);
$camera_date=explode('-',$camera_title[0]);$camera_date_year=$camera_date[0];$camera_date_month=$camera_date[1];$camera_date_day=$camera_date[2];$camera_date_full=$camera_date_day.'.'.$camera_date_month.'.'.$camera_date_year;
$camera_time=$camera_title[1];$camera_time_hour=substr($camera_time,0,2);$camera_time_min=substr($camera_time,2,2);$camera_time_sec=substr($camera_time,4,2);$camera_time_full=$camera_time_hour.':'.$camera_time_min.':'.$camera_time_sec;
$camera_title_full=$camera_date_full.' '.$camera_time_full;
echo'<div class="cam_item">';
echo'<p><a target="_blank" href="img/if-camera/'.$camera_file.'">Photo no. '.sprintf('%05d', $camera_num).'&nbsp;&nbsp;&#8226;&nbsp;&nbsp;'.$camera_title_full.'</a></p>';
echo'</div>';}
$count++;}
echo'</div>';

?>
