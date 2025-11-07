from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Даты и время
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    
    # Место проведения
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    location = models.CharField(max_length=300, blank=True)
    online_link = models.URLField(blank=True)
    
    # Изображение
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    
    # Настройки
    max_attendees = models.PositiveIntegerField(default=0)  # 0 = без ограничений
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def available_seats(self):
        if self.max_attendees == 0:
            return "Без ограничений"
        registered = self.tickets.filter(status='confirmed').count()
        return self.max_attendees - registered

class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)  # "Standard", "VIP" и т.д.
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)  # 0 = без ограничений
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"