#!/bin/bash
while true; do killall --older-than 10s node; sleep 10; done;