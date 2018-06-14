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

### Flask-Mail Usage

To learn how Flask-Mail works, I'll show you how to send an email from a 
Python shell. So fire up Python with `flask shell`, and then run the 
following commands:

```python
>>> from flask_mail import Message
>>> from app import mail
>>> msg = Message('test subject', sender=app.config['ADMINS'][0],
... recipients=['your-email@example.com'])
>>> msg.body = 'text body'
>>> msg.html = '<h1>HTML body</h1>'
>>> mail.send(msg)
```

The snippet of code above will send an email to a list of email 
addresses that you put in the `recipients` argument. I put the sender as 
the first configured admin (I've added the `ADMINS` configuration 
variable in a previous section). The email will have plain text and HTML 
versions, so depending on how your email client is configured you may 
see one or the other.

So as you see, this is pretty simple. Now let's integrate emails into 
the application.

### A Simple Email Framework

I will begin by writing a helper function that sends an email, which is 
basically a generic version of the shell exercise from the previous 
section. I will put this function in a new module called *app/email.py*:

```python
# app/email.py: Email sending wrapper function
from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
```

Flask-Mail supports some features that I'm not utilizing here such as Cc 
and Bcc lists. Be sure to check 
the [Flask-Mail](https://pythonhosted.org/Flask-Mail/) documentation if 
you are interested in those options.

### Requesting a Password Reset

As I mentioned above, I want users to have the option to request their 
password to be reset. For this purpose I'm going to add a link in the 
login page:

```html
    ...
    <p>
        Forgot Your Password?
        <a href="{{ url_for('reset_password_request') }}">Click to Reset It</a>
    </p>
    ...
```

When the user clicks the link, a new web form will appear that requests 
the user's email address as a way to initiate the password reset 
process. Here is the form class:

```python
# app/forms.py: Reset password request form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
```

And here is the corresponding HTML template 
in *app/templates/reset_password_request.html*:

```html
{% extends "base.html" %}

{% block content %}
    <h1>Reset Password</h1>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=64) }}<br>
            {% for error in form.email.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

I also need a view function to handle this form:

```python
# app/routes.py: Reset password request view function
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', 
                           title = 'Reset Password', 
                           form = form)
```

This view function is fairly similar to others that process a form. I 
start by making sure the user is not logged in. If the user is logged 
in, then there is no point in using the password reset functionality, so 
I redirect to the index page.

When the form is submitted and valid, I look up the user by the email 
provided by the user in the form. If I find the user, I send a password 
reset email. I'm using a `send_password_reset_email()` helper function 
to do this. I will show you this function below.

After the email is sent, I flash a message directing the user to look 
for the email for further instructions, and then redirect back to the 
login page. You may notice that the flashed message is displayed even if 
the email provided by the user is unknown. This is so that clients 
cannot use this form to figure out if a given user is a member or not.
