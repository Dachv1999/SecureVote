from rest_framework.routers import DefaultRouter
from .api import PadronElectoralViewSet, VotacionViewSet, VotoViewSet, ResultadoViewSet, PadronElectoralUsuarioViewSet, ReferendumViewSet, VotoReferendumViewSet, ResultadoReferendumViewSet

####################################################################
##                  Arma las rutas para el CRUD                   ## 
####################################################################

router_padron_electoral         = DefaultRouter()
router_padron_electoral_usuario = DefaultRouter()
#router_all_votacion             = DefaultRouter()
router_votacion                 = DefaultRouter()
router_voto                     = DefaultRouter()
router_resultado                = DefaultRouter()
router_referendum               = DefaultRouter()
router_votoReferendum           = DefaultRouter()
router_resultadoReferendum      = DefaultRouter()

router_padron_electoral.register(prefix='padron', basename='padron', viewset=PadronElectoralViewSet)
router_padron_electoral_usuario.register(prefix='padronUsuario', basename='padronUsuario', viewset=PadronElectoralUsuarioViewSet)
#router_all_votacion.register(prefix='allvotacion', basename='allvotacion', viewset=AllVotacionViewSet)
router_votacion.register(prefix='votacion', basename='votacion', viewset=VotacionViewSet)
router_voto.register(prefix='voto', basename='voto', viewset=VotoViewSet)
router_resultado.register(prefix='resultado', basename='resultado', viewset=ResultadoViewSet)
router_referendum.register(prefix='referendum', basename='referendum', viewset=ReferendumViewSet)
router_votoReferendum.register(prefix='votoReferendum', basename='votoReferendum', viewset=VotoReferendumViewSet)
router_resultadoReferendum.register(prefix='resultadoReferendum', basename='resultadoReferendum', viewset=ResultadoReferendumViewSet)

