from django.db import models
from Cuenta.models import Persona, Usuario
from django.db.models.deletion import CASCADE



class PartidoElectoral(models.Model):
    nombre_partido = models.CharField(max_length=50, unique=True)
    Sigla          = models.CharField(max_length=6, unique=True)
    #logo
    Slogan         = models.CharField(max_length=100)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_partido

class Candidato (Persona):
    id_partido = models.ForeignKey(PartidoElectoral,on_delete=CASCADE)

    def __str__(self):
        return self.nombre

class PadronElectoral(models.Model):
    nro_padron = models.PositiveIntegerField(primary_key=True)
    ci_usuario = models.ForeignKey(Usuario,on_delete=CASCADE, null=True)
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
    ci_votante   = models.ForeignKey(Usuario,on_delete=CASCADE)
    ci_candidato = models.ForeignKey(Candidato,on_delete=CASCADE)
    id_votacion  = models.ForeignKey(Votacion,on_delete=CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)


class Resultado(models.Model):
    GANADOR_ESTADO = (('G', "Ganador"), ('P', "Perdedor"))
    ci_candidato   = models.ForeignKey(Candidato,on_delete=CASCADE)
    id_votacion    = models.ForeignKey(Votacion,on_delete=CASCADE)
    cant_votos     = models.IntegerField()
    estado_result  = models.CharField(default='P', choices=GANADOR_ESTADO, max_length=1)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)