from rest_framework import serializers 
from users.models import *
 
 
class crimeSerializer(serializers.ModelSerializer):
    verified = serializers.SerializerMethodField('is_verified')

    def is_verified(self, email):
        verified_emails = self.context.get("verified_email_list",[])
        if email in verified_emails:
            return True
        return False
 
    class Meta:
        model = Crime
        fields = ('case_number',
                  'location',
                  'location_desc',
                  'community_area',
                  'date',
                  'type_crime',
                  'domestic',
                  'email',
                  'latitude',
                  'longitude',
                  'verified')

# has full data of the crime, which includes data from verify
class CrimeVerifiedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CrimeVerified
        fields = ('case_number',
                  'location',
                  'location_desc',
                  'community_area',
                  'date',
                  'type_crime',
                  'domestic',
                  'reported_email',
                  'latitude',
                  'longitude',
                  'verified_email',
                  'arrested')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('email',
                  'first_name',
                  'last_name',
                  'phone_num',
                  'pol_district')
