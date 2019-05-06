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
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import *
from users.serializers import *


@api_view(['GET'])
@parser_classes((JSONParser,))
def crime_list(request):
    if request.method == 'GET':
        crimes = CrimeVerified.objects.all()
        ver_crimes_serializer = CrimeVerifiedSerializer(crimes, many=True)
        # returns json as a list :(
        return JsonResponse(ver_crimes_serializer.data, safe=False)


@api_view(['GET','PUT','POST','DELETE'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,))
def crime_detail(request):
    user = request._request.user
    cn_id = request.data.get('case_number')

    if request.method == 'GET': 
        try:
            ver_crime = CrimeVerified.objects.filter(case_number=cn_id)
        except CrimeVerified.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        ver_crime_serializer = CrimeVerifiedSerializer(ver_crime, many=True) 
        return JsonResponse(ver_crime_serializer.data, status=status.HTTP_200_OK) 

    # TODO: modify report: allow police to modify arrest, verify
    elif request.method == 'PUT': 
        crime_data = JSONParser().parse(request)
        print crime_data 
        #crime_serializer = crimeSerializer(crime, data=crime_data) 
        #if crime_serializer.is_valid(): 
        #    crime_serializer.save() 
        #    return JsonResponse(crime_serializer.data) 
        #return JsonResponse(crime_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        pass

    # TODO: add a crime: if police modify
    elif request.method == 'POST':
        #crime_data = request._request
        #crime_serializer = crimeSerializer(data=crime_data)
        #if crime_serializer.is_valid():
        #     crime_serializer.save()
	#     return JsonResponse(crime_serializer.data, status=status.HTTP_201_CREATED)
	#return JsonResponse(cr,status=status.HTTP_400_BAD_REQUEST)
        pass

    elif request.method == 'DELETE':
        if user.isPolice():
            crime = Crime.objects.filter(case_number=cn_id)
        else:
            crime = Crime.objects.filter(case_number=cn_id,email=user.email)
        if crime:
            crime.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,)) 
def crime_list_ca(request, ca):
    ver_crimes = CrimeVerified.objects.filter(community_area = ca) 
    ver_crime_serializer = CrimeVerifiedSerializer(ver_crimes, many=True)
    return JsonResponse(ver_crime_serializer.data,status=status.HTTP_200_OK)


# TODO: return list of user reported crimes that includes verified attribute
# TODO: search by crime for police by case_number, and can edit and delete
# 	list all unverified <- can edit and delete

@api_view(['GET'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,))
def crime_search(request):
    # start here
    pass


''' ADVANCED FUNCTIONS'''
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_safety_all(request):
    '''
    Chuck will do this
    use the
    '''
    pass
''' HELPER FUNCTION'''
# def 

@api_view(['GET'])
def get_safety_info(request):
    '''
    given latitude and longitude, collect all crimes in a radius and
    predict safety value of that location, top 3 crimes that are most
    likely to occur to you, and the corresponding location where it happens
    
    For Safety Index, weight it based on per crime, where crimes that directly affect you
    like assult, burglary, or kidnapping have higher weights and things like "Human Trafficking"
    that are dangerous, but like won' really directly affect you, or "Public Indecency" which is bad
    but isn't like dangerous should have a lower weight.
    TODO: Make sure to weight them properly, we have to explain this as an advanced function.
 
    ONE idea to calculate the weight is once you collect all the crimes in an area, you multiply each 
    crime by their corresponding weight then add them up. Then you could divide them by the total number
    of crimes in that same area, but with the highest weight.
    ex: if for a lat and long, there are 20 crimes near by, the safey index would be (total calculated sum)/20*5, if 5 
    is the highest weight possible
    if you have a better idea to get a weight, do that instead
    TODO: ^ Make this a helper funciton so I can call it too in the other advanced feature

    For most common crime, pick top 3, use aggregate function or something, that have occurred in that area.
    For each crime from the top 3, pick the location that it is most likely to occur to you, so you only look at 
    locations where this crime happened. The location we are talking about is "location_desc"
    '''
    # this pulls the latitude and longitude from front end request
    lat = request.data.get('latitude')
    lon = request.data.get('longitude')
    
    # TODO : return a json that lists
    # {
    #   "safe_idx":<some meaningful number>
    #   "top_common_crime":[
    #     list top 3 that can affect user
    #     return it as tuple: (crime, location)
    #                                  ^ location where that crime is most likely to happen to you
    #   ]
    # }
    pass


''' USER INFO MODIFICATION '''

@api_view(['GET','POST'])
@parser_classes((JSONParser,))
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
        return JsonResponse(user_info.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,))
def get_user_reported(request):
    user = request._request.user
    uname = user.email
    reported = Crime.objects.filter(email=uname)
    verified = []
    for c in reported:
        verified += [v for v in CrimeVerified.objects.filter(case_number=c.case_number)]
    context = {"verified_email_list": verified }
    serializer = crimeSerializer(reported,context=context, many=True)
    # Returns json response as a list :( 
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


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
@permission_classes((AllowAny,))
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
    r.status_code = status.HTTP_200_OK
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
