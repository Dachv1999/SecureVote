from django.contrib import admin
from Votacion.models import PadronElectoral, PartidoElectoral, Votacion, Voto, Resultado, Candidato

admin.site.register(PadronElectoral)
admin.site.register(Candidato)
admin.site.register(PartidoElectoral)
admin.site.register(Votacion)
admin.site.register(Voto)
admin.site.register(Resultado)
