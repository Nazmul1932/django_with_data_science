from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view,login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('login/', login_view, name='login_view'),
    path('performance/', include('products.urls', namespace='products')),
    path('upload/', include('csvs.urls', namespace='csvs')),
    path('customer/', include('customers.urls', namespace='customers')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
