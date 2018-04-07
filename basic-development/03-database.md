# Basic Development with Flask and Microblog

## Database

### Introduction

The topic of this section is extremely important. For most applications,
there is going to be a need to maintain persistent data that can be 
retrieved efficiently, and this is exactly what *databases* are made 
for.

### Databases in Flask

As I'm sure you have heard already, Flask does not support databases 
natively. This is one of the many areas in which Flask is intentionally 
not opinionated, which is great, because you have the freedom to choose 
the database that best fits your application instead of being forced to 
adapt to one.

There are great choices for databases in Python, many of them with Flask 
extensions that make a better integration with the application. The 
databases can be separated into two big groups, those that follow 
the *relational* model, and those that do not. The latter group is often 
called *NoSQL*, indicating that they do not implement the popular 
relational query language [SQL](https://en.wikipedia.org/wiki/SQL). 
While there are great database products in both groups, my opinion is 
that relational databases are a better match for applications that have 
structured data such as lists of users, blog posts, etc., while NoSQL 
databases tend to be better for data that has a less defined structure. 
This application, like most others, can be implemented using either type 
of database, but for the reasons stated above, I'm going to go with a 
relational database.

In the previous section, I showed you a first Flask extension. In this 
part I'm going to use two more. The first 
is [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/), an 
extension that provides a Flask-friendly wrapper to the 
popular [SQLAlchemy](http://www.sqlalchemy.org/) package, which is 
an [Object Relational Mapper](https://en.wikipedia.org/wiki/Object-relational_mapping) 
or ORM. ORMs allow applications to manage a database using high-level 
entities such as classes, objects and methods instead of tables and SQL. 
The job of the ORM is to translate the high-level operations into 
database commands.

The nice thing about SQLAlchemy is that it is an ORM not for one, but 
for many relational databases. SQLAlchemy supports a long list of 
database engines, including the popular [MySQL](https://www.mysql.com/)
, [PostgreSQL](https://www.postgresql.org/) 
and [SQLite](https://www.sqlite.org/index.html). This is extremely 
powerful, because you can do your development using a simple SQLite 
database that does not require a server, and then when the time comes to 
deploy the application on a production server you can choose a more 
robust MySQL or PostgreSQL server, without having to change your 
application.

To install Flask-SQLAlchemy in your virtual environment, make sure you 
have activated it first, and the run:

```
(venv) $ pip install flask-sqlalchemy
```

### Database Migrations

Most database tutorials I've seen cover creation and use of a database, 
but do not adequately address the problem of making updates to an 
existing database as the application needs change or grow. This is hard 
because relational databases are centered around structured data, so 
when the structure changes the data that is already in the database 
needs to be *migrated* to the modified structure.

The second extension that I'm going to present in this part 
is [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate), 
which is actually one created by yours truly. This extension is a Flask 
wrapper for [Alembic](https://bitbucket.org/zzzeek/alembic), a database 
migration framework for SQLAlchemy. Working with database migrations 
adds a bit of work to get a database started, but that is a small price 
to pay for a robust way to make changes to your database in the future.

The installation process for Flask-Migrate is similar to other 
extensions you have seen:

```
(venv) $ pip install flask-migrate
```

### Flask-SQLAlchemy Configuration

During development, I'm going to use a SQLite database. SQLite databases 
are the most convenient choice for developing small applications, 
sometimes even not so small ones, as each database is stored in a single 
file on disk and there is no need to run a database server like MySQL 
and PostgreSQL.

We have two new configuration items to add to the config file:

```python
# config.py: Flask-SQLAlchemy configuration
import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

The Flask-SQLAlchemy extension takes the location of the application's 
database from the `SQLALCHEMY_DATABASE_URI` configuration variable. As 
you recall from the previous section, it is, in general a good practice 
to set configuration from environment variables, and provide a fallback 
value when the environment does not define the variable. In this case 
I'm taking the database URL from the `DATABASE_URL` environment 
variable, and if that isn't defined, I'm configuring a database 
named *app.db* located in the main directory of the application, which 
is stored in the `basedir` variable.

The `SQLALCHEMY_TRACK_MODIFICATIONS` configuration option is set 
to `False` to disable a feature of Flask-SQLAlchemy that I do not need, 
which is to signal the application every time a change is about to be 
made in the database.

The database is going to be represented in the application by 
the *database instance*. The database migration engine will also have an 
instance. These are objects that need to be created after the 
application, in the *app/__init__.py* file:

```python
# app/__init__.py: Flask-SQLAlchemy and Flask-Migrate initialization
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
```

I have made three changes to the init script. First, I have added a `db` 
object that represents the database. Then, I have added another object 
that represents the migration engine. Hopefully you see a pattern in how 
to work with Flask extensions. Most extensions are initialized as these 
two. Finally, I'm importing a new module called `models` at the bottom. 
This module will define the structure of the database.

### Database Models

The data that will be stored in the database will be represented by a 
collection of classes, usually called *database models*. The ORM layer 
within SQLAlchemy will do the translations required to map objects 
created from these classes into rows in the proper database tables.

Let's start by creating a model that represents users. The data is 
represented like this:

```
users
-----
id                 INTEGER
username           VARCHAR(64)
email              VARCHAR(120)
password_hash      VARCHAR(128)
```

The `id` field is usually in all models, and is used as 
the *primary key*. Each user in the database will be assigned a unique 
id value, stored in this field. Primary keys are, in most cases, 
automatically assigned by the database, so I just need to provide 
the `id` field marked as a primary key.

The `username`, `email` and `password_hash` fields are defined as 
strings (or `VARCHAR` in database jargon), and their maximum lengths are 
specified so that the database can optimize space usage. While 
the `username` and `email` fields are self-explanatory, 
the `password_hash` field deserves some attention. I want to make sure 
the application that I'm building adopts security best practices, and 
for that reason I will not be storing user passwords in the database. 
The problem with storing passwords is that if the database ever becomes 
compromised, the attackers will have access to the passwords, and that 
could be devastating for users. Instead of writing the passwords 
directly, I'm going to write *password hashes*, which greatly improve 
security. This is going to be the topic of another section, so don't 
worry about it too much for now.

So now that I know what I want for my users table, I can translate that 
into code in the new *app/models.py* module:

```python
# app/models.py: User database model
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'
```

The `User` class created above inherits from `db.Model`, a base class 
for all models from Flask-SQLAlchemy. This class defines several fields 
as class variables. Fields are created as instances of the `db.Column` 
class, which takes the field type as an argument, plus other optional 
arguments that, for example, allow me to indicate which fields are 
unique and indexed, which is important so that database searches are 
efficient.

The `__repr__` method tells Python how to print objects of this class, 
which is going to be useful for debugging. You can see the `__repr__()` 
method in action in the Python interpreter session below:

```python
>>> from app.models import User
>>> u = User(username='mary', email='mary@mail.com')
>>> u
<User mary>
```
