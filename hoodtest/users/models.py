# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Users(models.Model):
    email = models.EmailField(primary_key=True,max_length=50)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=10)
    # only admin can set pol_district for police accounts
    pol_district = models.IntegerField(default=None,null=True)

    def __str__(self):
        return self.email+": "+self.name
    def isPolice(self):
        if self.pol_district:
            return True
        else:
            return False

class Crime(models.Model):
    case_number = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    community_area = models.IntegerField(null=True,default = None)
    date = models.CharField(max_length=50)
    type_crime = models.CharField(max_length=40)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.case_number)+": "+self.type_crime

class Verify(models.Model):
    case_number = models.OneToOneField(Crime, on_delete=models.CASCADE,primary_key=True)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    arrested = models.BooleanField(default=False)
    def __str__(self):
        return unicode(self.case_number)+"<- "+unicode(self.email)
