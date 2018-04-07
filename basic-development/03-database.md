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
