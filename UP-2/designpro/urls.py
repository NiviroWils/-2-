from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


from cabinet.views import *
from designpro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cabinet/', include('cabinet.urls')),
    path('', RedirectView.as_view(url='/cabinet/', permanent=True)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
