from django.urls import path
from . import views
from . import tests
urlpatterns = [
    path('', views.cart_page, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('remove_item/', views.remove_from_cart, name='remove_item'),
    path('payment/', views.payment, name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # test
    # path('', tests.homepage, name='cart'),
    #  path('paymenthandler/', tests.paymenthandler, name='paymenthandler'),

]
