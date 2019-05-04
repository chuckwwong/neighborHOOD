from rest_framework import serializers 
from users.models import *
 
 
class crimeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Crime
        fields = ('case_number',
                  'location',
                  'community_area',
                  'date',
                  'type_crime',
                  'email')

# class fullcrimeSerializer(serializers.ModelSerializer):

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('email',
                  'first_name',
                  'last_name',
                  'phone_num',
                  'pol_district')
