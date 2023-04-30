from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import datetime
# Create your models here.
class docvUser(models.Model):
     USER_TYPE_CHOICES = (
        ('', '-Select Role'),
      (1, 'Verification_Assistant'),
      (2, 'Dealing_Assistant'),
  )
     email = models.EmailField(max_length=254, unique=True)
     name = models.CharField(max_length=254, null=True, blank=False)
     password = models.CharField(max_length=254, null=True, blank=False)
     user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
     is_active = models.BooleanField(default=True)
     last_login = models.DateTimeField(null=True, blank=True)
     date_joined = models.DateTimeField(auto_now_add=True)

     def create_user( name, email,user_type, password=None):

      if name is None:
         raise TypeError('Users must have a name.')

      if email is None:
         raise TypeError('Users must have an email address.')

      user = docvUser.objects.create(
         email=email,
         name=name,
         user_type=user_type,
         password = make_password(password),
         date_joined = datetime.now())

      return user

     


     