from django.urls import path
from .  import views
from django.views.generic import TemplateView
from . import views,models
from django.views.generic.detail import DetailView
from django.contrib.auth import views as auth_views

from . import forms
app_name='search'
urlpatterns=[
    path("login/",auth_views.LoginView.as_view(template_name="login.html",form_class=forms.authenticationform,),name="login",),
    path("signup/", views.signupview.as_view(), name="signup"),
    path( "products/", views.productlistview.as_view(), name="products" ),
    path("products/<slug:tag>/", views.productlistview.as_view(),name="products",),
    path("product/<slug:slug>/", DetailView.as_view(model= models.product),name="product",),   
    path("",TemplateView.as_view(template_name="pages/home.html"),name="home",),
    path("note/",views.notelistview.as_view(),name="notes_list"),
    path('create_note/', views.NoteqrView.as_view(), name='create_note'),

    path("note/create/",views.notecreateview.as_view(),name='note_create'),
    path("note/<int:pk>/",views.noteupdateview.as_view(),name="note_update"),
    path("note/<int:pk>/delete/",views.notedeleteview.as_view(),name="note_delete",),
]
