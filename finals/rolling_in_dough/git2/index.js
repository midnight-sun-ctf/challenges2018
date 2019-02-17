var express = require('express');
var session = require('express-session');
const puppeteer = require('puppeteer');
var RateLimit = require('express-rate-limit');
var FileStore = require('session-file-store')(session);

var apiLimiter = new RateLimit({
  windowMs: 60*1000, // 1 minutes
  max: 30,
  delayMs: 0, // disabled
  message: "Too many requests, please try again in one minute."
});

var app = express();

app.use(session({
    store: new FileStore({"secret": "lolwut in the butt"}),
    secret: 'amses bullar bär bådas barn',
    cookie: { secure: false },
    resave: false,
    saveUninitialized: false
}));

app.use('/submit', apiLimiter);

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({
	extended: true
}));

app.listen(2999, function () {
  console.log('Screensaver listening on port 2999!')
});

app.get('/*',function(req,res,next){
    req.session.tjosan = "hejsan"
    res.header('X-Frame-Options', 'DENY');
    res.header('X-Content-Type-Options', 'nosniff');
    res.header('X-XSS-Protection', '0');
    if(req.session.flag && req.session.flag != ""){
      res.send(req.session.flag);
    }else{
      next();
  }
});

index = `<!DOCTYPE html>
<html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" user-scalable="no" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="/static/style.css" />
      <script src="/static/jquery.js"></script>
      <script src="/static/bootstrap.js"></script>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.css" />
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.3.0/css/mdb.min.css" />
  </head>
  <body>
      <section class="login-info">
<div class="container">
  <div class="row main">
       <div class="form-header header">
          <h1 class="text-center text-black">BREADROLLER</h1>
        </div>
    <div class="main-content">
    	  <div class="row" id="container">
          	<hr>
          	<h4 class="text-center black-text">Make alert(1) pop <a href="http://breadroll.alieni.se:31337/?status=200&input=hello">here</a> in Chrome and submit the working URL in the form below.</h4>
          </div>
          <form method="post" action="/submit">
          <div class="input-group ">
            <span class="input-group-addon"><span class="glyphicon glyphicon-paperclip" aria-hidden="true"></span></span>
            <input type="text" class="form-control text-center" name="url" placeholder="URL that pops alert(1) without user interaction">
          </div>
          
          <div class="form-group ">
          <center>
              <input type="submit" value="submit" name="login" class="btn text-dark header btn-lg btn-block login-button"/>
              </center>
          </div>

          </form>
          
          <div class="form-group" id="container">
          </div>
      
      </div>
    </div></body></html>
`;

flag = `
<font color="red" size="6">`+process.env.FLAG+`</font>
`;

app.get('/', function (req, res) {
  res.send(index);
});

host = 'breadroll.alieni.se:31337'
//host = '127.0.0.1:2999'
hostregex = new RegExp("^http://"+host+"/");

app.use('/static', express.static('static'));

app.post('/submit', function (req, res){
    if(req.body.url && hostregex.test(req.body.url) && req.body.url.length < 500){
		url = req.body.url;
		try{
			puppeteer.launch({args: ['--no-sandbox']}).then(browser => {
				browser.newPage().then(function(page){
					page.on('framenavigated', function(frame){
						console.log(frame.url());
						if(!(hostregex.test(frame.url())) && !(/^(data|about):/.test(frame.url()))){
							browser.close();
							req.session.flag="";
							res.send("Not allowed to navigate outside of "+host);
						}
					});
					page.on('dialog', function(dialog){
						if(dialog.type() == 'alert'){
							if(dialog.message() == "1"){
								req.session.flag = flag
								browser.close();
								res.redirect("/");
							}else{
								browser.close();
								res.send("alert popped, but not with (1)!")
							}
						}
					});
					page.goto(url, { timeout: 2000 }).then(function(){ 
              page.waitFor(1000).then(function(){
                browser.close();res.redirect("/");
              });
            }).catch(function(){
						browser.close();
						res.redirect("/");
					});
				});
			});
		}catch(x){
			res.send("Error")
		}
    }else{
      res.send("Error, URL not matching "+hostregex+"?");
    }
});

