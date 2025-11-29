from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login/logout para usuários comuns
    path('accounts/', include('django.contrib.auth.urls')),

    # Site principal
    path('', include('noticias.urls')),
]