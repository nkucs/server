#!/bin/sh

n=0
while [ $n -lt 5 ]
do
    python manage.py migrate --no-input && 
    break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done

python manage.py runserver 0.0.0.0:8000
