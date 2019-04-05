# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    case_number = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=100)
    community_area = models.IntegerField(validators=[MinValueValidator(0),
                                                     MaxValueValidator(77)],default = 0)
    date = models.DateTimeField('date crime committed')
    type_crime = models.CharField(max_length=40)
    # arrested and verified are only able to be set by police
    arrested = models.BooleanField(default=False)
    # this attribute is not needed, as we have a verify table to check all the verified crimes
    #verified = models.BooleanField(default=False)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.case_number)+": "+self.type_crime

class Verify(models.Model):
    case_number = models.OneToOneField(Crime, on_delete=models.CASCADE,primary_key=True)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.case_number)+"<- "+self.email
