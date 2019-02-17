<?php
header('Server: Apache');
$db = new mysqli('database', 'slave', 'tjenatjenamittbenaminaarmareklena', 'captcha');
$db_insert = new mysqli('database', 'slave_inserter', 'tjenatjenamittbenaminaarmareklena', 'captcha');

$wat = $db_insert->query("INSERT INTO users (id, username) VALUES (1, 'root') ON DUPLICATE KEY UPDATE id=1, username='root'");

function add_user($name, $username, $password){
	global $db, $db_insert;

	$name = mysqli_real_escape_string($db_insert, $name);
	$username = mysqli_real_escape_string($db_insert, $username);

	if(strlen($password) > 55 || strlen($name) > 55 || strlen($username) > 55){
		header('Location: /login.php');
	}

	$password = substr($password, 0, 55);

	$result = $db_insert->query("INSERT INTO users (name, username, password) VALUES ('$name', '$username', '$password')");
	return (bool)$result;
}



function login($username, $password){
	global $db;

	$username = mysqli_real_escape_string($db, $username);
	$password = mysqli_real_escape_string($db, $password);

	$result = $db->query("SELECT * FROM users WHERE username='$username' AND password='$password'");

	if($result->num_rows === 0){
		return false;
	}
	$row = $result->fetch_assoc();
	return $row;
}

#