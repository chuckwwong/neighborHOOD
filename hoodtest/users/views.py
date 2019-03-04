# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Users, Crime
# Create your views here.
def index(request):
    user_list = list(Users.objects.all())
    usage = ""
    for u in user_list:
        usage += "UserID: {}\t name: {}\t email: {}<br/>".format(u.userID,u.name,u.email)
    html = "<p> {} <p/>".format(usage)
    return HttpResponse(html)
