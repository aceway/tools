#!/bin/bash
echo "rsync aceway-project to server:"
rsync -r --exclude='deployment.py' --progress /home/aceway/workspace/project/  aceway@www.aceway.com:/var/www/project/
