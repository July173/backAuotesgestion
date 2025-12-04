from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from .Person import Person
from .Role import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es requerido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    class Meta:
        db_table = 'user'
    
    registered = models.BooleanField(default=True, help_text="True si el usuario está registrado pero no activado. False si ya fue activado.")
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    login_code = models.CharField(max_length=10, null=True, blank=True, help_text="Código de verificación para 2FA por correo")
    login_code_expiration = models.DateTimeField(null=True, blank=True, help_text="Fecha de expiración del código de 2FA")
    login_code_used = models.BooleanField(null=True, default=False, help_text="Indica si el código de 2FA ya fue usado")
    
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campos para recuperación de contraseña
    reset_code = models.CharField(max_length=10, null=True, blank=True)
    reset_code_expiration = models.DateTimeField(null=True, blank=True)

    # Agregar related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='api_users',
        related_query_name='api_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='api_users',
        related_query_name='api_user',
    )

    objects = UserManager()

    # ✅ CAMPOS REQUERIDOS PARA AbstractBaseUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Campos requeridos además del USERNAME_FIELD

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email

    def soft_delete(self):
        """Marca el usuario como eliminado sin borrarlo de la BD"""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        """Restaura un usuario eliminado"""
        self.deleted_at = None
        self.is_active = True
        self.save()

    @property
    def is_deleted(self):
        """Verifica si el usuario está eliminado"""
        return self.deleted_at is not None
