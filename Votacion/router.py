from rest_framework.routers import DefaultRouter
from .api import PadronElectoralViewSet, VotacionViewSet, VotoViewSet, ResultadoViewSet

####################################################################
##                  Arma las rutas para el CRUD                   ## 
####################################################################

router_padron_electoral  = DefaultRouter()
router_votacion          = DefaultRouter()
router_voto              = DefaultRouter()
router_resultado         = DefaultRouter()

router_padron_electoral.register(prefix='padron', basename='padron', viewset=PadronElectoralViewSet)
router_votacion.register(prefix='votacion', basename='votacion', viewset=VotacionViewSet)
router_voto.register(prefix='voto', basename='voto', viewset=VotoViewSet)
router_resultado.register(prefix='resultado', basename='resultado', viewset=ResultadoViewSet)

