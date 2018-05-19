from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserManager(models.Manager):

    def validate(self, post):

        errors = {}

        fname = post['first_name']
        if not fname.isalpha():
            errors['fname_alpha'] = 'First name must be only alphabetical characters'
        if not len(fname) >= 2:
            errors['fname_len'] = 'First name must be 2 or more characters'

        lname = post['last_name']
        if not lname.isalpha():
            errors['lname_alpha'] = 'Last name must be only alphabetical characters'
        if not len(lname) >= 2:
            errors['lname_len'] = 'Last name must be 2 or more characters'

        password = post['password']
        if not password == post['confirm_password']:
            errors['pw_mismatch'] = 'Passwords must match'
        if not len(password) >= 8:
            errors['pw_len'] = 'Password must be 8 or more characters'

        try:
            validate_email(post['email'])
        except ValidationError:
            errors['email_format'] = 'Email must be a valid address'
        else:
            if not errors:
                if User.objects.filter(email = post['email']):
                    errors['email_unique'] = 'User already exists'


        return errors

class User(models.Model):
    ADMIN = 9
    NORMAL = 1
    LEVEL = (
        (ADMIN, 'Admin'),
        (NORMAL, 'Normal')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    level = models.IntegerField(choices=LEVEL, default=NORMAL)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Post(models.Model):
    entry = models.TextField()
    user = models.ForeignKey(User, related_name='posts')
    comment = models.ForeignKey('self', related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
