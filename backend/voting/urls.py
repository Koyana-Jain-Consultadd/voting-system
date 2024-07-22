from django.urls import path
from . import views

urlpatterns = [
    path("",views.userSignup, name="signup"),
    path("login/",views.userLogin, name="login"),
    path('home', views.home_view, name='home'),
    path('votingpanel', views.votingpanel, name='votingpanel'),
    path("logout/", views.userLogout, name="logout"),
]