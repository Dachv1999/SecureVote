from .models import Usuario, PartidoElectoral
from rest_framework import viewsets, permissions
from .serializers import UsuarioSerializer, PartidoElectoralSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################

class PartidoElectoralViewSet(viewsets.ModelViewSet):
    queryset = PartidoElectoral.objects.all()
    serializer_class   = PartidoElectoralSerializer
    permission_classes = [permissions.AllowAny]

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('ci')
    serializer_class   = UsuarioSerializer
    permission_classes = [permissions.AllowAny]