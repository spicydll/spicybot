#!/bin/bash

if ! [ -f secrets.env ]
then
    echo "$0: Must have secrets.env"
    exit -1
fi

if [[ "$1" -eq "prod" ]]
then
    echo "Production Mode"
    docker --env-file=secrets.env -d --restart always spicybot
else
    echo "Development Mode"
    docker --env-file=secrets.env spicybot
fi

