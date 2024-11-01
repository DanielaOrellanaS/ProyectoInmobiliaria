from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import CommercialAdvisor, BuilderCompany
from .serializers import ( CommercialAdvisorSerializer, BuilderCompanySerializer, LoginSerializer )
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class CommercialAdvisorViewSet(viewsets.ModelViewSet):
    queryset = CommercialAdvisor.objects.all()
    serializer_class = CommercialAdvisorSerializer
    permission_classes = [AllowAny]

class BuilderCompanyViewSet(viewsets.ModelViewSet):
    queryset = BuilderCompany.objects.all()
    serializer_class = BuilderCompanySerializer
    permission_classes = [AllowAny]

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if user.is_constructora:
        builder = user.builder_company
        profile_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "identification": user.identification,
            },
            "incorporation_time": builder.incorporation_time,
            "legal_representative": builder.legal_representative,
            "address": builder.address,
        }
    elif user.is_asesor:
        advisor = user.commercial_advisor
        profile_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "identification": user.identification,
            },
            "biography": advisor.biography,
            "skills": advisor.skills,
            "reviews": advisor.reviews,
            "num_sales": advisor.num_sales,
        }
    else:
        return Response({"error": "Tipo de usuario no reconocido."}, status=400)

    return Response(profile_data)