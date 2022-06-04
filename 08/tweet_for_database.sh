#!/bin/bash

# bash user_add_for_database.sh
# bash follow.sh

sukarusToken=$(http -v POST localhost:5000/login email=sukarus@gmail.com password=1111 | grep access_token | cut -d':' -f2 | cut -d'"' -f2)
http -v POST localhost:5000/tweet tweet="I fucked jm last night." "Authorization:${sukarusToken}"
http -v POST localhost:5000/tweet tweet="I grap her pussy hardly." "Authorization:${sukarusToken}"

gmToken=$(http -v POST localhost:5000/login email=gmhan@gmail.com password=2222 | grep access_token | cut -d':' -f2 | cut -d'"' -f2)
http -v POST localhost:5000/tweet tweet="His cock penentrated my body last night" "Authorization:${gmToken}"

http -v POST localhost:5000/tweet tweet="I want to fuck another women, tonight" "Authorization:${sukarusToken}"
http -v POST localhost:5000/tweet tweet="I love him" "Authorization:${gmToken}"

jeToken=$(http -v POST localhost:5000/login email=jekim@gmail.com password=3333 | grep access_token | cut -d':' -f2 | cut -d'"' -f2)
http -v POST localhost:5000/tweet tweet="I want to sleep with him" "Authorization:${jeToken}"

mysql -uroot -p1111 -Dminiter -e 'SELECT * FROM tweets;'
