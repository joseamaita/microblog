# Basic Development with Flask and Microblog

## Followers

### Introduction

In this section, I'm going to work on the application's database some 
more. I want users of the application to be able to easily choose which 
other users they want to follow. So, I'm going to be expanding the 
database so that it can keep track of who is following whom, which is 
harder than you may think.

### Database Relationships Revisited

I said above that I want to maintain a list of "followed" and "follower" 
users for each user. Unfortunately, a relational database does not have 
a list type that I can use for these lists, all there is are tables with 
records and relationships between these records.

The database has a table that represents users, so what's left is to 
come up with the proper relationship type that can model the 
follower/followed link. This is a good time to review the basic database 
relationship types:

**One-to-Many**

I have already used a one-to-many relationship previously. Here is the 
diagram for this relationship:

```
users                                        posts
-----                                        -----
id                 INTEGER     -------       id             INTEGER
username           VARCHAR(64)       |       body           VARCHAR(140)
email              VARCHAR(120)      |       timestamp      DATETIME
password_hash      VARCHAR(128)      ------- user_id        INTEGER
```

The two entities linked by this relationship are users and posts. I say 
that a user has *many* posts, and a post has *one* user (or author). The 
relationship is represented in the database with the use of 
a *foreign key* on the "many" side. In the relationship above, the 
foreign key is the `user_id` field added to the `posts` table. This 
field links each post to the record of its author in the user table.

It is pretty clear that the `user_id` field provides direct access to 
the author of a given post, but what about the reverse direction? For 
the relationship to be useful I should be able to get the list of posts 
written by a given user. The `user_id` field in the `posts` table is 
also sufficient to answer this question, as databases have indexes that 
allow for efficient queries such us "retrieve all posts that have 
a `user_id` of X".

**Many-to-Many**

A many-to-many relationship is a bit more complex. As an example, 
consider a database that has `students` and `teachers`. I can say that a 
student has *many* teachers, and a teacher has *many* students. It's 
like two overlapped one-to-many relationships from both ends.

For a relationship of this type I should be able to query the database 
and obtain the list of teachers that teach a given student, and the list 
of students in a teacher's class. This is actually non-trivial to 
represent in a relational database, as it cannot be done by adding 
foreign keys to the existing tables.

The representation of a many-to-many relationship requires the use of an 
auxiliary table called an *association table*. Here is how the database 
would look for the students and teachers example:

```
students                                          teachers
--------                                          --------
id  ---------                               ----- id
name        |                               |     name
            |                               |
            |        student_teacher        |
            |        ---------------        |
            -------- student_id             |
                     teacher_id -------------
```

While it may not seem obvious at first, the association table with its 
two foreign keys is able to efficiently answer all the queries about the 
relationship.

**Many-to-One and One-to-One**

A many-to-one is similar to a one-to-many relationship. The difference 
is that this relationship is looked at from the "many" side.

A one-to-one relationship is a special case of a one-to-many. The 
representation is similar, but a constraint is added to the database to 
prevent the "many" side to have more than one link. While there are 
cases in which this type of relationship is useful, it isn't as common 
as the other types.

### Representing Followers

Looking at the summary of all the relationship types, it is easy to 
determine that the proper data model to track followers is the 
many-to-many relationship, because a user follows *many* users, and a 
user has *many* followers. But there is a twist. In the students and 
teachers example I had two entities that were related through the 
many-to-many relationship. But in the case of followers, I have users 
following other users, so there is just users. So what is the second 
entity of the many-to-many relationship?

The second entity of the relationship is also the users. A relationship 
in which instances of a class are linked to other instances of the same 
class is called a *self-referential relationship*, and that is exactly 
what I have here.

Here is a diagram of the self-referential many-to-many relationship that 
keeps track of followers:

```
users                                        followers
-----                                        ---------
id                 INTEGER     ------------- follower_id        INTEGER
username           VARCHAR(64)       |------ folowed_id         INTEGER
email              VARCHAR(120)
password_hash      VARCHAR(128)
```

The `followers` table is the association table of the relationship. The 
foreign keys in this table are both pointing at entries in the user 
table, since it is linking users to users. Each record in this table 
represents one link between a follower user and a followed user. Like 
the students and teachers example, a setup like this one allows the 
database to answer all the questions about followed and follower users 
that I will ever need. Pretty neat.
