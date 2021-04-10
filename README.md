# Digital Oxford Wagtail Install

The repository for the [Wagtail](https://docs.wagtail.io/en/stable/index.html) powered [Digital Oxford](https://digitaloxford.com) site.


## Notes

- Requires Python 3.*
- This project uses [django-sass-processor](https://github.com/jrief/django-sass-processor) to manage scss files. Refer to that repository's README for instructions on how to manage the files. 
- Code formatting is controlled by [Black](https://black.readthedocs.io/en/stable/index.html). At some point that will probably become automated. 


## Local setup

Clone this repository and then:

```
$ cd <install-directory>
```

Create and activate your virtual environment:

```
$ python -m venv env
$ source ./env/bin/activate
```

Install requirements:

```
$ pip install -r requirements.txt
```

Run the migrations and create the superuser:

```
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py createsuperuser
```

Create a local secrets file at `<install-directory>/digitaloxford/settings/local.py` with the following format:

```
SECRET_KEY = 'some random hash'
```

Finally, start the server:

```
$ ./manage.py runserver
```

