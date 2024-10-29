from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with all permissions."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    identification = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    is_asesor = models.BooleanField(default=False)
    is_constructora = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'identification']

    def __str__(self):
        return self.email

class AsesorComercial(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="asesor_comercial")
    foto = models.ImageField(upload_to='asesores_fotos/', null=True, blank=True)
    biografia = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    reseñas = models.TextField(blank=True, null=True)
    numero_ventas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.name

class ConstructoraInmobiliaria(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="constructora_inmobiliaria")
    tiempo_constitucion = models.PositiveIntegerField(help_text="Años de constitución")
    representante_legal = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
