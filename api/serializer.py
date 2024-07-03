from rest_framework import serializers
from .models import Person

personDefaultFields = ["id","full_name", "email", "age", "password"]
class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = personDefaultFields
        
    