from .models import PadronElectoral, Votacion, Voto, Resultado, PadronElectoralUsuario, Votacion_extended
from rest_framework import viewsets, permissions
from .serializers import PadronElectoralSerializer, VotacionSerializer,AllVotacionSerializer, VotoSerializer, ResultadoSerializer, PadronElectoralUsuarioSerializer

####################################################################
##            Implementa un crud basico para cada modelo          ## 
####################################################################


""" class CandidatoViewSet(viewsets.ModelViewSet):
    queryset = Candidato.objects.all().order_by('carnet_identidad')
    serializer_class   = CandidatoSerializer
    permission_classes = [permissions.AllowAny] """

class PadronElectoralViewSet(viewsets.ModelViewSet):
    queryset = PadronElectoral.objects.all()
    serializer_class   = PadronElectoralSerializer
    permission_classes = [permissions.AllowAny]

class PadronElectoralUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PadronElectoralUsuario.objects.all()
    serializer_class   = PadronElectoralUsuarioSerializer
    permission_classes = [permissions.AllowAny]

class VotacionViewSet(viewsets.ModelViewSet):
    queryset = Votacion.objects.all()
    serializer_class   = VotacionSerializer
    permission_classes = [permissions.AllowAny]

#class AllVotacionViewSet(viewsets.ModelViewSet):
#    queryset = Votacion_extended.objects.all()
#    serializer_class   = AllVotacionSerializer
#    permission_classes = [permissions.AllowAny]

class VotoViewSet(viewsets.ModelViewSet):
    queryset = Voto.objects.all()
    serializer_class   = VotoSerializer
    permission_classes = [permissions.AllowAny]

class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class   = ResultadoSerializer
    permission_classes = [permissions.AllowAny]