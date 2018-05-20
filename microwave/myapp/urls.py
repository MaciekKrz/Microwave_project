from django.conf.urls import url
from .views import view_cached_product

urlpatterns = [
    url(r'^cache/', view_cached_product),
]