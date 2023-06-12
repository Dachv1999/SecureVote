import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, date

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.hashers import check_password

from .models import Usuario
from .serializers import UsuarioTokenSerializer, UsuarioSerializer
from Votacion.models import PartidoElectoral

@api_view(['POST'])
def register(request):
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON

    ci           = received_json_data['ci']
    nombre       = received_json_data['nombre']
    apellido     = received_json_data['apellido']
    fec_nac      = received_json_data['fecha_nacimiento']
    ciudad       = received_json_data['ciudad']
    email        = received_json_data['email']
    password     = received_json_data['password']
    telefono     = received_json_data['telefono']
    is_superuser = received_json_data['is_superuser']


    """ formatter_string = "%d-%m-%y" 
    datetime_object = datetime.strptime(fec_nac, formatter_string)
    date_object = datetime_object.date()
 """
    user = Usuario()

    user.ci = ci
    user.nombre = nombre
    user.apellido = apellido
    user.fecha_nacimiento = fec_nac
    user.ciudad = ciudad
    user.telefono = telefono
    user.email = email
    user.set_password(password)
    user.is_superuser = is_superuser

    user.save()

    user_serializer = UsuarioSerializer(user)

    return Response({
        'status_code': status.HTTP_201_CREATED,
        'msg': 'Usuario creado',
        'user': user_serializer.data
    })


@api_view(['POST'])
def login(request):

    #request.method == 'POST':
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    email = received_json_data['email']
    password = received_json_data['password']

    try: 
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Email Inválido'
        })

    
    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Contraseña Inválida'
        })

    
    token, _ = Token.objects.get_or_create(user=user)
    user_serializer = UsuarioTokenSerializer(user)
    return Response({
        'status_code': status.HTTP_201_CREATED,
        'msg': 'Inicio de Sesión satisfactoriamente',
        'user': user_serializer.data,
        'token': token.key
    })


@api_view(['POST'])
def logout(request):
    try:
        received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
        token = received_json_data['token']
        token = Token.objects.filter(key=token).first()

        if token:
            token.delete()

            return JsonResponse({
                'status_code': status.HTTP_200_OK,
                'msg': 'Token eliminado'
            })
        
        return JsonResponse({
                'status_code': status.HTTP_400_BAD_REQUEST,
                'msg': 'No se ha encontrado un usuario con esas credenciales'
            })

    except:
        JsonResponse({
                'status_code': status.HTTP_409_CONFLICT,
                'msg': 'No se ha encontrado token en la peticion'
            })
        
@api_view(['GET'])
def devolverCandidato(request, id_partido):
    partido = PartidoElectoral.objects.get(id = id_partido)
    candidato = Usuario.objects.filter(id_partido = partido).first()
    dataSerializer = UsuarioSerializer(candidato)

    return Response({
        'candidato': dataSerializer.data
    })

@api_view(['GET'])
def devUsrporPartidoE(request, id_partido1, id_partido2, id_partido3, id_partido4):

    partido1 = PartidoElectoral.objects.get(id = id_partido1)
    partido2 = PartidoElectoral.objects.get(id = id_partido2)
    partido3 = PartidoElectoral.objects.get(id = id_partido3)
    partido4 = PartidoElectoral.objects.get(id = id_partido4)

    candidato1 = Usuario.objects.filter(id_partido = partido1).first()
    candidato2 = Usuario.objects.filter(id_partido = partido2).first()
    candidato3 = Usuario.objects.filter(id_partido = partido3).first()
    candidato4 = Usuario.objects.filter(id_partido = partido4).first()

    cand1serialized = UsuarioSerializer(candidato1)
    cand2serialized = UsuarioSerializer(candidato2)
    cand3serialized = UsuarioSerializer(candidato3)
    cand4serialized = UsuarioSerializer(candidato4)

    return Response({
        'candidato1':cand1serialized.data,
        'candidato2':cand2serialized.data,
        'candidato3':cand3serialized.data,
        'candidato4':cand4serialized.data,
    })


@api_view(['GET'])
def devUsrsinPartido(request):
    usuariosSinPartido = Usuario.objects.filter(id_partido__isnull = True)

    serializedUser = UsuarioSerializer(usuariosSinPartido, many = True)
    
    return Response({
        'usuarios': serializedUser.data
    })



