from django.contrib import admin
from .models import Ticket, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'created_at', 'ticket_count')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def ticket_count(self, obj):
        return obj.tickets.count()
    ticket_count.short_description = 'Tickets'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'event', 'attendee', 'ticket_type', 'status', 'final_price', 'created_at')
    list_filter = ('status', 'event', 'ticket_type', 'created_at')
    search_fields = ('unique_code', 'attendee__email', 'event__title')
    readonly_fields = ('unique_code', 'qr_code', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('unique_code', 'event', 'ticket_type', 'attendee', 'order')
        }),
        ('Status & Price', {
            'fields': ('status', 'final_price')
        }),
        ('QR Code', {
            'fields': ('qr_code',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )