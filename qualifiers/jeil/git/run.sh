#!/bin/bash
./killall.sh &
socat TCP-LISTEN:55542,reuseaddr,fork EXEC:"./chall.sh"