#!/bin/bash
cd /opt/blog/blogproject
gunicorn --bind 0.0.0.0:8888 blogproject.wsgi --access-logfile=/tmp/blogaccess.log  --error-logfile=/tmp/blogerror.log  --reload --threads=5 
