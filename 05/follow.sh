#!/bin/bash

http -v POST localhost:5000/follow id=1 follow=2
http -v POST localhost:5000/follow id=2 follow=1
http -v POST localhost:5000/follow id=3 follow=1
