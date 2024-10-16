from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import AsesorComercial, ConstructoraInmobiliaria
from .serializers import ( AsesorComercialSerializer, ConstructoraInmobiliariaSerializer, LoginSerializer )

class AsesorComercialViewSet(viewsets.ModelViewSet):
    queryset = AsesorComercial.objects.all()
    serializer_class = AsesorComercialSerializer
    permission_classes = [AllowAny]

class ConstructoraInmobiliariaViewSet(viewsets.ModelViewSet):
    queryset = ConstructoraInmobiliaria.objects.all()
    serializer_class = ConstructoraInmobiliariaSerializer
    permission_classes = [AllowAny]

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
