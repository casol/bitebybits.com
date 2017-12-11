# FromBitsToBytes

Simple and clean Django App for personal blog. You can easily write complex blog posts, upload images, add tags, let users comment the posts.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

Try it locally:

Download or "git clone" the package:
```
$ git clone https://github.com/casol/frombitstobytes.git
$ cd frombitstobytes
```
First install the module, preferably in a virtual environment:
```
$ pip install -r ../requirements.txt
```
Initiate the migration and then migrate the database:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Create an admin user:
```
$ python manage.py createsuperuser
```
Setup a local server:
```
$ python manage.py runserver
```

## Deployment

Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 16.04 hosted on [DigitalOcean](https://m.do.co/c/750db310081f)

### See It Live

[https://frombitstobytes.com/](https://frombitstobytes.com/)

## Built With

* [Django](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Bootstrap](https://getbootstrap.com/) - Bootstrap
* [CKEditor](https://maven.apache.org/) - Rich Text Editor
* [Pillow](https://pillow.readthedocs.io/en/4.3.x/) - Python Imaging Library
* [Disqus](https://django-disqus.readthedocs.io/en/latest/) - Disqus
* [django-taggit](https://github.com/alex/django-taggit) - Simple tagging for django

## Features

* Rich Text Editor
* Highlight code snippets
* Comments
* Sitemaps
* reCAPTCHA
* RSS or Atom Feeds
* Tags
* Image uploader
* Cookie Policy
* Social Share
* Contact Form

## Authors

* **Krzysztof Sołtys** - *Initial work* - [casol](https://github.com/casol)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/casol/frombitstobytes/blob/master/LICENSE.md) file for details

## Acknowledgments

* Looking for great themes&templates? Check [Blackrock Digital](https://github.com/BlackrockDigital)
