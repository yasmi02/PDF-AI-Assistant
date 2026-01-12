from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('ask/', views.ask_question, name='ask_question'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/summary/', views.generate_summary, name='generate_summary'),
    path('documents/<int:pk>/delete/', views.delete_document, name='delete_document'),
    path('questions/', views.question_history, name='question_history'),
]