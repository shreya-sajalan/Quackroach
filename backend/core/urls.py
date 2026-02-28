from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Route anything starting with 'api/' to your app
    path('api/', include('api.urls')),
]