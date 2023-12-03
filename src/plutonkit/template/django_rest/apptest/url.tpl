from django.urls import path
from ({DJANGO_TEST_NAME}).apptest import views

urlpatterns = [
    path('apptest/', views.snippet_list),
    path('apptest/<int:pk>/', views.snippet_detail),
]
