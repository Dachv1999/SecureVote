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

from Cuenta.router import router_usuario, router_partido_electoral
from Votacion.router import router_padron_electoral,router_padron_electoral_usuario, router_votacion, router_resultado, router_voto, router_referendum, router_resultadoReferendum, router_votoReferendum
from Cuenta.views import login, logout, register, devolverCandidato, devUsrporPartidoE, devUsrsinPartido, buscadorUsuarios
from Votacion.views import calcularResultado, devolverVotacionesPorUsuario, devolverVotacionesActivas, devolverResultadoVotacion, devolverResultadoVotacionPorUsuario, sufragar, devolverListaVotosHash, devolverListaVotosHashReferendum, terminarVotacion, calcularResultadoActal, calcularResultadoProporcional, devolverVotacionesPorUsuario, terminarReferendum, sufragarReferendum, resultadoReferendum, resultadoActualReferendum, devolverReferendumsPorUsuario, devolverReferendumsActivas, devolverResultadoReferendum, devolverResultadoReferendumPorUsuario, resultado_Automatico, resultado_Automatico_Referendum

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router_usuario.urls)),
    path('api/', include(router_partido_electoral.urls)),
    path('api/', include(router_padron_electoral.urls)),
    path('api/', include(router_padron_electoral_usuario.urls)),
    path('api/', include(router_votacion.urls)),
    path('api/', include(router_voto.urls)),
    path('api/', include(router_resultado.urls)),
    path('api/', include(router_referendum.urls)),
    path('api/', include(router_votoReferendum.urls)),
    path('api/', include(router_resultadoReferendum.urls)),

    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('getCandidato/<int:id_partido>/', devolverCandidato),
    path('getCandxPartido/<int:id_partido1>/<int:id_partido2>/<int:id_partido3>/<int:id_partido4>/', devUsrporPartidoE),
    path('getUsersSinPartido/', devUsrsinPartido),
    path('buscarUsuarios/', buscadorUsuarios),

    path('calcResultado/<int:id_votacion>/', calcularResultado),
    path('calcResultadoProporcional/<int:id_votacion>', calcularResultadoProporcional),
    path('getVotacionesxUsuario/<int:ci>', devolverVotacionesPorUsuario),
    path('getVotacionesActivas/', devolverVotacionesActivas),
    path('getResultVotacion/<int:id_votacion>', devolverResultadoVotacion),
    path('getResultVotacionxUsr/<int:ci_usuario>', devolverResultadoVotacionPorUsuario),
    path('votar/', sufragar),
    path('getListVotosHash/<int:votacion_id>', devolverListaVotosHash),
    path('terminarVotacion/<int:id_votacion>', terminarVotacion),
    path('getResultadoActual/<int:id_votacion>', calcularResultadoActal),

    path('resultadoAutomatico/<int:id_votacion>/', resultado_Automatico),
    path('resultadoAutomaticoReferendum/<int:id_referendum>/', resultado_Automatico_Referendum),

    path('getListVotosHashReferendum/<int:referendum_id>', devolverListaVotosHashReferendum),
    path('terminarReferendum/<int:id_referendum>', terminarReferendum),
    path('sufragarReferendum/', sufragarReferendum),
    path('calcResultado/<int:id_referendum>/', resultadoReferendum),
    path('getResultadoActualReferendum/<int:id_referendum>/', resultadoActualReferendum),
    path('getReferendumsxUsuario/<int:ci>/', devolverReferendumsPorUsuario),
    path('getReferendumssActivas/', devolverReferendumsActivas),
    path('calcResultadoReferendum/<int:id_referendum>/', devolverResultadoReferendum),
    path('getResultReferendumsxUsr/<int:ci_usuario>/', devolverResultadoReferendumPorUsuario),

]
