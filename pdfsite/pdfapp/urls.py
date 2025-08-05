from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('merge/', views.merge_pdfs, name='merge_pdfs'),
    path('split/', views.split_pdf, name='split_pdf'),
    path('extract-text/', views.extract_text, name='extract_text'),



]
