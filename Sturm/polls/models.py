from django.db import models
from django.utils import timezone


class History(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    idStudent = models.IntegerField(db_column='idStudent', blank=True, default=0)
    P0 = models.TextField(db_column='P0', blank=True, default='0')
    P1 = models.TextField(db_column='P1', blank=True, default='0')
    G = models.TextField(db_column='G', blank=True, default='0')
    arr = models.TextField(db_column='arr', blank=True, default='0')
    theory = models.TextField(db_column='theory', blank=True, default='0')
    firstPoint = models.TextField(db_column='firstPoint', blank=True, default='0')
    secondPoint = models.TextField(db_column='secondPoint', blank=True, default='0')
    edges = models.TextField(db_column='edges', blank=True, default='0')
    numOfZeros = models.TextField(db_column='numOfZeros', blank=True, default='0')
    add1 = models.TextField(db_column='add1', blank=True, default='0')
    add2 = models.TextField(db_column='add2', blank=True, default='0')
    P0_original = models.TextField(db_column='P0_original', blank=True, default='0')
    lower = models.FloatField(db_column='lower', blank=True, default=0)
    upper = models.FloatField(db_column='upper', blank=True, default=0)

    def __str__(self):
        return f"P(x) = {self.P0}"

class Scores(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    idStudent = models.IntegerField(db_column='idStudent', blank=True, default=0)
    points = models.IntegerField(db_column='points', blank=True, default=0)
    index = models.IntegerField(db_column='index', blank=True, default=0)
    time = models.DateTimeField(db_column='time', blank=False, default=timezone.now)

    def __str__(self):
        return f"{self.idStudent}: {self.points} points"

class Questions(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    idStudent = models.IntegerField(db_column='idStudent', blank=True, default=0)
    idQuestion = models.IntegerField(db_column='idQuestion', blank=True, default=0)
    time = models.DateTimeField(db_column='time', blank=False, default=timezone.now)

    def __str__(self):
        return f"{self.idStudent}: {self.idQuestion}"

class UnansweredQuestions(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    idStudent = models.IntegerField(db_column='idStudent', blank=True, default=0)
    idQuestion = models.IntegerField(db_column='idQuestion', blank=True, default=0)
    time = models.DateTimeField(db_column='time', blank=False, default=timezone.now)

    def __str__(self):
        return f"{self.idStudent}: {self.idQuestion}"

class Searched(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    idStudent = models.IntegerField(db_column='idStudent', blank=True, default=0)
    idHistory = models.IntegerField(db_column='idHistory', blank=True, default=0)

    def __str__(self):
        return f"{self.idStudent}: {self.idHistory}"
