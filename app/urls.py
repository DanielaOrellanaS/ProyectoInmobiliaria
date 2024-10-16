from django.urls import path, include
from rest_framework import routers
from .views import *

# Crear el enrutador
router = routers.DefaultRouter()
router.register(r'asesores', AsesorComercialViewSet, basename='asesor')
router.register(r'constructoras', ConstructoraInmobiliariaViewSet, basename='constructora')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
]
