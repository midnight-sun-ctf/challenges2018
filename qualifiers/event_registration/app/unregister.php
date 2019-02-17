<?php
	session_start();
	if(isset($_SESSION['name'])){
		$_SESSION['registered'] = 0;
	}
	header('Location: /');