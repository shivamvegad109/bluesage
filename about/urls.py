from django.urls import path
from .views import about_page, wishlist


urlpatterns = [
    # path('', about_page, name='about'),
    path('', wishlist, name='about')
]
