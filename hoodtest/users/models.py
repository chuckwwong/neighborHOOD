# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    userID = models.CharField(primary_key=True,max_length=10)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=10)

    def __str__(self):
        return self.userID
class Crime(models.Model):
    case_number = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=100)
    date = models.DateTimeField('date published')
    type_crime = models.CharField(max_length=10)
    arrested = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.case_number)+": "+self.type_crime
