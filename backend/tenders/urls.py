from django.urls import path
from . import views

urlpatterns = [
    path('tenders/', views.tender_list, name='tender-list'),
    path('tenders/upload/', views.tender_upload, name='tender-upload'),
    path('tenders/<int:pk>/', views.tender_detail, name='tender-detail'),
    path('tenders/<int:pk>/stream/', views.tender_stream, name='tender-stream'),
]
