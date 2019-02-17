<?php
$input = "";
if(isset($_GET['input'])){
	$input = str_replace("<", "", $_GET['input']);
}

$status = isset($_GET['status']) ? $_GET['status'] : 200;
$status = (int)$status;

header('X-Frame-Options: deny');
header('X-Content-Type-Options: nosniff');
header('HTTP/1.1 ' . $status . ' OK');
?>
<?php
echo "-> " . $input . "\n<br/><br/>";
show_source(__FILE__);