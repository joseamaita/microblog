# Basic Development with Flask and Microblog

## User Logins

### Introduction

Previously, you learned how to create the user login form and how to 
work with a database. This part will teach you how to combine the 
topics from those two sections to create a simple user login system.

### Password Hashing

If you remember, previously, the user model was given a `password_hash` 
field, that so far is unused. The purpose of this field is to hold a 
hash of the user password, which will be used to verify the password 
entered by the user during the log in process. Password hashing is a 
complicated topic that should be left to security experts, but there are 
several easy to use libraries that implement all that logic in a way 
that is simple to be invoked from an application.

One of the packages that implement password hashing 
is [Werkzeug](http://werkzeug.pocoo.org/), which you may have seen 
referenced in the output of pip when you install Flask, since it is one 
of its core dependencies. Since it is a dependency, Werkzeug is already 
installed in your virtual environment. The following Python shell 
session demonstrates how to hash a password:

```python
>>> from werkzeug.security import generate_password_hash
>>> hash = generate_password_hash('foobar')
>>> hash
'pbkdf2:sha256:50000$33kYRkx2$953df8b0be8693f8eb608547d23a57c9e7195d0689b0d179881d59c3d1a7a7a6'
```

In this example, the password `foobar` is transformed into a long 
encoded string through a series of cryptographic operations that have no 
known reverse operation, which means that a person that obtains the 
hashed password will be unable to use it to obtain the original 
password. As an additional measure, if you hash the same password 
multiple times, you will get different results, so this makes it 
impossible to identify if two users have the same password by looking at 
their hashes.

The verification process is done with a second function from Werkzeug, 
as follows:

```python
>>> from werkzeug.security import check_password_hash
>>> check_password_hash(hash, 'foobar')
True
>>> check_password_hash(hash, 'barfoo')
False
```

The verification function takes a password hash that was previously 
generated, and a password entered by the user at the time of log in. The 
function returns `True` if the password provided by the user matches the 
hash, or `False` otherwise.

The whole password hashing logic can be implemented as two new methods 
in the user model:

```python
# app/models.py: Password hashing and verification
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

With these two methods in place, a user object is now able to do secure 
password verification, without the need to ever store original 
passwords. Here is an example usage of these new methods 
(use `flask shell`):

```
>>> u = User(username='mary', email='mary@mail.com')
>>> u.set_password('mypassword')
>>> u.check_password('anotherpassword')
False
>>> u.check_password('mypassword')
True
```
