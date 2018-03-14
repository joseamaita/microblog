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

Flask extensions are regular Python packages that are installed with 
pip. You can go ahead and install Flask-WTF on your virtual environment:

```
$ cd microblog.git/
$ source venv/bin/activate
(venv) $ pip install flask-wtf
```
