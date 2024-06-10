from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='index'),
    path('download_pdf/<int:id>/', views.download_pdf, name='download_pdf'),
    path('upload_pdf', views.upload_word, name='upload_word'),
    path('download_word/<int:id>/', views.download_word, name='download_word'),
]
