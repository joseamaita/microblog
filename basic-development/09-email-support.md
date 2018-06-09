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
