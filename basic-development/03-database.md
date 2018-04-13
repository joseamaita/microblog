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

### Creating the Migration Repository

The model class created above defines the initial database structure (or 
schema) for this application. But as the application continues to grow, 
there is going to be a need to change that structure, very likely to add 
new things, but sometimes also to modify or remove items. Alembic (the 
migration framework used by Flask-Migrate) will make these schema 
changes in a way that does not require the database to be recreated from 
scratch.

To accomplish this seemingly difficult task, Alembic maintains 
a *migration repository*, which is a directory in which it stores its 
migration scripts. Each time a change is made to the database schema, a 
migration script is added to the repository with the details of the 
change. To apply the migrations to a database, these migration scripts 
are executed in the sequence they were created.

Flask-Migrate exposes its commands through the `flask` command. You have 
already seen `flask run`, which is a sub-command that is native to 
Flask. The `flask db` sub-command is added by Flask-Migrate to manage 
everything related to database migrations. So let's create the migration 
repository for microblog by running `flask db init`:

```
(venv) $ flask db init
  Creating directory ~/microblog.git/migrations ... done
  Creating directory ~/microblog.git/migrations/versions ... done
  Generating ~/microblog.git/migrations/env.py ... done
  Generating ~/microblog.git/migrations/README ... done
  Generating ~/microblog.git/migrations/script.py.mako ... done
  Generating ~/microblog.git/migrations/alembic.ini ... done
  Please edit configuration/connection/logging settings in 
  '~/microblog.git/migrations/alembic.ini' before proceeding.
```

Remember that the `flask` command relies on the `FLASK_APP` environment 
variable to know where the Flask application lives. For this 
application, you want to set `FLASK_APP=microblog.py`.

After you run this command, you will find a new *migrations* directory, 
with a few files and a *versions* sub-directory inside. All these files 
should be treated as part of your project from now on, and in 
particular, should be added to source control.

### The First Database Migration

With the migration repository in place, it is time to create the first 
database migration, which will include the users table that maps to 
the `User` database model. There are two ways to create a database 
migration: manually or automatically. To generate a migration 
automatically, Alembic compares the database schema as defined by the 
database models, against the actual database schema currently used in 
the database. It then populates the migration script with the changes 
necessary to make the database schema match the application models. In 
this case, since there is no previous database, the automatic migration 
will add the entire `User` model to the migration script. 
The `flask db migrate` sub-command generates these automatic migrations: 

```
(venv) $ flask db migrate -m "users table"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
  Generating ~/microblog.git/migrations/versions/f15a034db877_users_table.py ... done
```

The output of the command gives you an idea of what Alembic included in 
the migration. The first two lines are informational and can usually be 
ignored. It then says that it found a user table and two indexes. Then 
it tells you where it wrote the migration script. The `f15a034db877` 
code is an automatically generated unique code for the migration (it 
will be different for you). The comment given with the `-m` option is 
optional, it adds a short descriptive text to the migration.

The generated migration script is now part of your project, and needs to 
be incorporated to source control. You are welcome to inspect the script 
if you are curious to see how it looks. You will find that it has two 
functions called `upgrade()` and `downgrade()`. The `upgrade()` function 
applies the migration, and the `downgrade()` function removes it. This 
allows Alembic to migrate the database to any point in the history, even 
to older versions, by using the downgrade path.

The `flask db migrate` command does not make any changes to the 
database, it just generates the migration script. To apply the changes 
to the database, the `flask db upgrade` command must be used.

```
(venv) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> f15a034db877, users table
```

Because this application uses SQLite, the `upgrade` command will detect 
that a database does not exist and will create it (you will notice a 
file named *app.db* is added after this command finishes, that is the 
SQLite database). When working with database servers such as MySQL and 
PostgreSQL, you have to create the database in the database server 
before running `upgrade`.

Note that Flask-SQLAlchemy uses a "snake case" naming conversion for 
database tables by default. For the `User` model above, the 
corresponding table in the database will be named `user`. For 
a  `AddressAndPhone` model class, the table would be 
named `address_and_phone`. If you prefer to choose your own table names, 
you can add an attribute named `__tablename__` to the model class, set 
to the desired name as a string.

### Database Upgrade and Downgrade Workflow

The application is in its infancy at this point, but it does not hurt to 
discuss what is going to be the database migration strategy going 
forward. Imagine that you have your application on your development 
machine, and also have a copy deployed to a production server that is 
online and in use.

Let's say that for the next release of your app you have to introduce a 
change to your models, for example, a new table needs to be added. 
Without migrations you would need to figure out how to change the schema 
of your database, both in your development machine and then again in 
your server, and this could be a lot of work.

But with database migration support, after you modify the models in your 
application you generate a new migration script ( `flask db migrate` ), 
you probably review it to make sure the automatic generation did the 
right thing, and then apply the changes to your development database 
( `flask db upgrade` ). You will add the migration script to source 
control and commit it.

When you are ready to release the new version of the application to your 
production server, all you need to do is grab the updated version of 
your application, which will include the new migration script, and 
run `flask db upgrade`. Alembic will detect that the production database 
is not updated to the latest revision of the schema, and run all the new 
migration scripts that were created after the previous release.

As I mentioned earlier, you also have a `flask db downgrade` command, 
which undoes the last migration. While you will be unlikely to need this 
option on a production system, you may find it very useful during 
development. You may have generated a migration script and applied it, 
only to find that the changes that you made are not exactly what you 
need. In this case, you can downgrade the database, delete the migration 
script, and then generate a new one to replace it.

### Database Relationships

Relational databases are good at storing relations between data items. 
Consider the case of a user writing a blog post. The user will have a 
record in the `users` table, and the post will have a record in 
the `posts` table. The most efficient way to record who wrote a given 
post is to link the two related records.

Once a link between a user and a post is established, the database can 
answer queries about this link. The most trivial one is when you have a 
blog post and need to know what user wrote it. A more complex query is 
the reverse of this one. If you have a user, you may want to know all 
the posts that this user wrote. Flask-SQLAlchemy will help with both 
types of queries.

Let's expand the database to store blog posts to see relationships in 
action. Here is the schema for a new `posts` table:

```
users                                        posts
-----                                        -----
id                 INTEGER     -------       id             INTEGER
username           VARCHAR(64)       |       body           VARCHAR(140)
email              VARCHAR(120)      |       timestamp      DATETIME
password_hash      VARCHAR(128)      ------- user_id        INTEGER
```

The `posts` table will have the required `id`, the `body` of the post 
and a `timestamp`. But in addition to these expected fields, I'm adding 
a `user_id` field, which links the post to its author. You've seen that 
all users have a `id` primary key, which is unique. The way to link a 
blog post to the user that authored it is to add a reference to the 
user's `id`, and that is exactly what the `user_id` field is. 
This `user_id` field is called a *foreign key*. The database diagram 
above shows foreign keys as a link between the field and the `id` field 
of the table it refers to. This kind of relationship is called 
a *one-to-many*, because "one" user writes "many" posts.

The modified *app/models.py* is shown below:

```python
# app/models.py: Posts database table and relationship
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, 
                          index = True, 
                          default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}>'
```

The new `Post` class will represent blog posts written by users. 
The `timestamp` field is going to be indexed, which is useful if you 
want to retrieve posts in chronological order. I have also added 
a `default` argument, and passed the `datetime.utcnow` function. When 
you pass a function as a default, SQLAlchemy will set the field to the 
value of calling that function (note that I did not include the `()` 
after `utcnow`, so I'm passing the function itself, and not the result 
of calling it). In general, you will want to work with UTC dates and 
times in a server application. This ensures that you are using uniform 
timestamps regardless of where the users are located. These timestamps 
will be converted to the user's local time when they are displayed.

The `user_id` field was initialized as a foreign key to `user.id`, which 
means that it references an `id` value from the users table. In this 
reference, the `user` part is the name of the database table for the 
model. It is an unfortunate inconsistency that in some instances such as 
in a `db.relationship()` call, the model is referenced by the model 
class, which typically starts with an uppercase character, while in 
other cases such as this `db.ForeignKey()` declaration, a model is given 
by its database table name, for which SQLAlchemy automatically uses 
lowercase characters and, for multi-word model names, snake case.

The `User` class has a new `posts` field, that is initialized 
with `db.relationship`. This is not an actual database field, but a 
high-level view of the relationship between users and posts, and for 
that reason it isn't in the database diagram. For a one-to-many 
relationship, a `db.relationship` field is normally defined on the "one" 
side, and is used as a convenient way to get access to the "many". So, 
for example, if I have a user stored in `u`, the expression `u.posts` 
will run a database query that returns all the posts written by that 
user. The first argument to `db.relationship` is the model class that 
represents the "many" side of the relationship. This argument can be 
provided as a string with the class name if the model is defined later 
in the module. The `backref` argument defines the name of a field that 
will be added to the objects of the "many" class that points back at the 
"one" object. This will add a `post.author` expression that will return 
the user given a post. The `lazy` argument defines how the database 
query for the relationship will be issued.

Since I have updates to the application models, a new database migration 
needs to be generated:

```
(venv) $ flask db migrate -m "posts table"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'post'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_post_timestamp' on '['timestamp']'
  Generating ~/microblog.git/migrations/versions/41cf27f62f9a_posts_table.py ... done
```

And the migration needs to be applied to the database:

```
(venv) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade f15a034db877 -> 41cf27f62f9a, posts table
```

If you are storing your project in source control, also remember to add 
the new migration script to it.

### Play Time

I have made you suffer through a long process to define the database, 
but I haven't shown you how everything works yet. Since the application 
does not have any database logic yet, let's play with the database in 
the Python interpreter to familiarize with it. So go ahead and fire up 
Python by running `python`. Make sure your virtual environment is 
activated before you start the interpreter.

Once in the Python prompt, let's import the database instance and the 
models:

```python
>>> from app import db
>>> from app.models import User, Post
```

Start by creating a new user:

```python
>>> u = User(username='mary', email='mary@mail.com')
>>> db.session.add(u)
>>> db.session.commit()
```

Changes to a database are done in the context of a session, which can be 
accessed as `db.session`. Multiple changes can be accumulated in a 
session and once all the changes have been registered you can issue a 
single `db.session.commit()`, which writes all the changes atomically. 
If at any time while working on a session there is an error, a call 
to `db.session.rollback()` will abort the session and remove any changes 
stored in it. The important thing to remember is that changes are only 
written to the database when `db.session.commit()` is called. Sessions 
guarantee that the database will never be left in an inconsistent state.

Let's add another user:

```python
>>> u = User(username='lucy', email='lucy@mail.com')
>>> db.session.add(u)
>>> db.session.commit()
```

The database can answer a query that returns all the users:

```python
>>> users = User.query.all()
>>> users
[<User mary>, <User lucy>]
>>> for u in users:
...     print(u.id, u.username)
...
1 mary
2 lucy
```

All models have a `query` attribute that is the entry point to run 
database queries. The most basic query is that one that returns all 
elements of that class, which is appropriately named `all()`. Note that 
the `id` fields were automatically set to 1 and 2 when those users were 
added.

Here is another way to do queries. If you know the `id` of a user, you 
can retrieve that user as follows:

```python
>>> u = User.query.get(1)
>>> u
<User mary>
>>> u = User.query.get(2)
>>> u
<User lucy>
```

Now let's add a blog post:

```python
>>> u = User.query.get(1)
>>> p = Post(body='This is my first post with Microblog!', author=u)
>>> db.session.add(p)
>>> db.session.commit()
```

I did not need to set a value for the `timestamp` field because that 
field has a default, which you can see in the model definition. And what 
about the `user_id` field? Recall that the `db.relationship` that I 
created in the `User` class adds a `posts` attribute to users, and also 
an `author` attribute to posts. I assign an author to a post using 
the `author` virtual field instead of having to deal with user IDs. 
SQLAlchemy is great in that respect, as it provides a high-level 
abstraction over relationships and foreign keys.

To complete this session, let's look at a few more database queries:

```python
>>> # get all posts written by a user
>>> u = User.query.get(1)
>>> u
<User mary>
>>> posts = u.posts.all()
>>> posts
[<Post This is my first post with Microblog!>]

>>> # same, but with a user that has no posts
>>> u = User.query.get(2)
>>> u
<User lucy>
>>> u.posts.all()
[]

>>> # print post author and body for all posts 
>>> posts = Post.query.all()
>>> for p in posts:
...     print(p.id, p.author.username, p.body)
...
1 mary This is my first post with Microblog!

# get all users in alphabetical order
>>> User.query.order_by(User.username.asc()).all()
[<User lucy>, <User mary>]
```

The [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) 
documentation is the best place to learn about the many options that are 
available to query the database.

To complete this section, let's erase the test users and posts created 
above, so that the database is clean and ready for future 
experimentation:

```python
>>> users = User.query.all()
>>> users
[<User mary>, <User lucy>]
>>> for u in users:
...     db.session.delete(u)
...
>>> posts = Post.query.all()
>>> posts
[<Post This is my first post with Microblog!>]
>>> for p in posts:
...     db.session.delete(p)
...
>>> db.session.commit()
>>> User.query.all()
[]
>>> Post.query.all()
[]
```
