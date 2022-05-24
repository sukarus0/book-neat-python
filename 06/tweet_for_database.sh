#!/bin/bash

bash user_add_for_database.sh
# bash follow.sh

http -v POST localhost:5000/tweet id=1 tweet="I fucked jm last night."
http -v POST localhost:5000/tweet id=1 tweet="I grap her pussy hardly."

http -v POST localhost:5000/tweet id=2 tweet="His cock penentrated my body last night"

http -v POST localhost:5000/tweet id=1 tweet="I want to fuck another women, tonight"
http -v POST localhost:5000/tweet id=2 tweet="I love him"

http -v POST localhost:5000/tweet id=3 tweet="I want to sleep with him"

mysql -uroot -p1111 -Dminiter -e 'SELECT * FROM tweets;'
