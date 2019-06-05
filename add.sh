#!/bin/bash 

find . -type d -name __pycache__ | xargs rm -rf
rm -rf /home/django/xx-scan/tmp/ 
rm -rf /home/django/xx-scan/data*
rm -rf /home/django/xx-scan/logs*
rm -rf /home/django/xx-scan/collect*
rm -rf /home/django/xx-scan/resul*

git config --global user.name "actanble"
git config --global user.email actanble@gmail.com 

git add . && git commit -m $1  && git push 
