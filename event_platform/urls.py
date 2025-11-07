from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Позже добавим сюда API routes:
    # path('api/auth/', include('users.urls')),
    # path('api/events/', include('events.urls')),
    # path('api/tickets/', include('tickets.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)