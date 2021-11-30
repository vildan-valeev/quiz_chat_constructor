from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from constructor.views import main_page
from . import settings
from .yasg import urlpatterns as swagger_urls


urlpatterns = [
    path("", main_page, name="main"),
    path('admin/', admin.site.urls),

    path('api/constructor/', include('constructor.urls')),

    path('api/users/', include('users.urls')),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += swagger_urls


