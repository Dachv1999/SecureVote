from .models import Usuario
from rest_framework import viewsets, permissions
from .serializers import UsuarioSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('carnet_identidad')
    serializer_class   = UsuarioSerializer
    permission_classes = [permissions.AllowAny]