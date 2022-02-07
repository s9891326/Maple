from django.urls import path

from mg import views

app_name = "mg"

urlpatterns = [
    path('add/', views.add, name="add"),
    path('delete/', views.delete, name="delete"),
]
