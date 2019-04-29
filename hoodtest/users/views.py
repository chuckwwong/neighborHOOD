from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, login, authenticate

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import *
from users.serializers import crimeSerializer

@csrf_exempt
def crime_list(request):

    if request.method == 'GET':
        crimes = Crime.objects.all()
        crimes_serializer = crimeSerializer(crimes, many=True)
        return JsonResponse(crimes_serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False'

    if request.method == 'POST':
        crime_data = JSONParser().parse(request)
        crime_serializer = crimeSerializer(data=crime_data)
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
        crime_serializer = crimeSerializer(crime) 
        return JsonResponse(crime_serializer.data) 

    elif request.method == 'PUT': 
        crime_data = JSONParser().parse(request) 
        crime_serializer = crimeSerializer(crime, data=crime_data) 
        if crime_serializer.is_valid(): 
            crime_serializer.save() 
            return JsonResponse(crime_serializer.data) 
        return JsonResponse(crime_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE':
        crime.delete() 
        return HttpResponse(status=status.HTTP_204_NO_CONTENT) 


@csrf_exempt
def crime_list_ca(request, ca):
    crimes = Crime.objects.filter(community_area = ca)

    if request.method == 'GET': 
        crimes_serializer = crimeSerializer(crimes, many=True)
        return JsonResponse(crimes_serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False'i
