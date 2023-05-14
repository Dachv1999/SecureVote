from .models import Usuario
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Usuario
        fields = ['carnet_identidad','nombre','apellido','fecha_nacimiento','ciudad','email','telefono','domicilio','created_at','updated_at']
        read_onty_fields = ('created_at', 'updated_at',)