from django.urls import path
from . import views


urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name="signout"),
    path('order/', views.getorder, name="order"),
]