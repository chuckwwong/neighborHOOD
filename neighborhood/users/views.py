# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from users.models import Crime
from users.serializers import CrimeSerializer
 
@csrf_exempt
def user_list(request):
    if request.method == 'POST':
        crime_data = JSONParser().parse(request)
        crime_serializer = CrimeSerializer(data=crime_data)
        if crime_serializer.is_valid():
            crime_serializer.save()
            return JsonResponse(crime_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(crime_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        Crime.objects.all().delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
 
 
@csrf_exempt 
def crime_detail(request, pk):
    try: 
        crime = Crime.objects.get(pk=pk) 
    except Crime.DoesNotExist: 
        return HttpResponse(status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        crime_serializer = CrimeSerializer(crime) 
        return JsonResponse(crime_serializer.data) 
 
    elif request.method == 'PUT': 
        crime_data = JSONParser().parse(request) 
        crime_serializer = CrimeSerializer(crime, data=crime_data) 
        if crime_serializer.is_valid(): 
            crime_serializer.save() 
            return JsonResponse(crime_serializer.data) 
        return JsonResponse(crime_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        crime.delete() 
        return HttpResponse(status=status.HTTP_204_NO_CONTENT) 
@csrf_exempt
def crime_list_location(request, location):
    crimes = Crime.objects.filter(location=location)
        
    if request.method == 'GET': 
        crimes_serializer = CrimeSerializer(crimes, many=True)
        return JsonResponse(crimes_serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False'i
