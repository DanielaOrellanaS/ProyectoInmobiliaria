from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("¡Hola, este es mi primer proyecto Django con rutas!")
