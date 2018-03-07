# Basic Development with Flask and Microblog

## Templates

By now, you should have a fully working, yet simple web application that 
has the following file structure:

```
microblog.git\
  venv\
  app\
    __init__.py
    routes.py
  microblog.py
```

To run the application, make sure `FLASK_APP=microblog.py` is set in 
your terminal session, and then execute `flask run`. This starts a web 
server with the application, which you can open by typing 
the **http://localhost:5000/** URL in your web browser's address bar.

In this section, you will continue working on the same application, and 
in particular, you are going to learn how to generate more elaborated 
web pages that have a complex structure and many dynamic components.

### Preparing yourself for working with templates

I want the home page of my microblogging application to have a heading 
that welcomes the user. For the moment, ignore that the application does 
not have the concept of users yet, as this is going to come later. For 
now, I'm going to use a *mock* user, which I'm going to implement as a 
Python dictionary, as follows:

```python
user = {'username': 'José A.'}
```

Creating mock objects is a useful technique that allows you to 
concentrate on one part of the application without having to worry about 
other parts of the system that don't exist yet. I want to design the 
home page of my application, and I don't want the fact that I don't have 
a user system in place to distract me, so I just make up a user object 
so that I can keep going.

The view function in the application returns a simple string. What I 
want to do now is expand that returned string into a complete HTML page, 
maybe something like this:

```python
# app/routes.py: Return complete HTML page from view function
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'José A.'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''
```

Update the view function as shown above and give the application a try 
to see how it looks in your browser.

![img](01-templates-a.png)
