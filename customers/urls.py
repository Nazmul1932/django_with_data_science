from django.urls import path
from .views import customerCorrView

app_name = 'customers'

urlpatterns = [
    path('', customerCorrView, name='main-customer-corr-view'),
]