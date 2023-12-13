from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from card.views import IDCardPDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate_id_cards/<int:pk>/', IDCardPDFView.as_view(), name='generate_id_cards'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
