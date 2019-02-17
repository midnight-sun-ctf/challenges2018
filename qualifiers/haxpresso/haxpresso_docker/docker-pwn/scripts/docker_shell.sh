#! /bin/bash

if [ $# -eq 0 ]
  then
    echo "./docker_shell.sh <image_name>"
    exit 1
fi

docker exec -i -t $1 /bin/sh 
