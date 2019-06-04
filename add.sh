#!/bin/bash 

find . -type d -name __pycache__ | xargs rm -rf
rm -rf /home/django/xx-scan/tmp/ 
rm -rf /home/django/xx-scan/datas/ 

git add .
git commit -m $1 
git push 

