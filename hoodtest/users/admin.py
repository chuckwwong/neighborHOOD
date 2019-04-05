# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Users, Crime, Verify

# Register your models here.
admin.site.register(Users)
admin.site.register(Crime)
admin.site.register(Verify)
