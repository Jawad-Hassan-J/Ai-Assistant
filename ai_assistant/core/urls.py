from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("plutonium/", views.plutonium, name="plutonium"),
    path('accounts/signup/', views.signup, name='signup'),

    path('content/create/',views.ContentCreate.as_view(), name='content_create'),
    path("profile/", views.profile, name="profile"),
    path("contents/", views.content_list, name="content_list"),

    path("contents/<int:content_id>/", views.content_detail, name="content_detail"), 
    path('content/<int:pk>/update/', views.ContentUpdate.as_view(), name='content_update'),
    path('content/<int:pk>/delete/', views.ContentDelete.as_view(), name='content_delete'),
]