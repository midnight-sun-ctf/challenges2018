if (!String.prototype.endsWith) {
	String.prototype.endsWith = function(search, this_len) {
		if (this_len === undefined || this_len > this.length) {
			this_len = this.length;
		}
		return this.substring(this_len - search.length, this_len) === search;
	};
}

function rndstr(l) {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < l; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}

function cpwpow(v) {
	while(1) {
        var pow = rndstr(10);
	    var h = sha256(v+pow);
        if(h.indexOf("1337") == 0) {
	        return pow;
        }
    }
}

function cloginpow(v) {
	while(1) {
        var pow = rndstr(10);
	    var h = sha256(v+pow);
        if(h.endsWith("66666")) {
	        return pow;
        }
    }
}
