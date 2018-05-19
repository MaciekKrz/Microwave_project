from django.conf.urls import url
from .views import viewProduct, view_cached_product

urlpatterns = [
    url(r'^$', viewProduct),
    url(r'^cache/', view_cached_product),
]