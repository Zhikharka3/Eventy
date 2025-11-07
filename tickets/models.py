from django.db import models
from django.conf import settings
from events.models import Event, TicketType
import qrcode
from io import BytesIO
from django.core.files import File

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('reserved', 'Reserved'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('checked_in', 'Checked In'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    
    # Данные билета
    unique_code = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    
    # Цена на момент покупки
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.unique_code} - {self.attendee.email}"
    
    def save(self, *args, **kwargs):
        if not self.unique_code:
            import uuid
            self.unique_code = str(uuid.uuid4())
            
        if not self.qr_code:
            self.generate_qr_code()
            
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.unique_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        
        self.qr_code.save(f'qrcode_{self.unique_code}.png', File(buffer), save=False)