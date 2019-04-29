from rest_framework import serializers 
from users.models import Crime
 
 
class crimeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Crime
        fields = ('case_number',
                  'location',
                  'community_area',
                  'date',
                  'type_crime',
                  'email')
