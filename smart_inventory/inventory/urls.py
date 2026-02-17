from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import signup_view

router = DefaultRouter()

router.register('suppliers', views.SupplierViewSet)

router.register('products', views.ProductViewSet)

router.register('transactions', views.StockTransactionViewSet)

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('add-supplier/', views.add_supplier, name='add_supplier'),

    path('add-product/', views.add_product, name='add_product'),

    path('add-transaction/', views.add_transaction, name='add_transaction'),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('api/', include(router.urls)),

    path('export-products/', views.export_products_csv, name='export_products'),

    path('export-transactions/', views.export_transactions_csv, name='export_transactions'),

    path("signup/", signup_view, name="signup"),

]
