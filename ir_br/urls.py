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
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from ir_br import views

# Include the router to the patterns
urlpatterns = [
    path('ir_br', views.IrBrApiView.as_view(), name="ir_br"),
    re_path(r'^ir_br/(?P<date>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})/$', views.IrBrApiGetView.as_view(), name="ir_br_date"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
