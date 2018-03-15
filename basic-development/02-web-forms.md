# Basic Development with Flask and Microblog

## Web Forms

### Introduction

Previously, I created a simple template for the home page of the 
application, and used fake objects as placeholders for things I don't 
have yet, like users or blog posts.

In this part, I'm going to fill one of those many holes I still have in 
this application, specifically how to accept input from users through 
web forms.

Web forms are one of the most basic building blocks in any web 
application. I will be using forms to allow users to submit blog posts, 
and also for logging in to the application.

Before you proceed here, make sure you have the *microblog* application 
as I left it in the previous part, and that you can run it without any 
errors.

### Introduction to Flask-WTF

To handle the web forms in this application, I'm going to use 
the [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) extension, 
which is a thin wrapper around 
the [WTForms](https://wtforms.readthedocs.io/en/stable/) package that 
nicely integrates it with Flask. This is the first Flask extension that 
I'm presenting to you, but it is not going to be the last. Extensions 
are a very important part of the Flask ecosystem, as they provide 
solutions to problems that Flask is intentionally not opinionated about.

Flask extensions are regular Python packages that are installed 
with `pip`. You can go ahead and install Flask-WTF on your virtual 
environment:

```
$ cd microblog.git/
$ source venv/bin/activate
(venv) $ pip install flask-wtf
```

### Configuration

So far the application is very simple, and for that reason I did not 
need to worry about its *configuration*. But for any applications except 
the simplest ones, you are going to find that Flask (and possibly also 
the Flask extensions that you use) offer some amount of freedom in how 
to do things, and you need to make some decisions, which you pass to the 
framework as a list of configuration variables.

There are several formats for the application to specify configuration 
options. The most basic solution is to define your variables as keys 
in `app.config`, which uses a dictionary style to set or read 
configuration variables. For example, you could do something like this:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
# ... add more variables here as needed
```

While the above syntax is sufficient to create configuration options for 
Flask, I like to enforce the principle of *separation of concerns*, so 
instead of putting my configuration in the same place where I create my 
application, I will use a slightly more elaborate structure that allows 
me to keep my configuration in a separate file.

A format that I really like because it is very extensible, is to use a 
class to store configuration variables. To keep things nicely organized, 
I'm going to create the configuration class in a separate Python module. 
Below you can see the new configuration class for this application, 
stored in a *config.py* module in the top-level directory. Let's see:

```python
# config.py: Secret key configuration
import secrets
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

Pretty simple, right? The configuration settings are defined as class 
variables inside the `Config` class. As the application needs more 
configuration items, they can be added to this class, and later if I 
find that I need to have more than one configuration set, I can create 
subclasses of it. But don't worry about this just yet.

The `SECRET_KEY` configuration variable that I added as the only 
configuration item is an important part in most Flask applications. 
Flask and some of its extensions use the value of the secret key as a 
cryptographic key, useful to generate signatures or tokens. The 
Flask-WTF extension uses it to protect web forms against a nasty attack 
called [Cross-Site Request Forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery)
or CSRF (pronounced "seasurf"). As its name implies, the secret key is 
supposed to be secret, as the strength of the tokens and signatures 
generated with it depends on no person outside of the trusted 
maintainers of the application knowing it.

The value of the secret key is set as an expression with two terms, 
joined by the `or` operator. The first term looks for the value of an 
environment variable, also called `SECRET_KEY`. The second term, is a 
value generated with the `secrets` library, which, in this case, is 
considered a hardcoded string. This is a pattern that you will see me 
repeat often for configuration variables. The idea is that a value 
sourced from an environment variable is preferred, but if the 
environment does not define the variable, then the hardcoded string is 
used instead. When you are developing this application, the security 
requirements are low, so you can just ignore this setting and let the 
hardcoded string be used. But, when this application is deployed on a 
production server, I will be setting a unique and difficult to guess 
value in the environment, so that the server has a secure key that 
nobody else knows.

Now that I have a config file, I need to tell Flask to read it and apply 
it. That can be done right after the Flask application instance is 
created using the `app.config.from_object()` method:

```python
# app/__init__.py: Flask configuration
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
```

The way I'm importing the `Config` class may seem confusing at first, 
but if you look at how the `Flask` class (uppercase "F") is imported 
from the `flask` package (lowercase "f") you'll notice that I'm doing 
the same with the configuration. The lowercase "config" is the name of 
the Python module *config.py*, and obviously the one with the uppercase 
"C" is the actual class.

As I mentioned above, the configuration items can be accessed with a 
dictionary syntax from `app.config`. Here you can see a quick session 
with the Python interpreter where I check what is the value of the 
secret key:

```python
>>> from microblog import app
>>> app.config['SECRET_KEY']
'ca7e5774383466f46e382229251a83059f3255219a5dbf87309c58d5f6a4c7b1'
```
