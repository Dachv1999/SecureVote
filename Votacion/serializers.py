from .models import PartidoElectoral, Candidato, PadronElectoral, Votacion, Voto, Resultado
from rest_framework import serializers

class PartidoElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PartidoElectoral
        fields = ['id','nombre_partido','Sigla','Slogan','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Candidato
        fields = ['carnet_identidad','nombre','apellido','fecha_nacimiento','ciudad','email','telefono','domicilio','id_partido','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class PadronElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PadronElectoral
        fields = ['nro_padron','ci_usuario','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class VotacionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Votacion
        fields = ['id','tipo_votacion','id_padron','inicio_votacion','fin_votacion','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Voto
        fields = ['id','ci_votante','ci_candidato','id_votacion','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Resultado
        fields = ['id','ci_candidato','id_votacion','cant_votos','estado_result','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)