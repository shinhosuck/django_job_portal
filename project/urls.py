from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job_portal.urls', namespace='job_portal')),
    path('', include('accounts.urls', namespace='accounts')),
    path('social-auth/',include('social_django.urls', namespace='social'))
]
urlpatterns += debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)