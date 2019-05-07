import json
import math
import operator
from django.db import connection
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

# weighted out of 5
c_wts = {
        'ARSON': 3, 'ASSAULT': 5, 'BATTERY': 5, 'BURGLARY': 5,
        'CONCEALED CARRY LICENSE VIOLATION': 1, 'CRIMINAL ABORTION': 1,
        'CRIMINAL DAMAGE': 1, 'CRIMINAL TRESPASS': 1, 'CRIM SEXUAL ASSAULT': 4, 
        'DECEPTIVE PRACTICE': 2, 'GAMBLING': 2, 'HOMICIDE': 4, 'HUMAN TRAFFICKING': 2,
        'INTERFERENCE WITH PUBLIC OFFICER': 2, 'INTIMIDATION': 3, 'KIDNAPPING': 4,
        'LIQUOR LAW VIOLATION': 2, 'MOTOR VEHICLE THEFT': 3, 'NARCOTICS': 1,
        'NON-CRIMINAL': 1, 'OBSCENITY': 1, 'OFFENSE INVOLVING CHILDREN': 4,
        'OTHER NARCOTIC VIOLATION': 1, 'OTHER OFFENSE': 2, 'PROSTITUTION': 1,
        'PUBLIC INDECENCY': 1, 'PUBLIC PEACE VIOLATION': 2, 'RITUALISM': 1, 'ROBBERY': 5,
        'SEX OFFENSE': 4, 'STALKING': 3, 'THEFT': 5, 'WEAPONS VIOLATION': 3 
        }

@api_view(['GET'])
@parser_classes((JSONParser,))
def crime_list(request):
    if request.method == 'GET':
        crimes = CrimeVerified.objects.all()
        ver_crimes_serializer = CrimeVerifiedSerializer(crimes, many=True)
        # returns json as a list :(
        return JsonResponse(ver_crimes_serializer.data, safe=False)

@csrf_exempt
@api_view(['GET','PUT','POST','DELETE'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,))
def crime_detail(request):
    user = request._request.user
    cn_id = request.data.get('case_number')

    if request.method == 'GET': 
        ver_crime = CrimeVerified.objects.filter(case_number=cn_id)
        if not ver_crime:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        ver_crime_serializer = CrimeVerifiedSerializer(ver_crime, many=True) 
        return JsonResponse(ver_crime_serializer.data, status=status.HTTP_200_OK, safe=False) 
    
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

    loc = request.data.get('location')
    loc_d = request.data.get('location_desc')
    ca = request.data.get('community_area')
    date = request.data.get('date')
    type_c = request.data.get('type_crime')
    dome = request.data.get('domestic')
    lat = request.data.get('latitude')
    lon = request.data.get('longitude')
    verr = request.data.get('verify')
    arr = request.data.get('arrested')

    if request.method == 'PUT':
        try:     
            crime = Crime.objects.get(case_number=cn_id)
        except Crime.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if loc:
            crime.location = loc
        if loc_d:
            crime.location_desc = loc_d
        if ca:
            crime.community_area = ca
        if date:
            crime.date = date
        if type_c:
            crime.type_crime = type_c
        if dome:
            crime.domestic = dome
        if lat:
            crime.latitude = lat
        if lon:
            crime.longitude = lon
        crime.save()
        if user.isPolice():
            exist = True
            try:
                verified = Verify.objects.get(case_number=cn_id)
            except Verify.DoesNotExist:
                exist = False
            if not exist:
                if verr:
                    verified = Verify(case_number=crime,email=user,arrested=arr)
                    verified.save()
            else:
                if not verr and verr != None:
                    verified.delete()
                else:
                    if arr != None:
                        verified.arrested = arr
                        verified.save()
        verif = [v.case_number for v in Verify.objects.filter(case_number=cn_id)]
        arrest = [v.case_number for v in Verify.objects.filter(case_number=cn_id,arrested=True)]
        context = {"verified_email_list": verif, "arrested_email_list": arrest }
        crime_info = crimeSerializer(crime, context=context) 
        #if crime_serializer.is_valid():
        return JsonResponse(crime_info.data,status=status.HTTP_200_OK) 
        #return JsonResponse(crime_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'POST':
        if not loc or not loc_d or not ca or not date or not type_c or not lat or not lon:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user.isPolice:
            if Crime.objects.filter(case_number=cn_id):
                return Response(status=status.HTTP_409_CONFLICT)
            crime = Crime(case_number=cn_id,location=loc,location_desc=loc_d,community_area=ca,date=date,type_crime=type_c,domestic=dome,email=user,latitude=lat,longitude=lon)
        else:
            crime = Crime(location=loc,location_desc=loc_d,community_area=ca,date=date,type_crime=type_c,domestic=dome,email=user,latitude=lat,longitude=lon)
        crime.save()
        if user.isPolice():
            if arr is None:
                arr = False
            verify = Verify(case_number=crime,email=user,arrested=arr)
            verify.save()
            ver_crime = CrimeVerified.objects.filter(case_number=crime.case_number)
            ver_crime_info = CrimeVerifiedSerializer(ver_crime,many=True)
            return JsonResponse(ver_crime_info.data,status=status.HTTP_201_CREATED,safe=False)
        crime_serializer =crimeSerializer(crime)
        return JsonResponse(crime_serializer.data, status=status.HTTP_201_CREATED) 
        #crime_serializer = crimeSerializer(data=crime_data)
        #if crime_serializer.is_valid():
        #     crime_serializer.save()
	#     return JsonResponse(crime_serializer.data, status=status.HTTP_201_CREATED)
	#return JsonResponse(cr,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@parser_classes((JSONParser,)) 
def crime_list_ca(request, ca):
    ver_crimes = CrimeVerified.objects.filter(community_area = ca) 
    ver_crime_serializer = CrimeVerifiedSerializer(ver_crimes, many=True)
    return JsonResponse(ver_crime_serializer.data,status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,))
def crime_search(request):
    # start here
    cn_id = request.data.get('case_number')
    if cn_id == None:
        # return all unverified crimes
        v_crimes = Verify.objects.all()
        crimes = Crime.objects.all()
        v_crimes = [v.case_number for v in v_crimes]
        unverified = []
        for c in crimes:
            if c not in v_crimes:
                unverified.append(c)
        crime_info = crimeSerializer(unverified, many=True)
        return JsonResponse(crime_info.data,status=status.HTTP_200_OK,safe=False)
    else:
        crime = Crime.objects.filter(case_number = cn_id)
        verif = [v.case_number for v in Verify.objects.filter(case_number=cn_id)]
        arrest = [v.case_number for v in Verify.objects.filter(case_number=cn_id,arrested=True)]
        context = {"verified_email_list": verif, "arrested_email_list": arrest }
        crime_info = crimeSerializer(crime, context=context,many=True)
        return JsonResponse(crime_info.data,status=status.HTTP_200_OK,safe=False)


''' ADVANCED FUNCTIONS'''
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_safety_all(request):
    ca_crimes = {}
    for i in range(78):
	collect_ca = []
        collect_ca += [c for c in CrimeVerified.objects.filter(community_area = i)]
        ca_crimes[i] = collect_ca
    weights = get_crime_weight_ca(ca_crimes)
    # make into json and return
    return JsonResponse(data=weights,status=status.HTTP_200_OK,safe=False)

''' HELPER FUNCTION'''
def get_crime_weight_ca(crimes_list):
    crime_weight = {}
    for ca, clist in crimes_list.items():
        if clist:
            # print ca, clist
            count = len(clist)
            max_poss = count * 5
            weight = 0
            for c in clist:
                weight += c_wts[c.type_crime]
            crime_weight[ca] = weight/float(max_poss)
        else:
            crime_weight[ca] = 0
    max_val = max(crime_weight.iteritems(), key=operator.itemgetter(1))[1]
    for ca, w in crime_weight.items():
        crime_weight[ca] = float("{0:.1f}".format(math.ceil(float(w)*10/max_val)/10.0))
    return crime_weight

def get_crime_weight(crimes_list):
    if crimes_list:
        count = len(crimes_list)
        max_poss = count*5
        weight = 0
        for c in crimes_list:
            weight += c_wts[c.type_crime]
        return float("{0:.1f}".format(math.ceil(float(weight)*10/max_val)/10.0))
    return 0

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
    crimes = CrimeVerified.objects.all()
    radius = []
    for c in crimes:
        if c.distance(lat,lon) <= 5:
            radius.append(c)
    max_weight = get_crime_weight(radius)
    
    return Response(status=status.HTTP_200_OK) #,safe=False)


''' USER INFO MODIFICATION '''
@csrf_exempt
@api_view(['GET','PUT'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated,))
def get_user_info(request):
    user = request._request.user
    if request.method == 'GET':
        user_info = UserSerializer(user)
        return JsonResponse(user_info.data, safe=False)
    elif request.method == 'PUT':
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
    arrest = []
    for c in reported:
        verified += [v.case_number for v in Verify.objects.filter(case_number=c.case_number)]
        arrest += [v.case_number for v in Verify.objects.filter(case_number=c.case_number,arrested=True)]
    context = {"verified_email_list": verified, "arrested_email_list": arrest}
    serializer = crimeSerializer(reported,context=context, many=True)
    # Returns json response as a list :( 
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
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
