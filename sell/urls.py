"""location URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

For the django rest used here please see:
    http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/

Examples:
    1. snippet_list = SnippetViewSet.as_view({'get': 'list','post': 'create'})
"""

# Create a router for the viewset
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from sell import views

router = DefaultRouter()

# Register the viewset
router.register(r'sell', views.SellDataViewSet, basename='sell')
router.register(r'sell_paginate', views.SellPaginatedDataViewSet, basename='sell_pagination')

# Include the router to the patterns
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^risk/$', views.RiskDataApiView.as_view(), name="risk_data"),
    url(r'^risk\.(?P<format>[a-z0-9]+)/?$', views.RiskDataApiView.as_view(), name="risk_data"),
]
