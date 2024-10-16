from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AsesorComercial, ConstructoraInmobiliaria

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'identification', 'is_asesor', 'is_constructora')

class AsesorComercialSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = AsesorComercial
        fields = ('user', 'foto', 'biografia', 'skills', 'reseñas', 'numero_ventas')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_asesor=True)
        asesor = AsesorComercial.objects.create(user=user, **validated_data)
        return asesor

class ConstructoraInmobiliariaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = ConstructoraInmobiliaria
        fields = ('user', 'nombre', 'tiempo_constitucion', 'representante_legal', 'direccion')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_constructora=True)
        constructora = ConstructoraInmobiliaria.objects.create(user=user, **validated_data)
        return constructora

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
