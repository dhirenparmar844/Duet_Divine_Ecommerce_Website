from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('cart/',views.cart,name='cart'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('shop/',views.shop,name='shop'),
    path('change_password/',views.change_password,name='change_password'),
    path('shop_single/',views.shop_single,name='shop_single'),
    path('seller_index',views.seller_index,name='seller_index'),
    path('seller_change_password/',views.seller_change_password,name='seller_change_password'),
    path('seller_add_product/',views.seller_add_product,name='seller_add_product'),
    path('seller_view_product/',views.seller_view_product,name='seller_view_product'),
    path('seller_edit_prodouct/<int:pk>',views.seller_edit_product,name='seller_edit_product'),
    path('seller_delete_product/<int:pk>',views.seller_delete_product,name='seller_delete_product'),
    path('category_men/',views.category_men,name='category_men'),
    path('category_women/',views.category_women,name='category_women'),
    path('category_kids/',views.category_kids,name='category_kids'),
    path('color_red/',views.color_red,name='color_red'),
    path('color_green/',views.color_green,name='color_green'),
    path('color_blue/',views.color_blue,name='color_blue'),
    path('color_white/',views.color_white,name='color_white'),
    path('product_detail/<int:pk>',views.product_detail,name='product_detail'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add_to_wishlist/<int:pk>',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/<int:pk>',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>',views.remove_from_cart,name='remove_from_cart'),
    path('cart/',views.cart,name='cart'),
    path('change_qty/',views.change_qty,name='change_qty'),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('search/',views.search,name='search'),
    path('seller_orders/',views.seller_orders,name='seller_orders'),
    path('change_password/',views.change_password,name='change_password'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('otp/',views.verify_otp,name='verify_otp'),
    path('new_password/',views.new_password,name='new_password'),
    path('billing_details/',views.billing_details,name='billing_details'),
    path('profile/',views.profile,name='profile'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('seller_profile/',views.seller_profile,name='seller_profile'),
    path('seller_profile_update/',views.seller_profile_update,name='seller_profile_update'),
    path('seller_order_detail/',views.seller_order_detail,name='seller_order_detail')




    











    

]