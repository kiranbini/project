from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('shop/', views.shop, name='shop'),
    path('category/<slug:link>', views.shop, name='by_category'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product_search/', views.Product_search, name='product_search'),
    path("shop-single/<int:pro_id>",views.single_product, name='pro_details'),
    path("feedback/<int:pro_id>", views.addfeedback, name='feedback'),
    path('order_view', views.order_confirmation, name='order_view')
]
