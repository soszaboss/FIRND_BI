from django.urls import path
from .views import file_watermarked

urlpatterns = [
    path('download-diploma/<path:url>/', file_watermarked, name='download-diploma'),
]
