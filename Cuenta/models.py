from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.deletion import CASCADE

####################################################################
##          Funciones object para crear user y suoeruser          ## 
####################################################################

class UsuarioManager(BaseUserManager): 
    
    def create_user(self, ci, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico!')

        user = self.model(
            ci       = ci,
            email    = self.normalize_email(email),
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ci, email, password=None):

        user = self.create_user(
            ci       = ci,
            email    = self.normalize_email(email),
            password = password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class PartidoElectoral(models.Model):
    nombre_partido = models.CharField(max_length=50, unique=True)
    Sigla          = models.CharField(max_length=6, unique=True)
    #logo
    Slogan         = models.CharField(max_length=100, blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_partido

############################################################################
##      Overide de la clase User para definir mis propios atributos       ## 
############################################################################

class Usuario(AbstractBaseUser):
    ci               = models.PositiveIntegerField(primary_key=True)
    cuenta           = models.CharField(max_length=255, unique=True, blank=True, null=True)
    nombre           = models.CharField(max_length=50, blank=True, null=True)
    apellido         = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    ciudad           = models.CharField(max_length=15, blank=True, null=True)
    email            = models.EmailField(max_length=80, unique=True)
    informacion      = models.CharField(max_length=100, blank=True, null=True)
    telefono         = models.IntegerField(validators=[MinValueValidator(70000000), MaxValueValidator(79999999)], blank=True, null=True)
    longitud         = models.CharField(max_length=80, blank=True, null=True)
    latitud          = models.CharField(max_length=80, blank=True, null=True)
    id_partido       = models.ForeignKey(PartidoElectoral, on_delete=CASCADE, blank=True, null=True)

    is_active        = models.BooleanField(default=True)
    is_superuser     = models.BooleanField(default=False)
    is_staff         = models.BooleanField(default=False)
    date_joined      = models.DateTimeField(default=timezone.now)
    last_login       = models.DateTimeField(blank=True, null=True)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    objects          = UsuarioManager() 

    USERNAME_FIELD  = 'email'
    EMAIL_FIELD     = 'email'
    REQUIRED_FIELDS = ['ci']

    def __str__(self):
        return str(self.nombre)
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True




