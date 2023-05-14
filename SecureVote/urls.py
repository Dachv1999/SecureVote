"""
URL configuration for SecureVote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Cuenta.router import router_usuario
from Votacion.router import router_partido_electoral, router_padron_electoral, router_candidato, router_votacion, router_resultado, router_voto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router_usuario.urls)),
    path('api/', include(router_candidato.urls)),
    path('api/', include(router_partido_electoral.urls)),
    path('api/', include(router_padron_electoral.urls)),
    path('api/', include(router_votacion.urls)),
    path('api/', include(router_voto.urls)),
    path('api/', include(router_resultado.urls))
]
