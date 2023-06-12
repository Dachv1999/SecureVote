import json
import pytz
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import Votacion, PadronElectoral, PadronElectoralUsuario, Voto, Resultado
from .serializers import PadronElectoralSerializer, PadronElectoralUsuarioSerializer, VotoSerializer, VotacionSerializer, ResultadoSerializer, AllVotacionSerializer, AllResultadoSerializer
from Cuenta.models import PartidoElectoral, Usuario
from Cuenta.serializers import UsuarioSerializer
from datetime import datetime, timedelta


def calcularResultadoInt(id_votacion):
    votacion = Votacion.objects.get(id = id_votacion)

    if votacion.activo == False:
        partido1 = PartidoElectoral.objects.get(id = votacion.partido1.id)
        partido2 = PartidoElectoral.objects.get(id = votacion.partido2.id)
        partido3 = PartidoElectoral.objects.get(id = votacion.partido3.id)
        partido4 = PartidoElectoral.objects.get(id = votacion.partido4.id)

        candidato1 = Usuario.objects.filter(id_partido = partido1).first()
        candidato2 = Usuario.objects.filter(id_partido = partido2).first()
        candidato3 = Usuario.objects.filter(id_partido = partido3).first()
        candidato4 = Usuario.objects.filter(id_partido = partido4).first()

        votos_candidato1 = Voto.objects.filter(ci_candidato = candidato1, id_votacion = votacion, tipo_voto='P').count()
        votos_candidato2 = Voto.objects.filter(ci_candidato = candidato2, id_votacion = votacion, tipo_voto='P').count()
        votos_candidato3 = Voto.objects.filter(ci_candidato = candidato3, id_votacion = votacion, tipo_voto='P').count()
        votos_candidato4 = Voto.objects.filter(ci_candidato = candidato4, id_votacion = votacion, tipo_voto='P').count()

        votos_blanco     = Voto.objects.filter(id_votacion = votacion, tipo_voto='B' ).count()
        votos_null       = Voto.objects.filter(id_votacion = votacion, tipo_voto='N' ).count()  
        
        candidatos = [candidato1, candidato2, candidato3, candidato4]
        votos_candidatos = [votos_candidato1, votos_candidato2, votos_candidato3, votos_candidato4]
        votos_validos = sum(votos_candidatos)
        total_votos = votos_validos + votos_blanco + votos_null

        if votacion.tipo_votacion == 'N':
            resultado_indice = determinar_ganador_Normal(votos_candidatos)
        else:
            resultado_indice = determinar_ganador_MayoriaAbs(votos_candidatos)

        if len(resultado_indice) == 1:
            candidato = candidatos[resultado_indice[0]]

            i = 0
            for cand in candidatos:
                resultado = Resultado()
                resultado.ci_candidato = cand
                resultado.id_votacion = votacion
                resultado.total_votos = total_votos
                resultado.cant_votos = votos_candidatos[i]
                resultado.cant_vpositivo = votos_validos
                resultado.cant_vblanco = votos_blanco
                resultado.cant_vnullo = votos_null
                
                if cand == candidato:
                    resultado.estado_result = 'G'

                resultado.save()
                i += 1
        else:
            if len(resultado_indice) == 0:
                i = 0
                for cand in candidatos:
                    resultado = Resultado()
                    resultado.ci_candidato = cand
                    resultado.id_votacion = votacion
                    resultado.total_votos = total_votos
                    resultado.cant_votos = votos_candidatos[i]
                    resultado.cant_vpositivo = votos_validos
                    resultado.cant_vblanco = votos_blanco
                    resultado.cant_vnullo = votos_null

                    resultado.save()
                    i += 1
            else:
                empate_candidatos = []
                for x in resultado_indice:
                    empate_candidatos.append(candidatos[x])
                    
                i = 0
                for cand in candidatos:
                    resultado = Resultado()
                    resultado.ci_candidato = cand
                    resultado.id_votacion = votacion
                    resultado.total_votos = total_votos
                    resultado.cant_votos = votos_candidatos[i]
                    resultado.cant_vpositivo = votos_validos
                    resultado.cant_vblanco = votos_blanco
                    resultado.cant_vnullo = votos_null

                    if cand in empate_candidatos:
                        resultado.estado_result = 'E'

                    resultado.save()
                    i += 1

@api_view(['GET'])
def calcularResultado(request, id_votacion):
    votacion = Votacion.objects.get(id = id_votacion)

    if votacion.activo == False:
        partido1 = PartidoElectoral.objects.get(id = votacion.partido1.id)
        partido2 = PartidoElectoral.objects.get(id = votacion.partido2.id)
        partido3 = PartidoElectoral.objects.get(id = votacion.partido3.id)
        partido4 = PartidoElectoral.objects.get(id = votacion.partido4.id)

        candidato1 = Usuario.objects.filter(id_partido = partido1).first()
        candidato2 = Usuario.objects.filter(id_partido = partido2).first()
        candidato3 = Usuario.objects.filter(id_partido = partido3).first()
        candidato4 = Usuario.objects.filter(id_partido = partido4).first()

        votos_candidato1 = Voto.objects.filter(ci_candidato = candidato1, id_votacion = votacion, tipo_voto='P').count()
        votos_candidato2 = Voto.objects.filter(ci_candidato = candidato2, id_votacion = votacion, tipo_voto='P').count()
        votos_candidato3 = Voto.objects.filter(ci_candidato = candidato3, id_votacion = votacion, tipo_voto='P').count()
        votos_candidato4 = Voto.objects.filter(ci_candidato = candidato4, id_votacion = votacion, tipo_voto='P').count()

        votos_blanco     = Voto.objects.filter(id_votacion = votacion, tipo_voto='B' ).count()
        votos_null       = Voto.objects.filter(id_votacion = votacion, tipo_voto='N' ).count()  
        
        candidatos = [candidato1, candidato2, candidato3, candidato4]
        votos_candidatos = [votos_candidato1, votos_candidato2, votos_candidato3, votos_candidato4]
        votos_validos = sum(votos_candidatos)
        total_votos = votos_validos + votos_blanco + votos_null

        if votacion.tipo_votacion == 'N':
            resultado_indice = determinar_ganador_Normal(votos_candidatos)
        else:
            resultado_indice = determinar_ganador_MayoriaAbs(votos_candidatos)

        if len(resultado_indice) == 1:
            candidato = candidatos[resultado_indice[0]]

            i = 0
            for cand in candidatos:
                resultado = Resultado()
                resultado.ci_candidato = cand
                resultado.id_votacion = votacion
                resultado.total_votos = total_votos
                resultado.cant_votos = votos_candidatos[i]
                resultado.cant_vpositivo = votos_validos
                resultado.cant_vblanco = votos_blanco
                resultado.cant_vnullo = votos_null
                
                if cand == candidato:
                    resultado.estado_result = 'G'

                resultado.save()
                i += 1

                return Response({
                    'status_code': status.HTTP_200_OK,
                    'estado': "Hay un ganador"
                })
        else:
            if len(resultado_indice) == 0:
                i = 0
                for cand in candidatos:
                    resultado = Resultado()
                    resultado.ci_candidato = cand
                    resultado.id_votacion = votacion
                    resultado.total_votos = total_votos
                    resultado.cant_votos = votos_candidatos[i]
                    resultado.cant_vpositivo = votos_validos
                    resultado.cant_vblanco = votos_blanco
                    resultado.cant_vnullo = votos_null

                    resultado.save()
                    i += 1

                    return Response({
                        'status_code': status.HTTP_200_OK,
                        'estado': "No Hay ganador por mayoria absoluta"
                    })
            else:
                empate_candidatos = []
                for x in resultado_indice:
                    empate_candidatos.append(candidatos[x])
                    
                i = 0
                for cand in candidatos:
                    resultado = Resultado()
                    resultado.ci_candidato = cand
                    resultado.id_votacion = votacion
                    resultado.total_votos = total_votos
                    resultado.cant_votos = votos_candidatos[i]
                    resultado.cant_vpositivo = votos_validos
                    resultado.cant_vblanco = votos_blanco
                    resultado.cant_vnullo = votos_null

                    if cand in empate_candidatos:
                        resultado.estado_result = 'E'

                    resultado.save()
                    i += 1
                    return Response({
                        'status_code': status.HTTP_200_OK,
                        'estado': "Hay empate"
                    })

def determinar_ganador_MayoriaAbs(votos_candidatos):
    # Obtener el número total de votos
    votos_validos = sum(votos_candidatos)

    # Obtener el número máximo de votos obtenidos por un candidato
    max_votos = max(votos_candidatos)

    # Verificar si hay un candidato con mayoría absoluta
    if max_votos > votos_validos / 2:
        # Encontrar el índice del candidato ganador
        indice_ganador = [votos_candidatos.index(max_votos)]
        return indice_ganador

    # Si hay un empate entre varios candidatos
    empate = [i for i, votos in enumerate(votos_candidatos) if votos == max_votos]
    if len(empate) > 1:
        return empate

    # Si no hay ganador por mayoría absoluta ni empate
    return []

def determinar_ganador_Normal(votos_candidatos):

    # Calcular el número total de votos válidos
    votos_validos = sum(votos_candidatos)

    # Calcular el porcentaje de votos para cada candidato
    porcentajes = [votos / votos_validos * 100 for votos in votos_candidatos]

    # Obtener el número máximo de votos obtenidos por un candidato
    max_votos = max(porcentajes)

    # Encontrar el índice del candidato con el mayor porcentaje de votos
    indice_ganador = [porcentajes.index(max_votos)]

    # Verificar si hay empate entre varios candidatos
    empate = [i for i, porcentaje in enumerate(porcentajes) if porcentaje == max_votos]
    if len(empate) > 1:
        return empate

    # Si no hay empate, retornar inice ganador
    return indice_ganador


@api_view(['GET'])
def devolverVotacionesPorUsuario(request, ci):
    padronesUsuarios = PadronElectoralUsuario.objects.filter(ci_usuario = ci)
    lista_padronesUsuarios = []
    for padronU in padronesUsuarios:
        lista_padronesUsuarios.append(padronU.id_padron.id)

    padrones = PadronElectoral.objects.filter(id__in = lista_padronesUsuarios)
    votacionUsuario = Votacion.objects.filter(padron_electoral__in=padrones, activo = True)

    votos = Voto.objects.filter(ci_votante = ci, id_votacion__in=votacionUsuario)
    lista_votos = []
    for voto in votos:
        lista_votos.append(voto.id_votacion.id)

    votacionUsuarioRealizadas = Votacion.objects.filter(id__in=lista_votos, activo = True)

    for votacion in votacionUsuario:
        if votacion in votacionUsuarioRealizadas:
            votacion.delete

    serializedData = VotacionSerializer(votacionUsuario, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'transactions': serializedData.data
    })


@api_view(['GET'])
def devolverVotacionesActivas(request):
    votacionUsuario = Votacion.objects.filter(activo = True)
    serializedData = VotacionSerializer(votacionUsuario, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'transactions': serializedData.data
    })

@api_view(['GET'])
def devolverResultadoVotacion(request, id_votacion):

    try: 
        votacion = Votacion.objects.get(id = id_votacion)
    except Votacion.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Votacion no existe'
        })
    
    cant_perd = Resultado.objects.filter(id_votacion = votacion, estado_result = 'P').count()

    candi_result = Resultado.objects.filter(id_votacion = votacion)
    resulSerialized = ResultadoSerializer(candi_result, many=True)

    if cant_perd == 3:
        ganador = Resultado.objects.get(id_votacion = votacion, estado_result = 'G')
        ganadorSerialized = ResultadoSerializer(ganador)
        return Response({
            'resultado':resulSerialized.data,
            'resultado_especifico': ganadorSerialized.data,
            'status': 'Ganador'
        })
    
    if  cant_perd < 3:

        empatadores = Resultado.objects.filter(id_votacion = votacion, estado_result = 'E')
        empatadoresSerialized = ResultadoSerializer(empatadores, many=True)
        return Response({
            'resultado':resulSerialized.data,
            'resultado_especifico': empatadoresSerialized.data,
            'status':'Empate'
        })
    
    if cant_perd == 4:
        return Response({
            'resultado':resulSerialized.data,
            'status':'Perdido'
        })
    
@api_view(['GET'])
def devolverResultadoVotacionPorUsuario(request,ci_usuario):

    try: 
        usuario = Usuario.objects.get(ci = ci_usuario)
    except Usuario.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Votacion no existe'
        })
    

    padronesUsuario = PadronElectoralUsuario.objects.filter(ci_usuario = usuario)
    lista_padrones = []
    for padron_normal in padronesUsuario:
        lista_padrones.append(padron_normal.id_padron.id)

    padron = PadronElectoral.objects.filter(id__in = lista_padrones)

    votacionesUsuario = Votacion.objects.filter(padron_electoral__in=padron, activo = False)

    resultados_final = []

    for votacion in votacionesUsuario:
        cant_perd = Resultado.objects.filter(id_votacion = votacion, estado_result = 'P').count()

        if cant_perd == 3:
            ganador = Resultado.objects.get(id_votacion = votacion, estado_result = 'G')
            #ganadorSerialized = ResultadoSerializer(ganador)
            resultados_final.append(ganador)
        
        if  cant_perd < 3 and cant_perd > 0:

            empatador = Resultado.objects.filter(id_votacion = votacion, estado_result = 'E').first()
            #empatadoresSerialized = ResultadoSerializer(empatador)
            resultados_final.append(empatador)

        if cant_perd == 4:
            perdedor = Resultado.objects.filter(id_votacion = votacion, estado_result = 'P').first()
            #empatadoresSerialized = ResultadoSerializer(perdedor)
            resultados_final.append(perdedor)


    resultadosSerialized = ResultadoSerializer(resultados_final, many=True)

    return Response({
            "respuesta":resultadosSerialized.data,
        })


@api_view(['POST'])
def sufragar(request):
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    votante   = received_json_data['ci_votante']
    candidato = received_json_data['ci_candidato']
    votacion  = received_json_data['id_votacion']
    hashvoto  = received_json_data['hashvoto']
    tipo_voto = received_json_data['tipo_voto']

    voto = Voto.objects.filter(ci_votante = votante, id_votacion = votacion).count()
    if voto > 0:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'msg':'Ya realizo un voto'
        })
    

    try: 
        usuario = Usuario.objects.get(ci = votante)
    except Usuario.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Votante no existe'
        })
    
    try: 
        votac = Votacion.objects.get(id = votacion)
    except Votacion.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Votacion no existe'
        })
    
    if candidato == 'N':#si el voto es nulo, no hay candidato
        voto = Voto()
        voto.ci_votante = usuario
        voto.id_votacion = votac
        voto.hashvoto = hashvoto
        voto.tipo_voto = 'N'
        voto.save()

        return Response({
            'status': status.HTTP_201_CREATED,
            'msg':'Voto creado y almacenado con exito'
        })

    if candidato == 'B':#si el voto es blanco, no hay candidato
        voto = Voto()
        voto.ci_votante = usuario
        voto.id_votacion = votac
        voto.hashvoto = hashvoto
        voto.tipo_voto = 'B'
        voto.save()

        return Response({
            'status': status.HTTP_201_CREATED,
            'msg':'Voto creado y almacenado con exito'
        })
    
    try: 
        usuarioCan = Usuario.objects.get(ci = candidato)
    except Usuario.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Candidato no existe'
        })
    
    

    voto = Voto()
    voto.ci_votante = usuario
    voto.ci_candidato = usuarioCan
    voto.id_votacion = votac
    voto.hashvoto = hashvoto
    voto.tipo_voto = tipo_voto
    voto.save()

    return Response({
            'status': status.HTTP_201_CREATED,
            'msg':'Voto creado y almacenado con exito'
        })

@api_view(['GET'])
def devolverListaVotosHash(request, votacion_id):#devuelve la lista de votos con su hash de una sola votacion
    try: 
        votacion = Votacion.objects.get(id = votacion_id)
    except Votacion.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Votacion no existe'
        })
    
    votos = Voto.objects.filter(id_votacion=votacion.id)
    votosSerialized = VotoSerializer(votos, many=True)

    return Response({
        'votos' : votosSerialized.data
    })



@api_view(['GET'])
def terminarVotacion(request, id_votacion):
    try:
        votacion = Votacion.objects.get(id = id_votacion, activo = True)
    except Votacion.DoesNotExist:
        return Response({
        'status_code': status.HTTP_404_NOT_FOUND,
        'error': 'Votacion no encontrada'
    })
    timezone = pytz.timezone('America/La_Paz')
    dt = datetime.now(timezone)
    votacion.fin_votacion = dt
    votacion.activo    = False
    votacion.save()
     
    calcularResultadoInt(id_votacion)
    return Response({
        'status_code': status.HTTP_202_ACCEPTED,
        'msg': 'Votación terminada satisfactoriamente'
    })

""" @api_view(['POST'])
def agregarUsuarioaPadron(request):
    try:
        votacion = Votacion.objects.get(id = id_votacion)
    except Votacion.DoesNotExist:
        return Response({
        'status_code': status.HTTP_404_NOT_FOUND,
        'error': 'Votacion no encontrada'
    })
    
    votacion.fin_votacion = timezone.now
    votacion.activo    = False
    votacion.save()
     
    calcularResultado(id_votacion)
    return Response({
        'status_code': status.HTTP_202_ACCEPTED,
        'msg': 'Votación terminada satisfactoriamente'
    }) """

