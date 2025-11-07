from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class UserType(models.TextChoices):
        ORGANIZER = 'organizer', _('Organizer')
        ATTENDEE = 'attendee', _('Attendee')
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20, 
        choices=UserType.choices, 
        default=UserType.ATTENDEE
    )
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Для организаторов
    organization_name = models.CharField(max_length=200, blank=True)
    organization_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Используем email вместо username для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # ОБРАТИТЕ ВНИМАНИЕ: здесь 'username'
    
    def __str__(self):
        return self.email
    
    @property
    def is_organizer(self):
        return self.user_type == self.UserType.ORGANIZER
    
    @property
    def is_attendee(self):
        return self.user_type == self.UserType.ATTENDEE