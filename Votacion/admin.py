from django.contrib import admin
from Votacion.models import PadronElectoral, Votacion, Voto, Resultado, PadronElectoralUsuario, Referendum, VotoReferendum, ResultadoReferendum

admin.site.register(PadronElectoral)
admin.site.register(PadronElectoralUsuario)
admin.site.register(Votacion)
#admin.site.register(Votacion_extended)
admin.site.register(Voto)
#admin.site.register(Voto_extended)
admin.site.register(Resultado)
#admin.site.register(Resultado_extended)
admin.site.register(Referendum)
admin.site.register(VotoReferendum)
admin.site.register(ResultadoReferendum)
