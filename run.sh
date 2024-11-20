#!/bin/bash

if ! [ -f secrets.env ]
then
    echo "$0: Must have secrets.env"
    exit -1
fi

if [[ "$1" == "prod" ]]
then
    echo "Production Mode"
    docker run --env-file=secrets.env -d --restart always --name=spicybot spicybot
else
    echo "Development Mode"
    docker run --env-file=secrets.env --name=spicybot spicybot
fi

