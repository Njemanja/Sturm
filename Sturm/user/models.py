from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class Student(AbstractUser):
    id = models.AutoField(db_column='id', primary_key=True)
    username = models.CharField(db_column='username', unique=True, max_length=20, blank=True, default='0')
    name = models.CharField(db_column='name', max_length=40, blank=True, default='0')
    surname = models.CharField(db_column='surname', max_length=40, blank=True, default='0')
    email = models.CharField(db_column='email', max_length=50, blank=True, default='0')
    password = models.TextField(db_column='password', blank=True, default='0')
    status = models.CharField(db_column='status', max_length=20, blank=True, default='0')
    reason = models.CharField(db_column='reason', max_length=20, blank=True, default='0')
    institution = models.CharField(db_column='institution', max_length=200, blank=True, default='0')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_user_set_permissions',
        blank=True
    )
    pass

    def __str__(self):
        return f"{self.username}_{self.email}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token
