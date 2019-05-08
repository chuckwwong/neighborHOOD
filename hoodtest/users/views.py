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
from rest_framework.permissions import IsAuthenticated

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
# center lat,lon values to set for new crimes
lat_long_dict = {
35: (41.8362095409,-87.6161477255), 36: (41.8222678696,-87.60026285), 37: (41.809542358,-87.6322509736), 38: (41.8123507322,-87.6191134411), 39: (41.8090960441,-87.5901452313),
4: (41.9743040153,-87.694233228), 40: (41.7912001679,-87.617739511), 41: (41.7940778142,-87.584535138), 42: (41.7779565653,-87.584390255), 1: (42.0119378101,-87.6656766355),
11: (41.9846030555,-87.7716020235), 12: (41.9963743663,-87.765847574),13: (41.9810071429,-87.7185850035), 14: (41.9693656816,-87.7181810818), 15: (41.956644545,-87.7687172416),
16: (41.9543414926,-87.716140847), 17: (41.9471545872,-87.8107727056), 18: (41.9307256744,-87.7993214452), 19: (41.9276439091,-87.7665006335), 2: (41.999313932,-87.6971586831),
20: (41.9226829552,-87.7330904469), 21: (41.9387830284,-87.7049350756), 22: (41.9230275473,-87.6965752676), 23: (41.9013359069,-87.7177029808),24: (41.9010893293,-87.6726292762),
25: (41.8965015695,-87.7711925843), 26: (41.8763209431,-87.7308837893), 27: (41.8784793574,-87.7053283066), 28: (41.8773206336,-87.6627174304), 29: (41.862470109,-87.7163608445),
3: (41.9656187046,-87.6446803779), 30: (41.837963862,-87.7136795265), 31: (41.8503172061,-87.663987764), 33: (41.8589792384,-87.6123942907), 34: (41.8418876716,-87.6341650177),
10: (41.9839513994,-87.8042210551), 8: (41.8978269759,-87.6203973526), 32: (41.8815274719,-87.6187418312), 43: (41.76298428,-87.5592683512), 44: (41.7390824367,-87.6142443554),
45: (41.7442281813,-87.5876862868), 46: (41.744864913,-87.5401780956), 47: (41.7277481781,-87.5965367548), 59: (41.8288014238,-87.6741758312), 6: (41.9441278382,-87.6466579503),
48: (41.7292878193,-87.5711424151), 49: (41.7103965388,-87.6231500503),5: (41.9464543897,-87.6874851835), 50: (41.7048033335,-87.5983533597), 51: (41.6940951537,-87.5716512439),
52: (41.7112327793,-87.5292081428), 53: (41.6685244409,-87.6369977412), 54: (41.6613180265,-87.6068314456), 55: (41.661290525,-87.5504940021), 56: (41.8001049167,-87.767985992),
57: (41.8089779611,-87.7260409632), 58: (41.8182167076,-87.6972280732), 60: (41.8359446753,-87.6454612399), 61: (41.808242003,-87.660237206), 62: (41.7929943789,-87.7238712991),
63: (41.7952558491,-87.6977384723), 64: (41.7790737604,-87.7736150521), 65: (41.7708255816,-87.7248804631), 66: (41.77272718,-87.6999594399), 67: (41.77895668,-87.6636076797),
68: (41.7754365969,-87.6417517534), 69: (41.7651284246,-87.6168952468), 7: (41.9210517157,-87.6360355339), 70: (41.7447039349,-87.7079215645),
71: (41.7429692699,-87.6549689029), 72: (41.7126121358,-87.6797878358), 73: (41.7194893672,-87.6497323872), 74: (41.6959887711,-87.7131433552),
75: (41.6882212207,-87.6684404536), 76: (41.9762876744,-87.8794058447), 77: (41.9877902524,-87.6575486406), 9: (42.0086088728,-87.815907765),
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
def crime_detail(request,pk):
    user = request._request.user

    if request.method == 'GET': 
        ver_crime = CrimeVerified.objects.filter(pk=pk)
        if not ver_crime:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        ver_crime_serializer = CrimeVerifiedSerializer(ver_crime, many=True) 
        return JsonResponse(ver_crime_serializer.data, status=status.HTTP_200_OK, safe=False) 

    cn_id = int(request.data.get('case_number'))   

    if request.method == 'DELETE':
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
    ca = int(request.data.get('community_area'))
    date = request.data.get('date')
    type_c = request.data.get('type_crime')
    dome = request.data.get('domestic')
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
            lat, lon = lat_long_dict[ca]
            crime.latitude = lat
            crime.longitude = lon
        if date:
            crime.date = date
        if type_c:
            crime.type_crime = type_c
        if dome:
            crime.domestic = dome
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
        if not loc or not loc_d or not ca or not date or not type_c:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        lat, lon = lat_long_dict[ca]
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
    for i in range(1,78):
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
    #max_val = max(crime_weight.iteritems(), key=operator.itemgetter(1))[1]
    #max_val = float(max(crime_weight, key = lambda ca: crime_weight[ca]))
    max_val = max(crime_weight.values())
    for ca, w in crime_weight.items():
        crime_weight[ca] = float("{0:.1f}".format(math.floor(float(w)*10.0/max_val)/10.0))
    #crime_weight[78] = max_val
    return crime_weight

def get_crime_weight(crimes_list):
    if crimes_list:
        count = len(crimes_list)
        max_val = count*5
        weight = 0
        for c in crimes_list:
            weight += c_wts[c.type_crime]
        return float("{0:.2f}".format(float(weight)*100/max_val))
    return 0

# NOT ACTUALLY A POST METHOD, BUT I WANT TO PASS IN LAT AND LONG SO Ls
@csrf_exempt
@api_view(['POST'])
def get_safety_info(request):
    '''
    given latitude and longitude, collect all crimes in a radius and
    predict safety value of that location, top 3 crimes that are most
    likely to occur to you, and the corresponding location where it happens
    '''
    lat = float(request.data.get('latitude'))
    lon = float(request.data.get('longitude'))
    
    with connection.cursor() as cursor: 
        crimes = []
        metrics = {}
        for c in CrimeVerified.objects.raw("select * from crime_verified where latitude <= %s and latitude >= %s"
        + "and longitude <= %s and longitude >= %s",[str(lat+0.02), str(lat-0.02), str(lon+0.02), str(lon-0.02)]):
            crimes.append(c)
        max_weight = get_crime_weight(crimes)
        metrics["safe_idx"] = max_weight
        cursor.execute("SELECT type_crime, count(*) total FROM crime_verified WHERE latitude <= %s and latitude >= %s"
        + "and longitude <=%s and longitude >= %s GROUP BY type_crime ORDER BY total DESC LIMIT 3",[str(lat+0.02), str(lat-0.02), str(lon+0.02), str(lon-0.02)])
        possible = cursor.fetchall()
        index = 1
        for tup in possible:
            cursor.execute("SELECT location_desc, count(*) total FROM crime_verified WHERE latitude <= %s and latitude >= %s"
            + "and longitude <= %s and longitude >= %s and type_crime = %s GROUP BY location_desc ORDER BY total DESC LIMIT 1",
            [str(lat+0.02), str(lat-0.02), str(lon+0.02), str(lon-0.02),tup[0]])
            poss_location = cursor.fetchone()
            metrics["crime_type"+str(index)] = tup[0]
            metrics["location_desc"+str(index)] = poss_location[0]
            index += 1
    return JsonResponse(data=metrics,status=status.HTTP_200_OK,safe=False)


''' USER INFO MODIFICATION '''
@csrf_exempt
@api_view(['GET','PUT','DELETE'])
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
    elif request.method == 'DELETE':
        print "logging out ", request._request.user.email
        logout(request._request)
        request.user.auth_token.delete()
        user.delete()
        r = Response()
        r.delete_cookie('token')
        r.status = status.HTTP_204_NO_CONTENT
        return r


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
        user = Users.objects.filter(email=uname)
        if user:
            return Response(status=status.HTTP_409_CONFLICT)
        u = Users(email=uname,password=pword,phone_num=p_num,first_name=f_name,last_name=l_name)
        u.set_password(pword)
        u.save()
        return Response(status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response(status=status.HTTP_409_CONFLICT)

@csrf_exempt
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
    usage = {}
    usage["isPolice"] = user.isPolice()
    usage["Authorization"] = token.key
    r = Response()
    r.data = usage
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
