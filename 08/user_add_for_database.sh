#!/bin/bash

http -v POST localhost:5000/sign-up name=DWLee email=sukarus@gmail.com password=1111 profile="Ph.d"
http -v POST localhost:5000/sign-up name=jmhan email=gmhan@gmail.com password=2222 profile="Actress:40"
http -v POST localhost:5000/sign-up name=jekim email=jekim@gmail.com password=3333 profile="Actress:20"

mysql -uroot -p1111 -Dminiter -e 'SELECT * FROM users;'
