var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);

var Jail = (function() {
    var rv = {};

    function secretFuncUnguessable{{ENV_SECRET_0}}(a,b,c){
        if(a === '{{ENV_SECRET_1}}' && b === '{{ENV_SECRET_2}}' && c === '{{ENV_SECRET_3}}'){
            return true;
        }
    }

    function call(code) {
        var line = "";

        if(new RegExp(/[\[\]\.\\\+\-\/;a-zA-Z{}`'"\s]/).test(code)){
            console.log("Unrecognized code.");
            throw 123;
            return;
        }

        if(!(code.length == 32)){
            console.log("Incorrect code length.");
            throw 123;
            return;
        }

        arguments = undefined;

        ret = null;
        ret = eval("this.secretFuncUnguessable"+code);

        if(typeof ret == "function"){
            if(ret.call(this,'{{ENV_SECRET_1}}', '{{ENV_SECRET_2}}', '{{ENV_SECRET_3}}') === true){
                console.log("{{ENV_SECRET_FLAG}}");
            }else{
                console.log("Incorrect code.");
            }
        }else{
            console.log("Incorrect code.");
        }
        throw 123;
    };
    rv.call = call;
    rv.toString = function(){return rv.call.toString()};

    return rv;
})();

template = `|￣￣￣￣￣￣￣￣|  
|    Internal    |
|＿＿＿＿＿＿＿＿|
       ||
(\\__/) || 
(•ㅅ•) || 
/ 　 づ  

Code: `;

function ask(){
    rl.question(template,function(answer){
        Jail.call(answer);
    });
}

ask();



