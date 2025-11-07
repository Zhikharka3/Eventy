from django.contrib import admin
from .models import Event, Category, TicketType

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'category', 'start_date', 'event_type', 'is_published', 'available_seats_display')
    list_filter = ('event_type', 'is_published', 'is_free', 'category', 'start_date')
    search_fields = ('title', 'description', 'organizer__email')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'organizer', 'category', 'image')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Location', {
            'fields': ('event_type', 'location', 'online_link')
        }),
        ('Settings', {
            'fields': ('max_attendees', 'is_published', 'is_free')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def available_seats_display(self, obj):
        return obj.available_seats
    available_seats_display.short_description = 'Available Seats'

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'price', 'quantity', 'tickets_sold')
    list_filter = ('event',)
    search_fields = ('name', 'event__title')
    
    def tickets_sold(self, obj):
        return obj.ticket_set.filter(status='confirmed').count()
    tickets_sold.short_description = 'Tickets Sold'