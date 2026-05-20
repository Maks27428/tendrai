from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('auth/register/', auth_views.register, name='auth-register'),
    path('auth/login/', auth_views.login_view, name='auth-login'),
    path('auth/me/', auth_views.me, name='auth-me'),
    path('tenders/', views.tender_list, name='tender-list'),
    path('tenders/upload/', views.tender_upload, name='tender-upload'),
    path('tenders/demo-pdfs/', views.demo_pdf_list, name='demo-pdf-list'),
    path('tenders/demo-pdfs/<str:filename>/', views.demo_pdf_download, name='demo-pdf-download'),
    path('tenders/monopoly-check/', views.monopoly_check, name='monopoly-check'),
    path('tenders/search-goszakup/', views.search_goszakup, name='search-goszakup'),
    path('health/llm/', views.health_llm, name='health-llm'),
    path('tenders/analyze-goszakup/', views.analyze_goszakup, name='analyze-goszakup'),
    path('tenders/<int:pk>/', views.tender_detail, name='tender-detail'),
    path('tenders/<int:pk>/export/', views.tender_export, name='tender-export'),
    path('tenders/<int:pk>/stream/', views.tender_stream, name='tender-stream'),
]
