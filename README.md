# Digital Oxford Wagtail Site

The repository for the [Wagtail](https://docs.wagtail.io/en/stable/index.html) powered [Digital Oxford](https://digitaloxford.com) site.


## Notes

- Requires Python 3.11 or newer
- This project uses [django-sass-processor](https://github.com/jrief/django-sass-processor) to manage scss files. Refer to that repository's README for instructions on how to manage the files.

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
$ pip install -r requirements/requirements-dev.txt
```

(NOTE: `requirements-dev.txt` includes `requirements.txt` automatically)

### Pre-commit hooks

This repository uses the [pre-commit](https://pre-commit.com/) framework to perform certain sanity checks during development. These include code formatting with [Ruff](https://docs.astral.sh/ruff/) and [DjHTML](https://github.com/rtts/djhtml), and detecting any private keys you may have accidentally added to the repository. For a full list see the file `<install-directory>/.pre-commit-config.yaml`.

Run pre-commit install to set up the git hook scripts

```
$ pre-commit install
```

Now pre-commit will run automatically on git commit.

### Configuration

Create a local environment file by copying `<install-directory>/core/.env_example` to `<install-directory>/core/.env` and filling out the details.

Run the migrations and create the superuser:

```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

Finally, start the development server:

```
$ python manage.py runserver_plus
```

## Deployment

Change to the installation directory:

```
$ cd /path/to/install
```

Activate the server python environment:

```
$ source .venv/bin.activate
```

Checkout the latest code:

```
$ git pull
```

Run any migrations:

```
$ python manage.py migrate
```

Compile the SCSS:

```
$ python manage.py compilescss
```

Collect the static assets:

```
$ python manage.py collectstatic
```

Trigger the web server to reload the files (in this case updating the access time on the `wsgi` file will update Apache)

```
$ touch core/wsgi.py
```
