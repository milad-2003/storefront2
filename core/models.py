from django.contrib.auth.models import AbstractUser
from django.db import models


# Always create this class in the beginning of a project
# Even if there is no need for that, use the 'pass' keyword in the body of the class
# Otherwise you can't migrate it later and get the following error:
# Migration admin.0001_initial is applied before its dependency core.0001_initial on database 'default'.
# There is no solution for this and you have to drop the database and create it again
class User(AbstractUser):
    email = models.EmailField(unique=True)
