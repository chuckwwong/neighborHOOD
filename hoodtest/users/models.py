# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import *
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
#from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import CustomUserManager

# Create your models here.
class Users(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True,primary_key=True)
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
    location_desc = models.CharField(max_length=100)
    community_area = models.IntegerField(null=True,default = None)
    date = models.CharField(max_length=50)
    type_crime = models.CharField(max_length=40)
    domestic = models.BooleanField(default=False)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=11,decimal_places=8)
    longitude = models.DecimalField(max_digits=11,decimal_places=8)

    def __str__(self):
        return str(self.case_number)+": "+self.type_crime

class Verify(models.Model):
    case_number = models.OneToOneField(Crime, on_delete=models.CASCADE,primary_key=True)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    arrested = models.BooleanField(default=False)
    def __str__(self):
        return unicode(self.case_number)+"<- "+unicode(self.email)

class CrimeVerified(models.Model):
    case_number = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    location_desc = models.CharField(max_length=100)
    community_area = models.IntegerField(null=True,default=None)
    date = models.CharField(max_length=40)
    type_crime = models.CharField(max_length=40)
    domestic = models.BooleanField(default=False)
    reported_email = models.ForeignKey(Users,related_name='users_crime', on_delete=models.DO_NOTHING)
    latitude = models.DecimalField(max_digits=11,decimal_places=8)
    longitude = models.DecimalField(max_digits=11,decimal_places=8)
    ver_case_num = models.OneToOneField(Crime, on_delete=models.DO_NOTHING)
    verified_email = models.ForeignKey(Users,related_name='users_users', on_delete=models.DO_NOTHING)
    arrested = models.BooleanField(default=False)

    def distance(self, base_lat, base_lon):
        R = 6371000 # metres
        lat1 = radians(self.latitude)
        lat2 = radians(base_lat)
        lat_diff = radians(float(base_lat) - float(self.latitude))
        lon_diff = radians(float(base_lon) - float(self.longitude))
        a = sin(lat_diff/2)**2 + cos(lat1) * cos(lat2) * sin(lon_diff/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c
        d *= 0.621371 # convert to miles
        return d

    class Meta:
        managed = False
        db_table = 'crime_verified'
