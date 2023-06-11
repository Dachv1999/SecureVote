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
        fields = ['ci','cuenta','nombre','apellido','fecha_nacimiento','ciudad','email','informacion','total_ventas','total_ganancias','total_gastos','telefono','domicilio','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)