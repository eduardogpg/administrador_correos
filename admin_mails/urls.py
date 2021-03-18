from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf import settings
from django.conf.urls.static import static

from .views import index
from .views import footer

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),

    path('footer/', footer, name='footer'),

    path('mails/', include('mails.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
