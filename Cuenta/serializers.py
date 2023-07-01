from .models import Usuario, PartidoElectoral
from rest_framework import serializers

class PartidoElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PartidoElectoral
        fields = ['id','nombre_partido','Sigla','Slogan','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Usuario
        fields = ['ci','nombre','apellido','fecha_nacimiento','ciudad','email','informacion','telefono','id_partido','is_superuser','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)

class UsuarioTokenSerializer(serializers.ModelSerializer):  #clase para lo que el JSON devolvera
    class Meta:
        model  = Usuario
        fields = ['ci','nombre','apellido','email','is_superuser']