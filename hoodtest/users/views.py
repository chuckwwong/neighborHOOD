import json
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.contrib.auth import logout, login, authenticate

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework import status

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from users.models import *
from users.serializers import *

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
        # In order to serialize objects, we must set 'safe=False'

''' USER INFO MODIFICATION '''

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def get_user_info(request):
    user = request._request.user
    if request.method == 'GET':
        user_info = UserSerializer(user)
        return JsonResponse(user_info.data, safe=False)
    elif request.method == 'POST':
        pword = request.data.get('password')
        if pword:
            user.password = pword
        p_num = request.data.get('phone_num')
        if p_num:
            user.phone_num = p_num
        f_name = request.data.get('first_name')
        if f_name:
            user.first_name = f_name
        l_name = request.data.get('last_name')
        if l_name:
            user.last_name = l_name
        user.save()
        user_info = UserSerializer(user)
        return JsonResponse(user_info.data,status=status.HTTP_200_OK,safe=False)

@api_view(['POST'])
@parser_classes((JSONParser,))
def register(request):
    uname = request.data.get('email')
    pword = request.data.get('password')
    p_num = request.data.get('phone_num')
    f_name = request.data.get('first_name')
    l_name = request.data.get('last_name')
    # cannot register a polic through website, must go through admin portal
    if not uname or not pword or not p_num or not f_name or not l_name:
	# if we don't have all fields required in try, fail
        resp = {}
        resp["details"] = "missing field values"
	json_resp = json.dumps(resp)
        return Response(status=status.HTTP_400_BAD_REQUEST,data=json_resp)
    
    try:
        u = Users(email=uname,password=pword,phone_num=p_num,first_name=f_name,last_name=l_name)
        u.set_password(pword)
        u.save()
        return Response(status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response(status=status.HTTP_409_CONFLICT)

@api_view(['POST'])
@parser_classes((JSONParser,))
def crime_login(request):
    uname = request.data.get('email')
    pword = request.data.get('password')
    user = authenticate(email=uname,password=pword)
    if user:
        login(request._request,user)
        print user.first_name,"logged in"
    else:
        return Response({"token": ""}, status=status.HTTP_403_FORBIDDEN)
    # generate token
    token, _ = Token.objects.get_or_create(user=user)
    r = Response()
    r.set_cookie(key="token",value=token.key)
    return r

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crime_logout(request):
    print "logging out ", request._request.user.email
    logout(request._request)
    request.user.auth_token.delete()
    r = Response()
    r.delete_cookie('token')
    r.status_code = status.HTTP_200_OK
    return r
