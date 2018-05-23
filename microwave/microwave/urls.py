"""microwave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from myapp.views import (StartView, StatusView, microwave_event,)
from myapp.views import (status, timer_plus, timer_minus, power_plus, power_minus, clean_status,)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^start_page/$', StartView.as_view(), name="index"),
    url(r'^microwave/status/(?P<id>(\d)+)$', StatusView.as_view(), name="status"),
    url(r'^microwave/event$', microwave_event),
    url(r'^store/', include('myapp.urls')),

    path('', status),
    path('T+', timer_plus),
    path('T-', timer_minus),
    path('P+', power_plus),
    path('P-', power_minus),
    path('stop', clean_status),
]