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
from django.urls import re_path

from operation import views

# Include the router to the patterns
urlpatterns = [
    re_path(r'^operation/(?P<pk>[0-9]+)/archive\.(?P<format>[a-z0-9]+)?/?$', views.ArchiveApiView.as_view(), name="archive"),
    #  url(r'^operation/(?P<pk>[0-9]+)/cost/?$', views.OperationCostView.as_view(), name="operation-cost"),
    #  url(r'^operation/(?P<pk>[0-9]+)/cost\.(?P<format>[a-z0-9]+)/?$', views.OperationCostView.as_view(), name="operation-cost"),
]
