from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from .views import index

urlpatterns = [
    path('',index),
    path('admin/', admin.site.urls),
    path('api/blog/',include('blog.api.urls')),
    path('api/accounts/', include('accounts.urls', namespace='account')),
    path('api/posts/', include('posts.urls', namespace='posts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Hamro Notes'
