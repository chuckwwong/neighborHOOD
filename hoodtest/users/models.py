# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
#from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import CustomUserManager

# Create your models here.
class Users(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True)
    phone_num = models.CharField(max_length=10)
    # only admin can set pol_district for police accounts
    pol_district = models.IntegerField(default=None,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_num','first_name','last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email+": "+self.first_name+" "+self.last_name
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
    domestic = models.BooleanField(default=False)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.case_number)+": "+self.type_crime

class Verify(models.Model):
    case_number = models.OneToOneField(Crime, on_delete=models.CASCADE,primary_key=True)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    arrested = models.BooleanField(default=False)
    def __str__(self):
        return unicode(self.case_number)+"<- "+unicode(self.email)
