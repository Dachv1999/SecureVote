from django.db import models
from django.conf import settings
from Cuenta.models import Usuario
from django.db.models.deletion import CASCADE

class PadronElectoral(models.Model):
    nro_padron = models.PositiveIntegerField(primary_key=True)
    ci_usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nro_padron', 'ci_usuario'], name='unique_migration_host_combination'
            )
        ]


class Votacion(models.Model):
    Votacion_Tipos  = (('A', "Normal"), ('B', "Mixto"))
    tipo_votacion   = models.CharField(default='B', choices=Votacion_Tipos, max_length=1)
    id_padron       = models.ForeignKey(PadronElectoral,on_delete=CASCADE)
    inicio_votacion = models.DateTimeField()
    fin_votacion    = models.DateTimeField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class Voto(models.Model):
    ci_votante   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votante', on_delete=models.CASCADE, null=True)
    ci_candidato = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='candidato',on_delete=models.CASCADE, null=True)
    id_votacion  = models.ForeignKey(Votacion,on_delete=CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)


class Resultado(models.Model):
    GANADOR_ESTADO = (('G', "Ganador"), ('P', "Perdedor"))
    ci_candidato   = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    id_votacion    = models.ForeignKey(Votacion,on_delete=CASCADE)
    cant_votos     = models.IntegerField()
    estado_result  = models.CharField(default='P', choices=GANADOR_ESTADO, max_length=1)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)