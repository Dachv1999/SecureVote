from django.db import models
from django.conf import settings
from Cuenta.models import Usuario, PartidoElectoral
from django.db.models.deletion import CASCADE

class PadronElectoral(models.Model):
    nombre      = models.CharField(max_length=50, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nombre)

class PadronElectoralUsuario(models.Model):
    ci_usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    id_padron  = models.ForeignKey(PadronElectoral,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Votacion(models.Model):
    Votacion_Tipos   = (('N', "Normal"), ('M', "MayoriaAbsoluta"), ('P', "Proporcional"))
    nombre           = models.CharField(max_length=70, blank=True, null=True)
    tipo_votacion    = models.CharField(default='N', choices=Votacion_Tipos, max_length=1)
    inicio_votacion  = models.DateTimeField(blank=True, null=True)
    fin_votacion     = models.DateTimeField(blank=True, null=True)
    padron_electoral = models.ForeignKey(PadronElectoral,on_delete=models.CASCADE, null=True)
    partido1         = models.ForeignKey(PartidoElectoral,related_name='partido1',on_delete=models.CASCADE, null=True)
    partido2         = models.ForeignKey(PartidoElectoral,related_name='partido2',on_delete=models.CASCADE, null=True)
    partido3         = models.ForeignKey(PartidoElectoral,related_name='partido3',on_delete=models.CASCADE, null=True)
    partido4         = models.ForeignKey(PartidoElectoral,related_name='partido4',on_delete=models.CASCADE, null=True)
    activo           = models.BooleanField(default=True)
    escanio          = models.PositiveIntegerField(default=0,blank=True, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.nombre)


class Votacion_extended(models.Model):
    votacion_id = models.ForeignKey(Votacion, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.votacion_id)

class Voto(models.Model):
    VOTO_ESTADO = (('P', "Positivo"), ('A', "Abstencion"),('B', "Blanco"), ('N', "Nulo"))
    ci_votante   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votante', on_delete=models.CASCADE, null=True)
    ci_candidato = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='candidato',on_delete=models.CASCADE, null=True)
    hashvoto     = models.CharField(max_length=255, blank=True, null=True)
    index        = models.PositiveIntegerField(blank=True, null=True)
    id_votacion  = models.ForeignKey(Votacion,on_delete=CASCADE)
    tipo_voto    = models.CharField(default='A', choices=VOTO_ESTADO, max_length=1)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.tipo_voto)
    
class Voto_extended(models.Model):
    voto_id = models.ForeignKey(Voto, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.voto_id)


class Resultado(models.Model):
    GANADOR_ESTADO  = (('G', "Ganador"), ('P', "Perdedor"), ('E', "Empatador"))
    ci_candidato    = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    id_votacion     = models.ForeignKey(Votacion,on_delete=CASCADE)
    cant_votos      = models.IntegerField(default = 0,blank=True, null=True)
    cant_vblanco    = models.IntegerField(default = 0,blank=True, null=True)
    cant_vpositivo  = models.IntegerField(default = 0,blank=True, null=True)
    cant_vnullo     = models.IntegerField(default = 0,blank=True, null=True)
    total_votos     = models.IntegerField(default = 0,blank=True, null=True)
    escanio_asig    = models.PositiveIntegerField(default = 0,blank=True, null=True)
    estado_result   = models.CharField(default='P', choices=GANADOR_ESTADO, max_length=1)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cant_votos)

class Resultado_extended(models.Model):
    resultado_id = models.ForeignKey(Resultado, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.resultado_id)
    


class Referendum(models.Model):
    nombre           = models.CharField(max_length=70, blank=True, null=True)
    pregunta         = models.CharField(max_length=255, blank=True, null=True)
    inicio_referendum= models.DateTimeField(blank=True, null=True)
    fin_referendum   = models.DateTimeField(blank=True, null=True)
    padron_electoral = models.ForeignKey(PadronElectoral,on_delete=models.CASCADE, null=True)
    activo           = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.nombre)
    
class Referendum_extended(models.Model):
    referendum_id = models.ForeignKey(Referendum, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.referendum_id)
    
class VotoReferendum(models.Model):
    VOTO_ESTADO = (('S', "Si"),('N', "No"), ('A', "Abstencion"),('B', "Blanco"), ('U', "Nulo"))
    ci_votante   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='elector', on_delete=models.CASCADE, null=True)
    hashvoto     = models.CharField(max_length=255, blank=True, null=True)
    index        = models.PositiveIntegerField(blank=True, null=True)
    id_referendum  = models.ForeignKey(Referendum,on_delete=CASCADE)
    tipo_voto    = models.CharField(default='N', choices=VOTO_ESTADO, max_length=1)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.tipo_voto)
    
class VotoReferendum_extended(models.Model):
    votoref_id = models.ForeignKey(VotoReferendum, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.votoref_id)


class ResultadoReferendum(models.Model):
    GANADOR_ESTADO = (('S', "Si"),('N', "No"), ('A', "Abstencion"),('B', "Blanco"), ('U', "Nulo"))
    id_referendum   = models.ForeignKey(Referendum,on_delete=CASCADE)
    cant_vsi        = models.IntegerField(default = 0,blank=True, null=True)
    cant_vblanco    = models.IntegerField(default = 0,blank=True, null=True)
    cant_vno        = models.IntegerField(default = 0,blank=True, null=True)
    cant_vnullo     = models.IntegerField(default = 0,blank=True, null=True)
    total_votos     = models.IntegerField(default = 0,blank=True, null=True)
    ganador         = models.CharField(default='B', choices=GANADOR_ESTADO, max_length=1)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.total_votos)

class ResultadoReferendum_extended(models.Model):
    resultado_id = models.ForeignKey(ResultadoReferendum, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.resultado_id)