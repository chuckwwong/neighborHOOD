# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Users, Crime, Verify

class UsersAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Users
    list_display = ('email', 'is_staff', 'is_active','is_superuser',)
    list_filter = ('email', 'is_staff', 'is_active','is_superuser',)
    fieldsets = (
        (None, {'fields': ('email','password',('first_name','last_name'),'phone_num','pol_district')}),
        ('Permissions', {'fields': ('is_staff','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',('first_name','last_name'), 'phone_num', 'pol_district', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register your models here.
admin.site.register(Users,UsersAdmin)
admin.site.register(Crime)
admin.site.register(Verify)
