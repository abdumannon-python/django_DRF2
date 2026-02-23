from .models import Users
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=( 'first_name', 'last_name','email' )

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    conf_password=serializers.CharField(write_only=True,required=True)
    class Meta:
        model=Users
        fields=('username', 'password','conf_password', 'email', 'first_name', 'last_name')


    def validate_username(self,username):
        if len(username)<6:
            raise ValidationError({'message':'Username kamida 7 belgidan iborat bolishi kerek'})
        elif not username.isalnum():
            raise ValidationError({'message':'username da ortiqcha belgi bolmasligi kerak '})
        elif username[0].isdigit():
            raise ValidationError({'message':'username raqam bilan boshlanmasin '})
        return username
    def create(self,validated_data):
        validated_data.pop('conf_password')
        user=Users.objects.create_user(**validated_data)
        return user


