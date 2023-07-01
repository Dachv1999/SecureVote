from .models import PadronElectoral, Votacion, Voto, Resultado, PadronElectoralUsuario, Votacion_extended, Resultado_extended, Voto_extended, Referendum, Referendum_extended, VotoReferendum, VotoReferendum_extended, ResultadoReferendum, ResultadoReferendum_extended
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
        fields = ['id','nombre','tipo_votacion','inicio_votacion','fin_votacion','padron_electoral','partido1','partido2','partido3','partido4','activo','escanio','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class AllVotacionSerializer(serializers.ModelSerializer):
    votacion_id = VotacionSerializer(many=True)
    class Meta:
        model  = Votacion_extended
        fields = ['votacion_id']

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Voto
        fields = ['id','ci_votante','ci_candidato','hashvoto','index','id_votacion','tipo_voto','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class AllVotoSerializer(serializers.ModelSerializer):
    voto_id = VotoSerializer(many=True)
    class Meta:
        model  = Voto_extended
        fields = ['voto_id']

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Resultado
        fields = ['id','ci_candidato','id_votacion','cant_votos','cant_vblanco','cant_vpositivo','cant_vnullo','estado_result','total_votos','escanio_asig','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class AllResultadoSerializer(serializers.ModelSerializer):
    resultado_id = ResultadoSerializer(many=True)
    class Meta:
        model  = Resultado_extended
        fields = ['resultado_id']

class ReferendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referendum
        fields = '__all__'
        read_onty_fields = ('created_at', 'updated_at',)

class AllReferendumSerializer(serializers.ModelSerializer):
    referendum_id = ReferendumSerializer(many=True)
    class Meta:
        model  = Referendum_extended
        fields = ['referendum_id']

class VotoReferendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotoReferendum
        fields = '__all__'
        read_onty_fields = ('created_at', 'updated_at',)

class AllVotoReferendumSerializer(serializers.ModelSerializer):
    votoRef_id = VotoReferendumSerializer(many=True)
    class Meta:
        model  = VotoReferendum
        fields = ['votoRef_id']

class ResultadoReferendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoReferendum
        fields = '__all__'
        read_onty_fields = ('created_at', 'updated_at',)

class AllResultadoReferendumSerializer(serializers.ModelSerializer):
    resultadoRef_id = ResultadoReferendumSerializer(many=True)
    class Meta:
        model  = ResultadoReferendum_extended
        fields = ['resultadoRef_id']