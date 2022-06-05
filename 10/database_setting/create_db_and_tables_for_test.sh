#!/bin/bash

mysql -uroot -p1111 -e 'create database miniter_test'
mysql -uroot -p1111 -Dminiter_test < ./sql/create_table.sql
mysql -uroot -p1111 -Dminiter_test -e 'show tables;'
