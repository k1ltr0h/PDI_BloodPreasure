#!/bin/bash


cd /opt/app/api_blood_preassure/
while [ true ]; do
   python3 manage.py runserver 0.0.0.0:8000
   sleep 1
done;

