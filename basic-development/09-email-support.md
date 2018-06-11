# Basic Development with Flask and Microblog

## Email Support

### Introduction

The application is doing pretty well on the database front now, so in 
this section I want to depart from that topic and add another important 
piece that most web applications need, which is the sending of emails.

Why does an application need to email its users? There are many reasons, 
but one common one is to solve authentication related problems. In this 
section, I'm going to add a password reset feature for users that forget 
their password. When a user requests a password reset, the application 
will send an email with a specially crafted link. The user then needs to 
click that link to have access to a form in which to set a new password.

### Introduction to Flask-Mail

As far as the actual sending of emails, Flask has a popular extension 
called [Flask-Mail](https://pythonhosted.org/Flask-Mail/) that can make 
the task very easy. As always, this extension is installed with pip:

```
(venv) $ pip install flask-mail
```

The password reset links will have a secure token in them. To generate 
these tokens, I'm going to use [JSON Web Tokens](https://jwt.io/), which 
also have a popular Python package:

```
(venv) $ pip install pyjwt
```

The Flask-Mail extension is configured from the `app.config` object. 
Remember when in a previous section I added the email configuration for 
sending yourself an email whenever an error occurred in production? I 
did not tell you this then, but my choice of configuration variables was 
modeled after Flask-Mail's requirements, so there isn't really any 
additional work that is needed, the configuration variables are already 
in the application.

Like most Flask extensions, you need to create an instance right after 
the Flask application is created. In this case this is an object of 
class `Mail`:

```python
# app/__init__.py: Flask-Mail instance
# ...
from flask_mail import Mail

app = Flask(__name__)
# ...
mail = Mail(app)
```

If you are planning to test sending of emails you have the same two 
options I mentioned before. If you want to use an emulated email server, 
Python provides one that is very handy that you can start in a second 
terminal with the following command:

```
(venv) $ python -m smtpd -n -c DebuggingServer localhost:8025
```

To configure for this server you will need to set two environment 
variables:

```
(venv) $ export MAIL_SERVER=localhost
(venv) $ export MAIL_PORT=8025
```

If you prefer to have emails sent for real, you need to use a real email 
server. If you have one, then you just need to set the `MAIL_SERVER`
, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME` and `MAIL_PASSWORD` 
environment variables for it. If you want a quick solution, you can use 
a Gmail account to send email, with the following settings:

```
(venv) $ export MAIL_SERVER=smtp.googlemail.com
(venv) $ export MAIL_PORT=587
(venv) $ export MAIL_USE_TLS=1
(venv) $ export MAIL_USERNAME=<your-gmail-username>
(venv) $ export MAIL_PASSWORD=<your-gmail-password>
```

Remember that the security features in your Gmail account may prevent 
the application from sending emails through it unless you explicitly 
allow "less secure apps" access to your Gmail account. You can read 
about this [here](https://support.google.com/accounts/answer/6010255?hl=en), 
and if you are concerned about the security of your account, you can 
create a secondary account that you configure just for testing emails, 
or you can enable less secure apps only temporarily to run your tests 
and then revert back to the more secure default.
