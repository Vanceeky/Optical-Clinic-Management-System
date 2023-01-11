
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_dashboard.urls')),
    path('', include('appointment.urls')),
    path('', include('inventory.urls')),
    path('', include('authentication.urls')),
]


handler404 = 'clinic.custom_views.handler404'
handler500 = 'clinic.custom_views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
