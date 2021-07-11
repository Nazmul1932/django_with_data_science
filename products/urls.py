from django.urls import path
from .views import char_select_view, add_purchase_view, salesDistView

app_name = 'products'

urlpatterns = [
    path('', char_select_view, name='main-products-view'),
    path('add_purchase/', add_purchase_view, name='add-purchase-view'),
    path('sales/', salesDistView, name='sales-dis-view'),
]