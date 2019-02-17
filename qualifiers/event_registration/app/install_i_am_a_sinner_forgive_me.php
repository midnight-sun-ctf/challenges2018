<?php
while(1){
	try{
		echo "sleeping....";
		sleep(5);
		$db = new mysqli('database', 'root', 'fegisbabiannyllebakfyllaitrynet', 'captcha');
		$db->query("DROP TABLE users");
		$db->query("CREATE TABLE users (id INT AUTO_INCREMENT, name TEXT, username VARCHAR(255) UNIQUE, password TEXT, PRIMARY KEY (id))");
		$db->query("REPLACE INTO users (id, name, username, password) VALUES (1, 'root', 'root', 'orangejuice_is_my_favvo_dricka_men_rip_mage_gone_halsbraenna');");
		if($db->query("grant select on captcha.* to 'slave'@'%' identified by 'tjenatjenamittbenaminaarmareklena';")){
			$db->query("grant insert, update on captcha.* to 'slave_inserter'@'%' identified by 'tjenatjenamittbenaminaarmareklena';");
			exit("Installed!");
		}
	}catch(Exception $x){
		sleep(5);
	}
}