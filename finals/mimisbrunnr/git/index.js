var express = require('express');
var session = require('express-session');
const puppeteer = require('puppeteer');
var RateLimit = require('express-rate-limit');
var FileStore = require('session-file-store')(session);

var defaultLink = "/xss?xss=traveller&mimis=plain";
var challengeName = "MIMISBRUNNR";
var debug = true; // Change to false when going live
var flag = `<font color="red" size="6">`+process.env.FLAG+`</font>`;
var xss_template = `
                              WELCOME, __CURRENT_PAYLOAD__
    /h e h e//////////////////////////////////////////////////////////////////////////////////////\`    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMNs:...-:/++osyhhdmmNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMh-  \`\`            \`\`\`..-://+osyyhdmmNNMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMN/\` \`.............\`\`\`\`\`\`\`\`\`        \`\`\`\`./dMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMy.  ..................................... \`+mMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMm/\` \`------.............................-+s-  .sNMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMy.  ...-------------------...............+o+o:\`  :dMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMm+\` \`...................------------------:o+++o+.  .sNMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMh-  .:----............................----/oooooooo-   :dMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMNs\`  .-----:-::--------....................-++++++oooo:\`  \`yNMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMN/  \`.............-------::::----..........-++++++++oooo+.   +NMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMN:  \`-......................---------:------/+++oooo++oooo+.   :mMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMh   .:::-----..........................----++++++++oooooooo+.   hMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMm:.\`\`  \`\`\`...-::///:---...................:+++ooooooo++/:-.\`\`\`.:mMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMNmdhyo+:-\`   -oss+..--:::::::----......:++++ooss:-.\`.-:+syhdmNMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMNh\` \`+osso/::-..\`\`.+osooo+//::-/:-../oss\`  +mNMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMo  .+syo++oossoooosossssssss-\`    :oss\`  /*∕MMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMd\` ./sy/   \`\`./sooosososssyy+/:-../+ss.  .yNMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMM. \`:oy/      \`\` .-+osoooos//+oosso+sy+/-\` /mMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMM: \`:oy/           :o-   \`\`      \`//syosy+\` .yNMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMM+ \`:oy/           -o-            -:ss\`\`+yo.  :dNMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMs \`:sy/           -o.            -:ss\`  :ss-   .:o/*∕MMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMs \`:sy/           -o.            -:ss\`   -os/\`\`    \`oMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMs \`:sy/           -/.            -:ss\`    \`/oo+:::  /MMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMNds. \`:sy/           :+\`            -:ss\`        \`.-\`  /*∕MMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMNds+-\`    .:syo/+osssooooo/oo+++//::--.\` ::ss\`    .osso+////*∕MMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMy.    \`..-:::oyyyssyyyysyyy+syyyyyssssssss+:sy-\`   :mMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMh\`   .-::::/ossyyyyyhhhhhhhh/shhhhhhhhhyyyyo:syss+/\` \`/dMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMM/  \`---.-:oyyyhhhhhyhhhhhhhh/yhhhhhhhhhhhyho:syyssss/\` \`/*∕MMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN.  /+-----+yyyyhhhyhhhhhhhhh/yhhhhhhhhhhhyho:syyyysss/  sMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN.  +o/.\`\`../oyyhhhhhhhhhhhhh+hhhhhhhhhhhhys/:syssssyyy. sMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN.  /+/::-\`\`\`.-::/+ossyhhhhhhshhhhhhyyso+//:--/o+ossyyy- oMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN\`  ++/:/:-:--......\`.----:://://:::::::-://+oossssssss: -MMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMNNmdy/  \`oo///:-:/::::::.-:------::-//++++oososssyysssyyssyy/  +hNMMMMMMMMMMMMN-    
    /*∕MMNhyo+/:-.\`\`    \`++///:::::::::---::://////:+ooosssssosssssssssssyyy+   \`.:oymNMMMMMMMN-    
    /*∕Mh-          \`..-:o+://::/::::--::---:::::/::/+oooooosyyssssyyyyyosyy+\`       \`:yNMMMMMN-    
    /*∕d\`    \`\`\`..--::/++o+/::::///:::---:::::::::/:/+oooooosyyyssyyyyyssssso/:::\`.\`    :dMMMMN-    
    /*∕/    \`..-::::::///so+///::///:::::::://////:/++ooooosssssssssssssyysysooo+///---  \`sNMMN-    
    /*∕+   \`----::::::://oso/+//://///:::::///////:/+++++osyyssyyyssysosyysysoooo+++++/\`\`  +NMN-    
    /*∕m-  \`\`.-::::::::::+oo++++:::///:////:::::////++ooosyyyssyyyssssssssssoooooo+++++/:   dMN-    
    /*∕Mm:   \`.-::::-::::::///++/////::///::///////+ooossssssssyyyssyssooooooo+++++++++/\`  .mMN-    
    /*∕MMNo.   \`.-----::::::::::::+++++++/:++++ooo+osssyyyysysoossooo++++++++++++++++//\`  \`/*∕N-    
    /*∕MMMMmy/.   \`....-:-::::::::://:++/+/+/+o/+oo+osssssso+/+/+////+++++///+///+/:-\`\`  \`sMMMN-    
    /*∕MMMMMMMmh+-\`    ..--------:::::::::::::::::::://///////////////++///:-:-:/:.    ./dMMMMN-    
    /*∕MMMMMMMMMMNdy/.\`      \`.......---::-:::::::::::::////://////:.--....    \`.\`\`.:ohNMMMMMMN-    
    /*∕MMMMMMMMMMMMMMNds+:.\`\`          \`\`\`\`\`\`...\`-:-.....-::::::-..         \`.-/oydNMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMNNmdyso+/:-.\`\`                  \`\`\`\`\`      \`.-/oydmNMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNmhysso+//:--....\`\`\`\`\`\`.-:/+sydmNMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNNNNNNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*/ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-- 
`;

var apiLimiter = new RateLimit({
  windowMs: 60*100, // 1 minutes
  max: 3,
  delayMs: 0, // disabled
  message: "Too many requests, please try again in one minute."
});

var app = express();

app.use(session({
    store: new FileStore({"secret": "lolwut in the butt"}),
    secret: 'bamses bullar bär bådas barn',
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
  console.log('XSS 2 listening on port 2999!')
});

app.get('/*',function(req,res,next){
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
          <h1 class="text-center text-black">`+challengeName+`</h1>
        </div>
    <div class="main-content">
    	  <div class="row" id="container">
          	<hr>
          	<h4 class="text-center black-text">Make alert(1) pop <a href="`+defaultLink+`">here</a> in Chrome and submit the working URL in the form below.</h4>
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

app.get('/', function (req, res) {
  res.send(index);
});

app.get('/xss', function (req, res) {
  res.header('Content-Security-Policy', "script-src 'self'");
  if(req.query.xss){
    xss = req.query.xss;
    
    res.header('Content-Type', req.query.mimis ? ('text/'+req.query.mimis.substring(0,7)) : 'text/plain');
    res.send(xss_template.replace("__CURRENT_PAYLOAD__", xss));
  }else{
    res.send(xss_template.replace("__CURRENT_PAYLOAD__","TRAVELLER"));
  }
});

host = debug?'127.0.0.1:2999':'mimis.alieni.se:2999';
host = host.replace(/\./g, "\\.");
hostregex = new RegExp("^http://"+host+"/");

app.use('/static', express.static('static'));

app.post('/submit', function (req, res){
    if(req.body.url && hostregex.test(req.body.url) && req.body.url.length < 1000){
		url = req.body.url;
		try{
			puppeteer.launch({args: ['--no-sandbox']}).then(browser => {
				browser.newPage().then(function(page){
					page.on('framenavigated', function(frame){
						console.log(frame.url());
						if(!(hostregex.test(frame.url())) && !(/^(data|about):/.test(frame.url()))){ // New window without URL will get about:blank
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
                try{
                  browser.close();
                  res.redirect("/");
                }catch(error){
                  // If alert pops, this will error since browser is already closed.
                }
              });
            }).catch(function(e){
              try{
    						browser.close();
    						res.redirect("/");
              }catch(error){
               // If alert pops, this will error since browser is already closed.
              }
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

