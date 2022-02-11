"""Maple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Maple.settings import base

url_routers = {
    "exchange": "exchange.urls",
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mg/', include("mg.urls")),
]

urlpatterns += [
    path(url, include(router)) for url, router in url_routers.items()
]

urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
