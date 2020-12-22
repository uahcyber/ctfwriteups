<?php
/* flag_checker */
include('flag.php');

if(!isset($_GET['flag'])) {
    highlight_file(__FILE__);
    die();
}

function checkFlag($flag) {
    $example_flag = strtolower('FAKE-X-MAS{d1s_i\$_a_SaMpL3_Fl4g_n0t_Th3_c0Rr3c7_one_karen_l1k3s_HuMu5.0123456789}');
    $valid = true;
    for($i = 0; $i < strlen($flag) && $valid; $i++)
        if(strpos($example_flag, strtolower($flag[$i])) === false) $valid = false;
    return $valid;
}


function getFlag($flag) {
    $command = "wget -q -O - https://kuhi.to/flag/" . $flag;
    $cmd_output = array();
    exec($command, $cmd_output);
    if(count($cmd_output) == 0) {
        echo 'Nope';
    } else {
        echo 'Maybe';
    }
}

$flag  = $_GET['flag'];
if(!checkFlag($flag)) {
    die('That is not a correct flag!');
}

getFlag($flag);
?>