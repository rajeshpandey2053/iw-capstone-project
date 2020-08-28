from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


API_TITLE = 'Hamro Note API'
API_DESCRIPTION = ' A Web API for sharing notes of college'

schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/blog/',include('blog.api.urls')),
    path('api/accounts/', include('accounts.urls', namespace='account')),
    path('api/posts/', include('posts.urls', namespace='posts')),
    path('schema/',schema_view),
    path('',include_docs_urls(title=API_TITLE,description=API_DESCRIPTION)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Hamro Notes'
