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
