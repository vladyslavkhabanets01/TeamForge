from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('lfg/', include('lfg.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
