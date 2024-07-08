import uuid
from rest_framework import serializers
from .models import User, Organization
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            userId=str(uuid.uuid4()),
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
        )
        user.password = make_password(validated_data['password'])
        user.save()
        return user

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['orgId', 'name', 'description']
        

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'password', 'phone']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            phone=validated_data.get('phone', ''),
            password=make_password(validated_data['password']),
            userId=str(uuid.uuid4()),
        )
        org_name = f"{user.firstName}'s Organisation"
        Organization.objects.create(
            orgId=str(uuid.uuid4()),
            name=org_name,
            description='',
        )
        return user
    
    
class AddUserToOrganizationSerializer(serializers.Serializer):
    userId = serializers.CharField()

    def validate_user_id(self, value):
        if not User.objects.filter(userId=value).exists():
            raise serializers.ValidationError("User with this ID does not exist")
        return value