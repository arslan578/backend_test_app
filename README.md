# Backend Setup

This is a repository for a web application developed with Django, built with gromomarketingdev

### Features

1. **Local Authentication** using email and password with [allauth](https://pypi.org/project/django-allauth/)
2. **Rest API** using [django rest framework](http://www.django-rest-framework.org/)
3. **Forgot Password**

# Development

Following are instructions on setting up your development environment.


## Application Setup

1. [Python](https://www.python.org/downloads/release/python-389/)

### Installation

1. Install [pipenv](https://pypi.org/project/pipenv/)
2. Clone this repo and `cd backend_app`
3. Run `pip install --user --upgrade pipenv` to get the latest pipenv version.
4. Run `pipenv --python 3.8.9`
5. Run `pipenv install`
6. Run `cp .env.example .env`