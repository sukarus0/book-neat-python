#!/bin/bash

http -v POST localhost:5000/sign-up name=DWLee email=sukarus@gmail.com password=1111 profile="Ph.d"

mysql -uroot -p1111 -Dminiter -e 'SELECT * FROM users;'
