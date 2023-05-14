from rest_framework.routers import DefaultRouter
from .api import UsuarioViewSet

router_usuario = DefaultRouter()

router_usuario.register(prefix='usuario', basename='usuario', viewset=UsuarioViewSet)
