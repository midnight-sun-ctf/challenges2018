<?php
ob_start();
	require_once('lib.php');
	session_start();
	if(isset($_POST['register'])){
		if(strlen(trim($_POST['username'])) == 0){
			die('Empty username!!!');
		}
		if(strlen(trim($_POST['password'])) == 0){
			die('Empty password!!!');
		}
		if(strlen(trim($_POST['fullname'])) == 0){
			die('Empty fullname!!!');
		}
		if(strlen(trim($_POST['username'])) > 55){
			die('Too long username!!!');
		}
		if(strlen(trim($_POST['password'])) > 55){
			die('Too long password!!!');
		}
		if(strlen(trim($_POST['fullname'])) > 55){
			die('Too long fullname!!!');
		}
		add_user($_POST['fullname'], $_POST['username'], $_POST['password']);
		echo "Done!";
		die;
	}elseif(isset($_POST['login'])){
		if(strlen(trim($_POST['username'])) == 0){
			die('Empty username!!!');
		}
		if(strlen(trim($_POST['password'])) == 0){
			die('Empty password!!!');
		}
		if(strlen(trim($_POST['username'])) > 55){
			die('Too long username!!!');
		}
		if(strlen(trim($_POST['password'])) > 55){
			die('Too long password!!!');
		}
		$auth = login($_POST['username'], $_POST['password']);
		if($auth){
			$_SESSION['username'] = $auth['username'];
			$_SESSION['name'] = $auth['name'];
			$_SESSION['id'] = $auth['id'];
			$_SESSION['registered'] = 1;
			header('Location: /');
		}else{
			header('Location: /login.php');
		}
		die;
	}
?>
<div class="row">
  <div class="col">
    <h2>Login</h2>
      <form action="login.php" method="POST" enctype="multipart/form-data">
        <div class="row">
          <div class="col">
            <div class="form-group">
              <input type="text" placeholder="username" name="username" maxlength="55" class="form-control" />
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <input type="text" placeholder="password" name="password" maxlength="55" class="form-control" />
            </div>
          </div>
        </div>
        <div class="row">
		  <div class="col">
		    <input type="hidden" name="login" />
		    <button type="submit" class="btn btn-primary">Login</button>
		  </div>
		</div>
	  </form>
    </div>
  </div>
<div class="row">
<div class="col">
<h2>Register</h2>
<form action="login.php" method="POST" enctype="multipart/form-data">
<div class="form-group">
<input type="text" placeholder="fullname" name="fullname" maxlength="55" class="form-control" />
</div>
<div class="form-group">
<input type="text" placeholder="username" name="username" maxlength="55" class="form-control" />
</div>
<div class="form-group">
<input type="text" placeholder="password" name="password" maxlength="55" class="form-control" />
</div>
<input type="hidden" name="register" />
<button type="submit" class="btn btn-primary">Register</button>
</form>
</div></div>
<?php
$html = ob_get_contents();
ob_end_clean();
?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>Event Registration - Login</title>
	
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
		<?php echo $html; ?>
	</div>
	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
