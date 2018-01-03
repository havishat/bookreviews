
# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
EMAILisnotvalid = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
passd = re.compile(r'^([^0-9]*|[^A-Z]*)$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class LoginManager(models.Manager):

    def validate_login(self, postData):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=postData['email'])) > 0:
            # check this user's password
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("Name should be more than 5 characters")
        if len(postData['alias'])< 2 :
            errors.append('alias must be at least two characters')
        if len(postData['password']) < 8 :
            errors.append("Password should be more than 8 characters")
        if passd.match(postData['password']):
            errors.append("least 1 uppercase letter and 1 numeric value")
        if postData['password'] != postData['password_confirm']:
            errors.append("Password and Password Confirmation are not same")
        if not errors:
        # make our new user
        # hash password
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                password=hashed
            )
            return new_user
        return errors


class ReviewManager(models.Manager):
    def recent_and_not(self):
        '''
        returns a tuple with the zeroeth index containing query for 3 most recent reviews, and the first index
        containing the rest
        '''
        return (self.all().order_by('-created_at')[:3], self.all().order_by('-created_at')[3:])

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = LoginManager()
    def __str__(self):
        return self.email

class Author(models.Model):
    author_name =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.author_name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.title

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name="reviews")
    reviewer = models.ForeignKey(User, related_name="reviews_user")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()
    def __str__(self):
        return "Book: {}".format(self.book.title)


