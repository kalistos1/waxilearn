
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/',include('accounts.urls')),
    path('',include('membership.urls')),
    path('signals/',include('signalsubscription.urls')),
    path('betting/',include('bettingsubscription.urls')),
    path('dashboard/',include('onlinecourses.urls')),
]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)