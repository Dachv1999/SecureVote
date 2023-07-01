import json
import pytz
import random
from web3 import Web3
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import Votacion, PadronElectoral, PadronElectoralUsuario, Voto, Resultado, Referendum, VotoReferendum, ResultadoReferendum
from .serializers import PadronElectoralSerializer, PadronElectoralUsuarioSerializer, VotoSerializer, VotacionSerializer, ResultadoSerializer, AllVotacionSerializer, AllResultadoSerializer, ResultadoReferendumSerializer, VotoReferendumSerializer, ReferendumSerializer
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
        elif votacion.tipo_votacion == 'M':
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
                

@api_view(['GET'])
def calcularResultadoActal(request, id_votacion):
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
        
        votos_candidatos = [votos_candidato1, votos_candidato2, votos_candidato3, votos_candidato4]
        votos_validos = sum(votos_candidatos)
        total_votos = votos_validos + votos_blanco + votos_null

        return Response({
                    'candidato1': candidato1.nombre + " " + candidato1.apellido,
                    'votos1': votos_candidato1,
                    'partido1': partido1.nombre_partido,
                    'candidato2': candidato2.nombre + " " + candidato2.apellido,
                    'votos2': votos_candidato2,
                    'partido2': partido2.nombre_partido,
                    'candidato3': candidato3.nombre + " " + candidato3.apellido,
                    'votos3': votos_candidato3,
                    'partido3': partido3.nombre_partido,
                    'candidato4': candidato4.nombre + " " + candidato4.apellido,
                    'votos4': votos_candidato4,
                    'partido4': partido4.nombre_partido,
                    'votosB': votos_blanco,
                    'votosN': votos_null,
                    'votosTotal': total_votos,
                    'votacion': id_votacion,
                })


@api_view(['GET'])
def calcularResultadoProporcional(request, id_votacion):
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
        
        if votacion.tipo_votacion == 'P':
            resultado_indice, escanios_asignar = determinar_ganador_proporcional(votos_candidatos, votacion.escanio)

        if escanios_asignar[0] > escanios_asignar[1]:
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
                
                indice_escanio = resultado_indice.index(i)
                resultado.escanio_asig = escanios_asignar[indice_escanio]
                if cand == candidato:
                    resultado.estado_result = 'G'

                resultado.save()
                i += 1

            return Response({
                'status_code': status.HTTP_200_OK,
                'estado': "Hay un ganador"
            })
        else:
            if escanios_asignar[0] == escanios_asignar[1]:
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

                    indice_escanio = resultado_indice.index(i)
                    resultado.escanio_asig = escanios_asignar[indice_escanio]
                            
                    resultado.save()
                    i += 1

                return Response({
                    'status_code': status.HTTP_200_OK,
                    'estado': "No hay ganador, escaños repartidos equitativamente"
                })

def calcularResultadoProp(id_votacion):
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
        
        if sum(votos_candidatos) == 0:
            return Response({
                'status_code': status.HTTP_400_BAD_REQUEST,
                'estado': "No hay gandores, todos botos en blanco o nulos"
            })
        
        
        if votacion.tipo_votacion == 'P':
            resultado_indice, escanios_asignar = determinar_ganador_proporcional(votos_candidatos, votacion.escanio)

            
        if escanios_asignar[0] > escanios_asignar[1]:
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
                
                indice_escanio = resultado_indice.index(i)
                resultado.escanio_asig = escanios_asignar[indice_escanio]
                if cand == candidato:
                    resultado.estado_result = 'G'

                resultado.save()
                i += 1

            return Response({
                'status_code': status.HTTP_200_OK,
                'estado': "Hay un ganador"
            })
        else:
            if escanios_asignar[0] == escanios_asignar[1]:
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

                    indice_escanio = resultado_indice.index(i)
                    resultado.escanio_asig = escanios_asignar[indice_escanio]
                            
                    resultado.save()
                    i += 1

                return Response({
                    'status_code': status.HTTP_200_OK,
                    'estado': "No hay ganador, escaños repartidos equitativamente"
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


def determinar_ganador_proporcional(votos, num_escanos):
    print(votos)
    if sum(votos) == 0:
        return [], []
    
    num_partidos = len(votos)
    escanos = [0] * num_partidos

    # Crear una lista de tuplas (indice, votos) para tener en cuenta los partidos sin votos
    partidos = list(enumerate(votos))

    for _ in range(num_escanos):
        max_votos = 0
        indice_max = 0

        # Encuentra el partido con más votos sin escaños asignados
        for i, partido in partidos:
            if partido > max_votos and escanos[i] == 0:
                max_votos = partido
                indice_max = i

        # Asigna un escaño al partido seleccionado
        escanos[indice_max] += 1

    orden_posiciones = sorted(range(len(votos)), key=lambda i: votos[i], reverse=True)
    escanos_ordenados = sorted(escanos, reverse=True)

    return orden_posiciones, escanos_ordenados




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
    index     = received_json_data['index']
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
        voto.index = index
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
        voto.index = index
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
    voto.index = index
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
def devolverListaVotosHashReferendum(request, referendum_id):#devuelve la lista de votos con su hash de una solo referendum
    try: 
        referendum = Referendum.objects.get(id = referendum_id)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })
    
    votosRef = VotoReferendum.objects.filter(id_referendum=referendum.id)
    votosRefSerialized = VotoReferendumSerializer(votosRef, many=True)

    return Response({
        'votosRef' : votosRefSerialized.data
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

@api_view(['GET'])
def terminarReferendum(request, id_referendum):
    try:
        referendum = Referendum.objects.get(id = id_referendum, activo = True)
    except Referendum.DoesNotExist:
        return Response({
        'status_code': status.HTTP_404_NOT_FOUND,
        'error': 'Referendum no encontrado'
    })
    timezone = pytz.timezone('America/La_Paz')
    dt = datetime.now(timezone)
    referendum.fin_referendum = dt
    referendum.activo    = False
    referendum.save()
     
    resultadoReferendumGuardar(id_referendum)
    return Response({
        'status_code': status.HTTP_202_ACCEPTED,
        'msg': 'Referendum terminado satisfactoriamente'
    })

@api_view(['POST'])
def sufragarReferendum(request):
    received_json_data = json.loads(request.body.decode("utf-8")) #Obtener el JSON
    votante    = received_json_data['ci_votante']
    referendum = received_json_data['id_referendum']
    hashvoto   = received_json_data['hashvoto']
    index      = received_json_data['index']
    tipo_voto  = received_json_data['tipo_voto']

    votosRef = VotoReferendum.objects.filter(ci_votante = votante, id_referendum = referendum).count()
    if votosRef > 0:
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
        referen = Referendum.objects.get(id = referendum)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })

    if tipo_voto == 'N':#si el voto es nulo, no hay candidato
        voto = VotoReferendum()
        voto.ci_votante = usuario
        voto.id_referendum = referen
        voto.hashvoto = hashvoto
        voto.tipo_voto = 'N'
        voto.save()

        return Response({
            'status': status.HTTP_201_CREATED,
            'msg':'Voto creado y almacenado con exito'
        })

    if tipo_voto == 'B':#si el voto es blanco, no hay candidato
        voto = VotoReferendum()
        voto.ci_votante = usuario
        voto.id_referendum = referen
        voto.hashvoto = hashvoto
        voto.tipo_voto = 'B'
        voto.save()

        return Response({
            'status': status.HTTP_201_CREATED,
            'msg':'Voto creado y almacenado con exito'
        })

    voto = VotoReferendum()
    voto.ci_votante = usuario
    voto.id_referendum = referen
    voto.hashvoto = hashvoto
    voto.tipo_voto = tipo_voto
    voto.save()

    return Response({
            'status': status.HTTP_201_CREATED,
            'msg':'Voto creado y almacenado con exito'
        })

    
@api_view(['GET'])
def resultadoReferendum(request, id_referendum):
    
    try: 
        referendum = Referendum.objects.get(id = id_referendum)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })

    lista_resultado = calcularResultadoReferendum(id_referendum)
    posicion_mayor = lista_resultado.index(max(lista_resultado))

    resultado = ResultadoReferendum()
    resultado.id_referendum = referendum
    resultado.cant_vsi      = lista_resultado[0]
    resultado.cant_vno      = lista_resultado[1]
    resultado.cant_vnullo   = lista_resultado[2]
    resultado.cant_vblanco  = lista_resultado[3]
    resultado.total_votos   = lista_resultado[4]

    if(posicion_mayor == 0):
        resultado.ganador = "S"
    if(posicion_mayor == 1):
        resultado.ganador = "N"
    if(posicion_mayor == 2):
        resultado.ganador = "U"
    if(posicion_mayor == 3):
        resultado.ganador = "B"

    resultado.save()    

    serializerData = ResultadoReferendumSerializer(resultado)

    return Response({
            'resultado': serializerData.data
        })

def resultadoReferendumGuardar(id_referendum):
    
    try: 
        referendum = Referendum.objects.get(id = id_referendum)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })

    lista_resultado = calcularResultadoReferendum(id_referendum)

    lista_comparar = [lista_resultado[0], lista_resultado[1], lista_resultado[2], lista_resultado[3]]
    posicion_mayor = lista_resultado.index(max(lista_comparar))

    resultado = ResultadoReferendum()
    resultado.id_referendum = referendum
    resultado.cant_vsi      = lista_resultado[0]
    resultado.cant_vno      = lista_resultado[1]
    resultado.cant_vnullo   = lista_resultado[2]
    resultado.cant_vblanco  = lista_resultado[3]
    resultado.total_votos   = lista_resultado[4]

    if(posicion_mayor == 0):
        resultado.ganador = "S"
    if(posicion_mayor == 1):
        resultado.ganador = "N"
    if(posicion_mayor == 2):
        resultado.ganador = "U"
    if(posicion_mayor == 3):
        resultado.ganador = "B"

    resultado.save()    

    serializerData = ResultadoReferendumSerializer(resultado)

    return Response({
            'resultado': serializerData.data
        })

    
@api_view(['GET'])
def resultadoActualReferendum(request, id_referendum):
    
    try: 
        referendum = Referendum.objects.get(id = id_referendum)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })
    
    lista_resultado = calcularResultadoReferendum(id_referendum)
    posicion_mayor = lista_resultado.index(max(lista_resultado))

    resultado = ""
    if(posicion_mayor == 0):
        resultado = "votos a favor gana por el momento"
    if(posicion_mayor == 1):
        resultado = "votos en contra gana por el momento"
    if(posicion_mayor == 2):
        resultado = "votos nulos gana por el momento"
    if(posicion_mayor == 3):
        resultado = "votos en blanco gana por el momento"


    return Response({
            'ref_pregunta': referendum.pregunta,
            'votos_si': lista_resultado[0],
            'votos_no': lista_resultado[1],
            'votos_nulos': lista_resultado[2],
            'votos_blancos': lista_resultado[3],
            'total_votos': lista_resultado[4],
            'resultado':resultado
        })




def calcularResultadoReferendum(id_referendum):
    
    try: 
        referendum = Referendum.objects.get(id = id_referendum)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })
    
    resultado = []

    votosSi = VotoReferendum.objects.filter(id_referendum = referendum, tipo_voto = 'S').count() 
    votosNo = VotoReferendum.objects.filter(id_referendum = referendum, tipo_voto = 'N').count() 
    votosNulos = VotoReferendum.objects.filter(id_referendum = referendum, tipo_voto = 'U').count() 
    votosBlancos = VotoReferendum.objects.filter(id_referendum = referendum, tipo_voto = 'B').count() 
    totalVotos = votosSi + votosNo + votosNulos + votosBlancos

    resultado.append(votosSi)
    resultado.append(votosNo)
    resultado.append(votosNulos)
    resultado.append(votosBlancos)
    resultado.append(totalVotos)

    return resultado

@api_view(['GET'])
def devolverReferendumsPorUsuario(request, ci):
    padronesUsuarios = PadronElectoralUsuario.objects.filter(ci_usuario = ci)
    lista_padronesUsuarios = []
    for padronU in padronesUsuarios:
        lista_padronesUsuarios.append(padronU.id_padron.id)

    padrones = PadronElectoral.objects.filter(id__in = lista_padronesUsuarios)
    referendumUsuario = Referendum.objects.filter(padron_electoral__in=padrones, activo = True)

    votos = VotoReferendum.objects.filter(ci_votante = ci, id_referendum__in=referendumUsuario)
    lista_votos = []
    for voto in votos:
        lista_votos.append(voto.id_referendum.id)

    referendumUsuarioRealizadas = Referendum.objects.filter(id__in=lista_votos, activo = True)

    for votacion in referendumUsuario:
        if votacion in referendumUsuarioRealizadas:
            votacion.delete

    serializedData = ReferendumSerializer(referendumUsuario, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'referendums': serializedData.data
    })


@api_view(['GET'])
def devolverReferendumsActivas(request):
    referendumsUsuario = Referendum.objects.filter(activo = True)
    serializedData = ReferendumSerializer(referendumsUsuario, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'referendums': serializedData.data
    })


@api_view(['GET'])
def devolverResultadoReferendum(request,id_referendum):

    try: 
        referendum = Referendum.objects.get(id = id_referendum, activo = False)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })

    resultadoReferendum = ResultadoReferendum.objects.get(id_referendum = referendum.id)

    resultadosSerialized = ResultadoReferendumSerializer(resultadoReferendum)

    return Response({
            "referendums":resultadosSerialized.data,
        })

@api_view(['GET'])
def devolverResultadoReferendumPorUsuario(request,ci_usuario):

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

    referendumsUsuario = Referendum.objects.filter(padron_electoral__in=padron, activo = False)

    referendumsResultUsuario = ResultadoReferendum.objects.filter(id_referendum__in=referendumsUsuario)

    resultadosSerialized = ResultadoReferendumSerializer(referendumsResultUsuario, many=True)

    return Response({
            "referendums":resultadosSerialized.data,
        })

@api_view(['GET'])
def resultado_Automatico(request,id_votacion):
    
    try: 
        votacion = Votacion.objects.get(id = id_votacion)
    except Votacion.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Votacion no existe'
        })

    usuarios = Usuario.objects.all()
    listaCandidatos = [votacion.partido1, votacion.partido2, votacion.partido3, votacion.partido4]

    candidatos = []

    for usuario in usuarios:
        if usuario.id_partido in listaCandidatos:
            candidatos.append(usuario)

    
    padronElectoralUsuario = PadronElectoralUsuario.objects.filter(id_padron = votacion.padron_electoral)

    listaVotos = ['P', 'B', 'N']
    

    for usuario in padronElectoralUsuario:
        voto = Voto()
        voto.ci_votante   = usuario.ci_usuario
        voto.id_votacion  = votacion
        voto.tipo_voto    = listaVotos[gen_congruencial_mix(3)]

        if voto.tipo_voto == 'P':
            voto.ci_candidato = candidatos[gen_congruencial_mix(4)]
            voto.hashvoto     = votarNormal(voto.tipo_voto, votacion.id, voto.ci_candidato.ci)
        else:
            voto.hashvoto     = votarNormal(voto.tipo_voto, votacion.id, 111111)
        
        voto.index = getCantVotosNormal()
        voto.save()

    votacion.activo = False
    votacion.save()

    if votacion.tipo_votacion == 'N' or votacion.tipo_votacion == 'M':
        calcularResultadoInt(votacion.id)

        return JsonResponse({
            'status_code': status.HTTP_201_CREATED,
            'msg': 'Votacion Generada Exitosamente'
        })
    else:
        return calcularResultadoProp(votacion.id)

    
    
@api_view(['GET'])
def resultado_Automatico_Referendum(request,id_referendum):
    
    try: 
        referendum = Referendum.objects.get(id = id_referendum)
    except Referendum.DoesNotExist:
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'msg': 'Referendum no existe'
        })

    
    padronElectoralUsuario = PadronElectoralUsuario.objects.filter(id_padron = referendum.padron_electoral)

    listaVotos = ['S', 'N', 'B', 'U']
    
    for usuario in padronElectoralUsuario:
        voto = VotoReferendum()
        voto.ci_votante    = usuario.ci_usuario
        voto.id_referendum = referendum
        voto.tipo_voto     = listaVotos[gen_congruencial_mix(4)]
        voto.hashvoto      = votarReferendum(voto.tipo_voto, referendum.id)
        voto.index         = getCantVotosReferendum()

        voto.save()

    referendum.activo = False
    referendum.save()

    return resultadoReferendumGuardar(referendum.id)



def gen_congruencial_mix(m):
    seed = random.randint(0, 200) 
    a = random.randint(1, 50)   
    c = random.randint(1, 50)

    result = (a * seed + c) % m
    return result


#################################  SMART CONTRACT  ############################################


def votarNormal(vote_data,votacion_data,candidato_data):
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    contract = getContractVotoNormal(web3) #Obtenemos el contrato creado

    # Cargar la dirección y la clave privada del propietario de la cuenta
    sender_address = "0xe09353aF121d40D728edDf2f9040d04BEE6074A5"
    sender_private_key = "0x2a99f448ab31f7c566338f47a8a1fb603ee22d75fbbc9fb88e0e4e197ded9114"

    transaction = contract.functions.vote(vote_data, votacion_data, candidato_data).build_transaction({'from': sender_address,  'nonce': web3.eth.get_transaction_count(sender_address)})

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=sender_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    transaction_hash = web3.eth.wait_for_transaction_receipt(tx_hash)
    hash = web3.eth.get_transaction(transaction_hash['transactionHash'])

    return (hash['hash'].hex())

def getVotoNormal(index):
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    contract = getContractVotoNormal(web3)

    vote = contract.functions.getVote(index).call()

    return vote

def getCantVotosNormal():
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    contract = getContractVotoNormal(web3)

    cantVotes = contract.functions.getVoteCount().call()

    return cantVotes

def getContractVotoNormal(web3):

    # Cargar el contrato Solidity
    contract_address = "0x334473dACA2cc8D7c1203A941eC00f89FC9b8B07"
    contract_abi =[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_voteData",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_votacionData",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_candidatoData",
				"type": "uint256"
			}
		],
		"name": "vote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getVote",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getVoteCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "votes",
		"outputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "voteId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "voteData",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "votacionData",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "candidato",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract


def votarReferendum(vote_data,votacion_data):
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    contract = getContractVotoReferendum(web3) #Obtenemos el contrato creado

    # Cargar la dirección y la clave privada del propietario de la cuenta
    sender_address = "0xe09353aF121d40D728edDf2f9040d04BEE6074A5"
    sender_private_key = "0x2a99f448ab31f7c566338f47a8a1fb603ee22d75fbbc9fb88e0e4e197ded9114"

    transaction = contract.functions.vote(vote_data, votacion_data).build_transaction({'from': sender_address,  'nonce': web3.eth.get_transaction_count(sender_address)})

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=sender_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    transaction_hash = web3.eth.wait_for_transaction_receipt(tx_hash)
    hash = web3.eth.get_transaction(transaction_hash['transactionHash'])

    return (hash['hash'].hex())

def getVotoReferendum(index):
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    contract = getContractVotoReferendum(web3)

    vote = contract.functions.getVote(index).call()

    return vote

def getCantVotosReferendum():
    # Conectar a la instancia de Ganache
    ganache_url = "http://localhost:7545"  
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    contract = getContractVotoReferendum(web3)

    cantVotes = contract.functions.getVoteCount().call()

    return cantVotes

def getContractVotoReferendum(web3):

    # Cargar el contrato Solidity
    contract_address = "0x62e3e75D16BD14A79d4Ae713519988cA4c4E6244"
    contract_abi =[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_voteData",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_votacionData",
				"type": "uint256"
			}
		],
		"name": "vote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getVote",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getVoteCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "votes",
		"outputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "voteId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "voteData",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "votacionData",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

#############################################################################################


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




