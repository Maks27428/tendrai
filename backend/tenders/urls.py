from django.urls import path
from . import views

urlpatterns = [
    path('tenders/', views.tender_list, name='tender-list'),
    path('tenders/upload/', views.tender_upload, name='tender-upload'),
    path('tenders/demo-pdfs/', views.demo_pdf_list, name='demo-pdf-list'),
    path('tenders/demo-pdfs/<str:filename>/', views.demo_pdf_download, name='demo-pdf-download'),
    path('tenders/monopoly-check/', views.monopoly_check, name='monopoly-check'),
    path('tenders/<int:pk>/', views.tender_detail, name='tender-detail'),
    path('tenders/<int:pk>/export/', views.tender_export, name='tender-export'),
    path('tenders/<int:pk>/stream/', views.tender_stream, name='tender-stream'),
]
