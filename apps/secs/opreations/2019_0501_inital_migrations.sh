#!/bin/bash

python ../apps/manage.py shell << EOF
from secs.models import Userprofile


EOF

