#! /bin/bash
cd locus
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=locus.settings
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username anindya --noinput --email a@g.com
python setup_superuser.py
python manage.py runserver 0.0.0.0:8000