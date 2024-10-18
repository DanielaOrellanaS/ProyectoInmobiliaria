from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AsesorComercial, ConstructoraInmobiliaria

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'identification', 'password')

class AsesorComercialSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = AsesorComercial
        fields = ('user', 'foto', 'biografia', 'skills', 'reseñas', 'numero_ventas')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  # Extrae la contraseña
        user = User.objects.create_user(**user_data)
        user.set_password(password)  # Establece la contraseña
        user.is_asesor = True  # Marca al usuario como asesor
        user.save()
        asesor = AsesorComercial.objects.create(user=user, **validated_data)
        return asesor


class ConstructoraInmobiliariaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = ConstructoraInmobiliaria
        fields = ('user', 'nombre', 'tiempo_constitucion', 'representante_legal', 'direccion')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')  # Extrae la contraseña
        user = User.objects.create_user(**user_data)
        user.set_password(password)  # Establece la contraseña
        user.is_constructora = True  # Marca al usuario como constructora
        user.save()
        constructora = ConstructoraInmobiliaria.objects.create(user=user, **validated_data)
        return constructora

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
