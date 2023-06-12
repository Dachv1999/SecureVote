from .models import PadronElectoral, Votacion, Voto, Resultado, PadronElectoralUsuario, Votacion_extended, Resultado_extended, Voto_extended
from rest_framework import serializers

""" class PartidoElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PartidoElectoral
        fields = ['id','nombre_partido','Sigla','Slogan','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',) """

""" class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Candidato
        fields = ['carnet_identidad','nombre','apellido','fecha_nacimiento','ciudad','email','telefono','domicilio','id_partido','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',) """

class PadronElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PadronElectoral
        fields = ['id','nombre','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class PadronElectoralUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PadronElectoralUsuario
        fields = ['id','ci_usuario','id_padron','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class VotacionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Votacion
        fields = ['id','tipo_votacion','inicio_votacion','fin_votacion','padron_electoral','partido1','partido2','partido3','partido4','activo','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class AllVotacionSerializer(serializers.ModelSerializer):
    votacion_id = VotacionSerializer(many=True)
    class Meta:
        model  = Votacion_extended
        fields = ['votacion_id']

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Voto
        fields = ['id','ci_votante','ci_candidato','hashvoto','id_votacion','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class AllVotoSerializer(serializers.ModelSerializer):
    voto_id = VotoSerializer(many=True)
    class Meta:
        model  = Voto_extended
        fields = ['voto_id']

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Resultado
        fields = ['id','ci_candidato','id_votacion','cant_votos','cant_vblanco','cant_vpositivo','cant_vnullo','estado_result','total_votos','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class AllResultadoSerializer(serializers.ModelSerializer):
    resultado_id = ResultadoSerializer(many=True)
    class Meta:
        model  = Resultado_extended
        fields = ['resultado_id']