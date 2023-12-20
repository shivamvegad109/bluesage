from django.urls import path
from . import views


urlpatterns = [
    path('', views.shop_page, name='shop'),
    path(
        'product/<product_id>', views.product_details, name='product-details'
    ),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('category/<category_id>', views.category, name='category'),
    path('add_to_cart/', views.add_product, name='add_to_cart'),
    path('add-to-wishlist/', views.add_prodcut_to_wishlist, name='add-to-wishlist'),
    # remove-wishlist-item
    path('remove-wishlist-item/', views.remove_from_wishlist, name='remove-wishlist-item'),

]
