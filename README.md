# Digital Oxford Wagtail Install

How to get up and running with a local install.

```
$ cd <install-directory>
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
