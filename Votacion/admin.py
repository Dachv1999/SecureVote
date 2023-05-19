from django.contrib import admin
from Votacion.models import PadronElectoral, Votacion, Voto, Resultado

admin.site.register(PadronElectoral)
admin.site.register(Votacion)
admin.site.register(Voto)
admin.site.register(Resultado)
