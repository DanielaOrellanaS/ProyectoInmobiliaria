from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'asesores', CommercialAdvisorViewSet, basename='asesor')
router.register(r'constructoras', BuilderCompanyViewSet, basename='constructora')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
]
