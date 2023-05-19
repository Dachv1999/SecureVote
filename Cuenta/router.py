from rest_framework.routers import DefaultRouter
from .api import UsuarioViewSet, PartidoElectoralViewSet

####################################################################
##                  Arma las rutas para el CRUD                   ## 
####################################################################

router_usuario           = DefaultRouter()
router_partido_electoral = DefaultRouter()

router_usuario.register(prefix='usuario', basename='usuario', viewset=UsuarioViewSet)
router_partido_electoral.register(prefix='partido', basename='partido', viewset=PartidoElectoralViewSet)
