from django.urls import path
from . import views

urlpatterns = [
    
    path("register/",views.SignUpView.as_view(),name='register'),
    path("login/",views.SignInView.as_view(),name='login'),
    path('logout/',views.logoutpage,name='logout'),
]
