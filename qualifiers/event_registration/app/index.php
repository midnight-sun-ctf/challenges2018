<?php
ob_start();
	require_once('lib.php');
	session_start();
	if(isset($_SESSION['username'])){
		if((int)$_SESSION['id'] === 1){
			echo "midnight{dub_i_dub_i_dub_i_dubdubdub_dub_i_dub_i_dub_i_yeah_yeah}";
			die();
		}else{
			if(isset($_SESSION['name'])){
				if(isset($_SESSION['registered']) && $_SESSION['registered'] === 1){
					echo "Hello ".htmlentities($_SESSION['name']).", thank you for registering for the event! Click <a href='unregister.php'>here</a> to unregister.";
				}else{
					echo "Hello ".htmlentities($_SESSION['name']).", we're sorry you can't make it to the event!";
				}
			}else{
				echo "user not found";
			}
		}
	}else{
		header('Location: login.php');
	}
?>
<br />
<a href="logout.php">Logout</a>
<?php
$html = ob_get_contents();
ob_end_clean();
?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>Event Registration - Manage</title>
	
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
	<style>
		div.gallery {
			margin: 5px;
			border: 1px solid #ccc;
			float: left;
			width: 180px;
		}
		
		div.gallery:hover {
			border: 1px solid #777;
		}
		
		div.gallery img {
			width: 100%;
			height: auto;
		}
		
		div.desc {
			padding: 15px;
			text-align: center;
		}
	</style>
</head>
<body>
	<div class="container">
		<div class="row">
			<div class="col">
				<h1>Event Registration</h1>
			</div>
		</div>
		<div class="row">
			<div class="col">
				<?php echo $html; ?>
			</div>
		</div>
	</div>
	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
