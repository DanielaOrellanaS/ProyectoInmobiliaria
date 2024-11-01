from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CommercialAdvisor, BuilderCompany

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'identification', 'password')

class CommercialAdvisorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = CommercialAdvisor
        fields = ('user', 'photo', 'biography', 'skills', 'reviews', 'num_sales')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  
        user = User.objects.create_user(**user_data)
        user.set_password(password)  
        user.is_asesor = True  
        user.save()
        asesor = CommercialAdvisor.objects.create(user=user, **validated_data)
        return asesor

class BuilderCompanySerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = BuilderCompany
        fields = ('user', 'incorporation_time', 'legal_representative', 'address')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  
        user = User.objects.create_user(**user_data)
        user.set_password(password)  
        user.is_constructora = True  
        user.save()
        constructora = BuilderCompany.objects.create(user=user, **validated_data)
        return constructora

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
