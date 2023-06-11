import json
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .models import Usuario

@api_view(['POST'])
def login(request):

    #request.method == 'POST':
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    email = received_json_data['email']
    password = received_json_data['password']

    try: 
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response("Email inválido")
    
    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return Response("Contraseña inválida")
    
    token, _ = Token.objects.get_or_create(user=user)

    return Response(token.key)



